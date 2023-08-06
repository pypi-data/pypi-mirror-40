""" ResNet Bottleneck as node operator
    BatchNorm2d+ReLU in the first layer and each AOGBlock
    Different units in a stage split the outchannels evenly 
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function  # force to use print as function print(args)
from __future__ import unicode_literals

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from .aog.AOG import *
#from cfgs.config2 import cfg       # old cfg
from .config import cfg         # new cfg
from .operator import *


_bias = False
_inplace = True


########################################### MixedOps ################################################

class MixedOp(nn.Module):
    def __init__(self, cin, cout, stride, dropRate, group=1):
        super(MixedOp, self).__init__()
        self._ops = nn.ModuleList()
        for name in cfg.search.op_candidates:
            op = OPS[name](cin, cout, stride, dropRate, group)
            self._ops.append(op)

    def forward(self, x, weights):
        return sum(w * op(x) for w, op in zip(weights, self._ops))

            
class MixedOp_Lateral(nn.Module):
    def __init__(self, cin, cout, stride, dropRate, group=1):
        super(MixedOp_Lateral, self).__init__()
        self._ops = nn.ModuleList()
        for name in cfg.search.op_candidates_lateral:
            op = OPS[name](cin, cout, stride, dropRate, group)
            self._ops.append(op)

    def forward(self, x, xall, weights):
        return sum(w * op(x, xall) for w, op in zip(weights, self._ops))

########################################### AOG Block ################################################
 
### AOG build block
class AOGBlock(nn.Module):    
    def __init__(self, stage, unit, aog, inchannels, outchannels, dropRate, stride):
        super(AOGBlock, self).__init__()        
        self.stage = stage
        self.unit = unit
        self.aog = aog                
        self.inchannels = inchannels
        self.outchannels = outchannels
        self.dropRate = dropRate
        self.stride = stride            
        
        self.dim = aog.param.grid_wd
        self.in_slices = self.calculate_slices(self.dim, inchannels)
        self.out_slices = self.calculate_slices(self.dim, outchannels)

        self.node_set = aog.node_set
        self.primitive_set = aog.primitive_set
        self.BFS = aog.BFS
        self.DFS = aog.DFS

        self.NodeOpCnt = 0
        self.NodeOpLateralCnt = 0
        self.mapping = [[], []]

        self.hasLateral = {}

        self.or_node_info = {}
        self.set_weights_attr()

        if 'operator' in cfg.search.space:
            if cfg.search.mode == 'individual':
                self.alphas = [Variable(1e-3*torch.randn(self.NodeOpCnt, len(cfg.search.op_candidates)).cuda(), requires_grad=True), \
                        Variable(1e-3*torch.randn(self.NodeOpLateralCnt, len(cfg.search.op_candidates_lateral)).cuda(), requires_grad=True)]
                AOGNet._arch_parameters['stage_{}_unit_{}'.format(self.stage, self.unit)] = [self.alphas, self.mapping]
            elif cfg.search.mode == 'shared':
                if 'shared' not in AOGNet._arch_parameters:
                    self.alphas = [Variable(1e-3*torch.randn(self.NodeOpCnt, len(cfg.search.op_candidates)).cuda(), requires_grad=True), \
                            Variable(1e-3*torch.randn(self.NodeOpLateralCnt, len(cfg.search.op_candidates_lateral)).cuda(), requires_grad=True)]
                    AOGNet._arch_parameters['shared'] = [self.alphas, self.mapping]
                else:
                    self.alphas = AOGNet._arch_parameters['shared'][0]
        if 'structure' in cfg.search.space:
            if cfg.search.mode == 'individual':
                self.beta = {}
                for k, v in self.or_node_info.items():
                    self.beta[k] = Variable(1e-3*torch.randn(1, v).cuda(), requires_grad=True)
                AOGNet._arch_parameters['beta_stage_{}_unit_{}'.format(self.stage, self.unit)] = self.beta
            elif cfg.search.mode == 'shared':
                if 'beta_shared' not in AOGNet._arch_parameters:
                    self.beta = {}
                    for k, v in self.or_node_info.items():
                        self.beta[k] = Variable(1e-3*torch.randn(1, v).cuda(), requires_grad=True)
                    AOGNet._arch_parameters['beta_shared'] = self.beta
                else:
                    self.beta = AOGNet._arch_parameters['beta_shared']


    def calculate_slices(self, dim, channels):
        slices = [0] * dim
        for i in range(channels):
            slices[i % dim] += 1
        for d in range(1, dim):
            slices[d] += slices[d - 1]
        slices = [0] + slices
        return slices
              
    def set_weights_attr(self):                
        for id_ in self.DFS:
            node = self.node_set[id_]            
            arr = self.primitive_set[node.rect_idx]
            groups = arr.Width()   if cfg.aognet.use_group_conv else 1
            if node.node_type == NodeType.TerminalNode:                
                inplane = self.inchannels if cfg.aognet.terminal_node_no_slice[self.stage] else \
                            self.in_slices[arr.x2 + 1] - self.in_slices[arr.x1]
                outplane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]
                stride = self.stride
                
                if 'operator' in cfg.search.space:
                    setattr(self, 'weight' + str(node.id), MixedOp(inplane, outplane, stride, self.dropRate)) #, groups))
                else:
                    setattr(self, 'weight' + str(node.id), OPS[cfg.aognet.node_op](inplane, outplane, stride, self.dropRate)) #, groups))
                self.NodeOpCnt += 1
                self.mapping[0].append(node.id)

            elif node.node_type == NodeType.AndNode:                
                plane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]                
                stride = 1

                self.hasLateral[node.id] = False
                for chid in node.child_ids:
                    ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                    if arr.Width() == ch_arr.Width():
                        self.hasLateral[node.id] = True
                        break
                
                if self.hasLateral[node.id]:
                    if 'operator' in cfg.search.space:
                        setattr(self, 'weight' + str(node.id), MixedOp_Lateral(plane, plane, stride, self.dropRate, groups))
                    else:
                        setattr(self, 'weight' + str(node.id), OPS[cfg.aognet.node_op_lateral](plane, plane, stride, self.dropRate, groups))
                    self.NodeOpLateralCnt += 1
                    self.mapping[1].append(node.id)
                else:
                    if 'operator' in cfg.search.space:
                        setattr(self, 'weight' + str(node.id), MixedOp(plane, plane, stride, self.dropRate, groups))
                    else:
                        setattr(self, 'weight' + str(node.id), OPS[cfg.aognet.node_op](plane, plane, stride, self.dropRate, groups))
                    self.NodeOpCnt += 1
                    self.mapping[0].append(node.id)

            elif node.node_type == NodeType.OrNode:     
                assert self.node_set[node.child_ids[0]].node_type != NodeType.OrNode                                                           
                plane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]
                stride = 1

                self.hasLateral[node.id] = False
                for chid in node.child_ids:
                    ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                    if self.node_set[chid].node_type == NodeType.OrNode or arr.Width() < ch_arr.Width():                        
                        self.hasLateral[node.id] = True
                        break
                
                if self.hasLateral[node.id]:
                    assert 'structure' not in cfg.search.space, "or node structure search doenn't support lateral connection"
                    if 'operator' in cfg.search.space:
                        setattr(self, 'weight' + str(node.id), MixedOp_Lateral(plane, plane, stride, self.dropRate, groups))
                    else:
                        setattr(self, 'weight' + str(node.id), OPS[cfg.aognet.node_op_lateral](plane, plane, stride, self.dropRate, groups))
                    self.NodeOpLateralCnt += 1
                    self.mapping[1].append(node.id)
                else:
                    if 'operator' in cfg.search.space:
                        setattr(self, 'weight' + str(node.id), MixedOp(plane, plane, stride, self.dropRate, groups))
                    else:
                        setattr(self, 'weight' + str(node.id), OPS[cfg.aognet.node_op](plane, plane, stride, self.dropRate, groups))
                    self.NodeOpCnt += 1
                    self.mapping[0].append(node.id)
                    if 'structure' in cfg.search.space and len(node.child_ids)>1:
                        self.or_node_info[str(node.id)] = len(node.child_ids)

    def forward(self, x):       
        if 'operator' in cfg.search.space:
            weights = F.softmax(self.alphas[0], dim=-1)
            if self.NodeOpLateralCnt:
                weights_lateral = F.softmax(self.alphas[1], dim=-1)
        NodeIdTensorDict = {}
        NodeOpCnt, NodeOpLateralCnt = 0, 0
        for id_ in self.DFS:
            node = self.node_set[id_]
            arr = self.primitive_set[node.rect_idx]
            if node.node_type == NodeType.TerminalNode:                
                right, left = self.in_slices[arr.x2 + 1], self.in_slices[arr.x1]                       
                tnode_tensor = x if cfg.aognet.terminal_node_no_slice[self.stage] else x[:, left:right, :, :].contiguous()
                # assert tnode_tensor.requires_grad, 'slice needs to retain grad'
                if 'operator' in cfg.search.space:
                    tnode_output = getattr(self, 'weight' + str(node.id))(tnode_tensor, weights[NodeOpCnt])
                else:
                    tnode_output = getattr(self, 'weight' + str(node.id))(tnode_tensor)
                NodeOpCnt += 1
                NodeIdTensorDict[node.id] = tnode_output
                # print('{}-{}: tnode{} {} {}'.format(self.stage, self.unit, node.id, tnode_tensor.size(), tnode_output.size()))
            elif node.node_type == NodeType.AndNode:               
                child_tensor = []
                for chid in node.child_ids:
                    ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                    if arr.Width() > ch_arr.Width():
                        child_tensor.append(NodeIdTensorDict[chid])                    
                anode_tensor = torch.cat(child_tensor, 1)

                if self.hasLateral[node.id]:
                    parent_ids1 = set(node.parent_ids)                    
                    for chid in node.child_ids:
                        ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                        parent_ids2 = self.node_set[chid].parent_ids
                        if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) == 0: # need to check if they share non-root ancestor(s)
                            anode_tensor = anode_tensor + NodeIdTensorDict[chid]
                            
                    anode_tensor_all = anode_tensor
                    for chid in node.child_ids:
                        ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                        parent_ids2 = self.node_set[chid].parent_ids
                        if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) > 0:
                            anode_tensor_all = anode_tensor_all +  NodeIdTensorDict[chid]
                    if 'operator' in cfg.search.space:
                        anode_output = getattr(self, 'weight'+str(node.id))(anode_tensor, anode_tensor_all, weights_lateral[NodeOpLateralCnt])
                    else:
                        anode_output = getattr(self, 'weight'+str(node.id))(anode_tensor, anode_tensor_all)
                    NodeOpLateralCnt += 1
                else:
                    if 'operator' in cfg.search.space:
                        anode_output = getattr(self, 'weight' + str(node.id))(anode_tensor, weights[NodeOpCnt])
                    else:
                        anode_output = getattr(self, 'weight' + str(node.id))(anode_tensor)
                    NodeOpCnt += 1
                NodeIdTensorDict[node.id] = anode_output
                # print('{}-{} anode{} {} {}'.format(self.stage, self.unit, node.id, anode_tensor.size(), anode_output.size()))
            elif node.node_type == NodeType.OrNode:
                if 'structure' in cfg.search.space and str(node.id) in self.or_node_info:
                    weights = F.softmax(self.beta[str(node.id)], dim=-1)[0]
                    onode_tensor = NodeIdTensorDict[node.child_ids[0]] * weights[0]
                    for i, chid in enumerate(node.child_ids[1:]):
                        onode_tensor = onode_tensor + NodeIdTensorDict[chid] * weights[i+1]
                else:
                    onode_tensor = NodeIdTensorDict[node.child_ids[0]]
                    for chid in node.child_ids[1:]:
                        if self.node_set[chid].node_type != NodeType.OrNode:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            if arr.Width() == ch_arr.Width(): 
                                onode_tensor = onode_tensor + NodeIdTensorDict[chid] 
                                            
                if self.hasLateral[node.id]:
                    parent_ids1 = set(node.parent_ids) 
                    for chid in node.child_ids[1:]:
                        parent_ids2 = self.node_set[chid].parent_ids
                        if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) == 0:
                            onode_tensor = onode_tensor + NodeIdTensorDict[chid]

                    onode_tensor_all = onode_tensor
                    for chid in node.child_ids[1:]:
                        ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                        parent_ids2 = self.node_set[chid].parent_ids
                        if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) > 0:
                            onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid] 
                        elif self.node_set[chid].node_type == NodeType.TerminalNode and arr.Width() < ch_arr.Width():
                            ch_left = self.out_slices[arr.x1] - self.out_slices[ch_arr.x1]
                            ch_right = self.out_slices[arr.x2 + 1] - self.out_slices[ch_arr.x1]                                
                            onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid][:, ch_left:ch_right, :, :].contiguous()
                        
                    if 'operator' in cfg.search.space:
                        onode_output = getattr(self, 'weight'+str(node.id))(onode_tensor, onode_tensor_all, weights_lateral[NodeOpLateralCnt])
                    else:
                        onode_output = getattr(self, 'weight'+str(node.id))(onode_tensor, onode_tensor_all)
                    NodeOpLateralCnt += 1
                else:
                    if 'operator' in cfg.search.space:
                        onode_output = getattr(self, 'weight' + str(node.id))(onode_tensor, weights[NodeOpCnt]) 
                    else:
                        onode_output = getattr(self, 'weight' + str(node.id))(onode_tensor) 
                    NodeOpCnt += 1
                NodeIdTensorDict[node.id] = onode_output
                # print('{}-{} onode{} {} {}'.format(self.stage, self.unit, node.id, onode_tensor.size(), onode_output.size()))

        out = NodeIdTensorDict[self.aog.BFS[0]]
        return out


### AOGNet
class AOGNet(nn.Module):
    _arch_parameters = {}
    def __init__(self, num_classes):
        super(AOGNet, self).__init__()
        self._criterion = nn.CrossEntropyLoss().cuda()
        filter_list = cfg.aognet.filter_list
        self.aogs = self._create_aogs()
        
        if cfg.dataset == 'imagenet':            
            self.first_layer = ImageNetFirstLayer(3, filter_list[0])           
        elif cfg.dataset == 'cifar10' or cfg.dataset == 'cifar100':            
            self.first_layer = CIFARFirstLayer(3, filter_list[0])           
        else:
            raise NotImplementedError           

        self.aog_blocks = self._make_blocks()
        
        self.output = FinalLayer(filter_list[-1], num_classes)

        ## initialize
        for m in self.modules():            
            if isinstance(m, nn.Conv2d):
                if cfg.aognet.init_mode == 'xavier':
                    nn.init.xavier_normal_(m.weight)
                else:
                    n = m.kernel_size[0] * m.kernel_size[1] * (m.out_channels if cfg.aognet.init_mode == 'fan_out' else m.in_channels)
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()                        
            if isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1.)
                m.bias.data.zero_()

    def arch_parameters(self):
        return AOGNet._arch_parameters

    def get_architecture(self):
        arch_dict = {}
        for k, v in AOGNet._arch_parameters.items():
            if 'beta' in k:
                arch_dict[k] = {}
                for kk, vv in v.items():
                    weights = F.softmax(vv, dim=-1)[0].data.cpu().numpy().tolist()
                    arch_dict[k][kk] = weights
                continue
            arch_weights = []
            arch_params = v[0]
            mapping = v[1]
            genotype = ['' for _ in range(len(mapping[0]) + len(mapping[1]))]
            for i in range(2):
                weights = F.softmax(arch_params[i], dim=-1)
                weights_np = weights.data.cpu().numpy()
                arch_weights.append(weights_np)
                for j in range(weights_np.shape[0]):
                    if i == 0:
                        genotype[mapping[0][j]] = cfg.search.op_candidates[np.argmax(weights_np[j])]
                    else:
                        genotype[mapping[1][j]] = cfg.search.op_candidates_lateral[np.argmax(weights_np[j])]
            arch_dict[k] = (arch_weights, mapping, genotype)

        return arch_dict


    def _loss(self, input, target):
        outputs = self(input)
        return self._criterion(outputs, target) 
        
    def _create_aogs(self):
        aogs = []
        num_stages = len(cfg.aognet.filter_list) - 1
        for i in range(num_stages):
            grid_ht = 1
            grid_wd = int(cfg.aognet.dims[i])
            aogs.append(get_aog(grid_ht=grid_ht, grid_wd=grid_wd, max_split=cfg.aognet.max_split[i],
                                use_tnode_as_alpha_channel=False,
                                use_tnode_topdown_connection=True if cfg.aognet.extra_node_hierarchy[i] == 1 else False,
                                use_tnode_bottomup_connection_layerwise=True if cfg.aognet.extra_node_hierarchy[i] == 2 else False,
                                use_tnode_bottomup_connection_sequential=True if cfg.aognet.extra_node_hierarchy[i] == 3 else False,
                                use_node_lateral_connection=True if cfg.aognet.extra_node_hierarchy[i] == 4 else False,
                                use_tnode_bottomup_connection=True if cfg.aognet.extra_node_hierarchy[i] == 5 else False,
                                remove_single_child_or_node=cfg.aognet.turn_off_unit_or_node,
                                remove_symmetric_children_of_or_node=cfg.aognet.remove_symmetric_children_of_or_node[i],
                                max_children_kept_for_or=1000))

        return aogs

    def _make_blocks(self):
        blocks = nn.Sequential()
        num_stages = len(cfg.aognet.filter_list) - 1
        for i in range(num_stages):          
            # different units in a stage split the outchannels evenly 
            in_channels = cfg.aognet.filter_list[i]
            out_channels = cfg.aognet.filter_list[i+1]
            step_channels = (out_channels - in_channels) // cfg.aognet.units[i]
            aog = self.aogs[i]
            for j in range(cfg.aognet.units[i]):
                name_ = 'stage_{}_unit_{}'.format(i, j)
                dropRate = cfg.aognet.dropRate[i]                
                stride = cfg.aognet.stride[i] if j==0 else 1                
                outchannels = in_channels + step_channels if j < cfg.aognet.units[i]-1 else out_channels
                use_stride = stride
                if stride > 1 and cfg.aognet.when_downsample == 1:
                    blocks.add_module(name_ + 'conv0', nn.Conv2d(in_channels, in_channels, kernel_size=1, bias=_bias))
                    blocks.add_module(name_+ 'bn0', nn.BatchNorm2d(in_channels, eps=cfg.eps))
                    blocks.add_module(name_+ 'relu0', nn.ReLU(inplace=True))
                    blocks.add_module(name_ + 'avgpool', nn.AvgPool2d(kernel_size=stride, stride=stride))
                    use_stride = 1

                blocks.add_module(name_, AOGBlock(i, j, aog, in_channels, outchannels, dropRate, use_stride))

                blocks.add_module(name_+'bn1', nn.BatchNorm2d(outchannels, eps=cfg.eps))
                blocks.add_module(name_+'relu1', nn.ReLU(inplace=True))
                
                in_channels = outchannels

        return blocks

    def forward(self, x):
        y = self.first_layer(x)
        y = self.aog_blocks(y)        
        y = self.output(y)
        return y


def aognet_search(**kwargs):
    '''
    Construct an AOGNet model
    '''
    return AOGNet(**kwargs)
