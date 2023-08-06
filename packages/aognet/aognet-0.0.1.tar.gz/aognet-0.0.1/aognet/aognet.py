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
from .config import cfg         # new cfg
from .operator import *

import os
if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'aog_blocks_gen.py')):
    from .aog_blocks_gen import *

_bias = False
_inplace = True


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

        self.largest_tnode_idx = 0
        self.is_last = (stage == len(cfg.aognet.filter_list)-2 and unit == cfg.aognet.units[-1]-1)

        self.hasLateral = {}
        self.hasDblCnt = {}
        self.define_summary = []
        self.fwd_summary = []

        self.set_weights_attr()
        if not cfg.aognet.extra_bn:
            self.bn = nn.BatchNorm2d(outchannels, eps=cfg.eps)
            if cfg.auxiliary and self.is_last:
                self.bn1 = nn.BatchNorm2d(outchannels, eps=cfg.eps)
            self.relu = nn.ReLU(inplace=True)

    def calculate_slices(self, dim, channels):
        slices = [0] * dim
        for i in range(channels):
            slices[i % dim] += 1
        for d in range(1, dim):
            slices[d] += slices[d - 1]
        slices = [0] + slices
        return slices

    def create_op(self, node_id, cin, cout, stride, groups=1, extra_bn=False):
        if not cfg.aognet.genotype:
            if self.hasLateral[node_id]:
                setattr(self, 'weight' + str(node_id), OPS[cfg.aognet.node_op_lateral](cin, cout, stride, self.dropRate, groups, extra_bn))
                op = OPS_NAME[cfg.aognet.node_op_lateral]
            else:
                setattr(self, 'weight' + str(node_id), OPS[cfg.aognet.node_op](cin, cout, stride, self.dropRate, groups, extra_bn))
                op = OPS_NAME[cfg.aognet.node_op]

        elif cfg.search.mode == 'shared':
            setattr(self, 'weight' + str(node_id), OPS[cfg.aognet.genotype[0]['shared'][2][node_id]](cin, cout, stride, self.dropRate, groups, extra_bn))
            op = OPS_NAME[cfg.aognet.genotype[0]]

        self.define_summary.append({'id': node_id, 'op': op, 'cin': cin, 'cout': cout, 'stride': stride, 'groups': groups, 'extra_bn': extra_bn})

        # TODO: individual

              
    def set_weights_attr(self):                
        for id_ in self.DFS:
            node = self.node_set[id_]            
            arr = self.primitive_set[node.rect_idx]
            groups = arr.Width()   if cfg.aognet.use_group_conv else 1
            if node.node_type == NodeType.TerminalNode:                
                if arr.Width() == self.dim:
                    self.largest_tnode_idx = node.id
                self.hasLateral[node.id] = False
                self.hasDblCnt[node.id] = False 
                inplane = self.inchannels if cfg.aognet.terminal_node_no_slice[self.stage] else \
                            self.in_slices[arr.x2 + 1] - self.in_slices[arr.x1]
                outplane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]
                stride = self.stride
                self.create_op(node.id, inplane, outplane, stride) #, groups)

            elif node.node_type == NodeType.AndNode:                
                plane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]                
                stride = 1
                extra_bn = cfg.aognet.extra_bn

                self.hasLateral[node.id] = False
                self.hasDblCnt[node.id] = False 
                for chid in node.child_ids:
                    ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                    if arr.Width() == ch_arr.Width():
                        self.hasLateral[node.id] = True
                        break
                if cfg.aognet.handle_dbl_cnt:
                    for chid in node.child_ids:
                        if node.npaths / self.node_set[chid].npaths != 1.0:
                            self.hasDblCnt[node.id] = True
                            break
                    
                self.create_op(node.id, plane, plane, stride, groups, extra_bn)

            elif node.node_type == NodeType.OrNode:     
                assert self.node_set[node.child_ids[0]].node_type != NodeType.OrNode                                                           
                plane = self.out_slices[arr.x2 + 1] - self.out_slices[arr.x1]
                stride = 1
                extra_bn = (cfg.aognet.extra_bn and len(node.child_ids) > 1 and arr.Width() > 1)

                self.hasLateral[node.id] = False
                self.hasDblCnt[node.id] = False 
                for chid in node.child_ids:
                    ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                    if self.node_set[chid].node_type == NodeType.OrNode or arr.Width() < ch_arr.Width():                        
                        self.hasLateral[node.id] = True
                        break
                if cfg.aognet.handle_dbl_cnt:
                    for chid in node.child_ids:
                        if node.npaths / self.node_set[chid].npaths != 1.0:
                            self.hasDblCnt[node.id] = True
                            break
            
                self.create_op(node.id, plane, plane, stride, groups, extra_bn)


    def forward(self, x):       
        NodeIdTensorDict = {}

        # T-nodes, (hope they will be computed in parallel by pytorch)
        for id_ in self.DFS:
            node = self.node_set[id_]
            if node.node_type == NodeType.TerminalNode:
                arr = self.primitive_set[node.rect_idx]
                right, left = self.in_slices[arr.x2 + 1], self.in_slices[arr.x1]                       
                tnode_tensor = x if cfg.aognet.terminal_node_no_slice[self.stage] else x[:, left:right, :, :].contiguous()
                # assert tnode_tensor.requires_grad, 'slice needs to retain grad'
                tnode_output = getattr(self, 'weight' + str(node.id))(tnode_tensor)
                NodeIdTensorDict[node.id] = tnode_output
                ## debug
                #op = getattr(self,'weight'+str(node.id)).op
                #m, n, o = op.conv1, op.conv2, op.conv3
                #m_ = (torch.std(m.weight)/math.sqrt(2./m.out_channels)).data.cpu().numpy()
                #n_ = (torch.std(n.weight)/math.sqrt(2./(n.out_channels*9))).data.cpu().numpy()
                #o_ = (torch.std(o.weight)/math.sqrt(2./o.out_channels)).data.cpu().numpy()
                #print(self.stage, self.unit, node.id, arr.Width(), "T", m_, n_, o_)
                # print('{}-{}: tnode{} {} {}'.format(self.stage, self.unit, node.id, tnode_tensor.size(), tnode_output.size()))

        # AND- and OR-nodes
        for id_ in self.DFS:
            node = self.node_set[id_]
            arr = self.primitive_set[node.rect_idx]
            if node.node_type == NodeType.AndNode:
                if self.hasDblCnt[node.id]:
                    child_tensor = []
                    child_tensor_all = []
                    for chid in node.child_ids:
                        ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                        if arr.Width() > ch_arr.Width():
                            child_tensor.append(NodeIdTensorDict[chid] * (node.npaths / self.node_set[chid].npaths))  
                            child_tensor_all.append(NodeIdTensorDict[chid])         

                    anode_tensor = torch.cat(child_tensor, 1)
                    anode_tensor_all = torch.cat(child_tensor_all, 1)

                    if self.hasLateral[node.id]:
                        parent_ids1 = set(node.parent_ids)                    
                        for chid in node.child_ids:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) == 0: # need to check if they share non-root ancestor(s)
                                anode_tensor = anode_tensor + NodeIdTensorDict[chid] * (node.npaths / self.node_set[chid].npaths)
                                anode_tensor_all = anode_tensor_all + NodeIdTensorDict[chid]

                        #anode_tensor_all = anode_tensor
                        for chid in node.child_ids:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) > 0:
                                anode_tensor_all = anode_tensor_all +  NodeIdTensorDict[chid]
                        anode_output = getattr(self, 'weight'+str(node.id))(anode_tensor, anode_tensor_all)
                    else:
                        anode_output = getattr(self, 'weight' + str(node.id))(anode_tensor_all, anode_tensor)
                else:
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
                        anode_output = getattr(self, 'weight'+str(node.id))(anode_tensor, anode_tensor_all)
                    else:
                        anode_output = getattr(self, 'weight' + str(node.id))(anode_tensor)
                
                NodeIdTensorDict[node.id] = anode_output

                ## debug
                #op = getattr(self,'weight'+str(node.id)).op
                #m, n, o = op.conv1, op.conv2, op.conv3
                #m_ = (torch.std(m.weight)/math.sqrt(2./m.out_channels)).data.cpu().numpy()
                #n_ = (torch.std(n.weight)/math.sqrt(2./(n.out_channels*9))).data.cpu().numpy()
                #o_ = (torch.std(o.weight)/math.sqrt(2./o.out_channels)).data.cpu().numpy()
                #print(self.stage, self.unit, node.id, arr.Width(), "A", m_, n_, o_)
                # print('{}-{} anode{} {} {}'.format(self.stage, self.unit, node.id, anode_tensor.size(), anode_output.size()))
            elif node.node_type == NodeType.OrNode:
                if self.hasDblCnt[node.id]: 
                    onode_tensor = NodeIdTensorDict[node.child_ids[0]] * (node.npaths / self.node_set[node.child_ids[0]].npaths) 
                    onode_tensor_all = NodeIdTensorDict[node.child_ids[0]]
                    for chid in node.child_ids[1:]:
                        if self.node_set[chid].node_type != NodeType.OrNode:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            if arr.Width() == ch_arr.Width(): 
                                onode_tensor = onode_tensor + NodeIdTensorDict[chid] * (node.npaths / self.node_set[chid].npaths) 
                                onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid]

                    if self.hasLateral[node.id]:
                        parent_ids1 = set(node.parent_ids) 
                        for chid in node.child_ids[1:]:
                            parent_ids2 = self.node_set[chid].parent_ids
                            if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) == 0:
                                onode_tensor = onode_tensor + NodeIdTensorDict[chid] * (node.npaths / self.node_set[chid].npaths)
                                onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid]

                        #onode_tensor_all = onode_tensor
                        for chid in node.child_ids[1:]:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) > 0:
                                onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid] 
                            elif self.node_set[chid].node_type == NodeType.TerminalNode and arr.Width() < ch_arr.Width():
                                ch_left = self.out_slices[arr.x1] - self.out_slices[ch_arr.x1]
                                ch_right = self.out_slices[arr.x2 + 1] - self.out_slices[ch_arr.x1]                                
                                onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid][:, ch_left:ch_right, :, :].contiguous()

                        onode_output = getattr(self, 'weight'+str(node.id))(onode_tensor, onode_tensor_all)
                    else:
                        onode_output = getattr(self, 'weight' + str(node.id))(onode_tensor_all, onode_tensor)
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

                        onode_output = getattr(self, 'weight'+str(node.id))(onode_tensor, onode_tensor_all)
                    else:
                        onode_output = getattr(self, 'weight' + str(node.id))(onode_tensor)
                        
                NodeIdTensorDict[node.id] = onode_output

                ## debug
                #op = getattr(self,'weight'+str(node.id)).op
                #m, n, o = op.conv1, op.conv2, op.conv3
                #m_ = (torch.std(m.weight)/math.sqrt(2./m.out_channels)).data.cpu().numpy()
                #n_ = (torch.std(n.weight)/math.sqrt(2./(n.out_channels*9))).data.cpu().numpy()
                #o_ = (torch.std(o.weight)/math.sqrt(2./o.out_channels)).data.cpu().numpy()
                #print(self.stage, self.unit, node.id, arr.Width(), "O", m_, n_, o_)
                # print('{}-{} onode{} {} {}'.format(self.stage, self.unit, node.id, onode_tensor.size(), onode_output.size()))

        out = NodeIdTensorDict[self.aog.BFS[0]]
        if not cfg.aognet.extra_bn:
            out = self.bn(out)
            out = self.relu(out)

        if cfg.auxiliary and self.is_last:
            if not cfg.aognet.extra_bn:
                out1 = self.bn1(NodeIdTensorDict[self.largest_tnode_idx])
                out1 = self.relu(out1)
                return out, out1
            else:
                return out, NodeIdTensorDict[self.largest_tnode_idx]
        else:
            return out


### AOGNet
class AOGNet(nn.Module):
    def __init__(self, num_classes, block=AOGBlock, use_generated=False):
        super(AOGNet, self).__init__()
        filter_list = cfg.aognet.filter_list
        self.aogs = self._create_aogs()
        self.block = block
        self.use_generated = use_generated
        
        if cfg.dataset == 'imagenet':            
            self.first_layer = ImageNetFirstLayer(3, filter_list[0])           
        elif cfg.dataset == 'cifar10' or cfg.dataset == 'cifar100':            
            self.first_layer = CIFARFirstLayer(3, filter_list[0])           
        else:
            raise NotImplementedError           
        
        self.aog_blocks = self._make_blocks()
        
        self.output = FinalLayer(filter_list[-1], num_classes)

        if cfg.auxiliary:
            assert cfg.dataset in ['cifar10', 'cifar100'], "aux only support cifar"
            c_aux = cfg.aognet.filter_list[-1]
            self.aux_head = AuxHeadCIFAR(c_aux, num_classes)

        ## initialize
        for m in self.modules():            
            if isinstance(m, nn.Conv2d):
                if cfg.aognet.init_mode == 'xavier':
                    nn.init.xavier_normal_(m.weight)
                elif cfg.aognet.init_mode == 'fan_out':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif cfg.aognet.init_mode == 'fan_in':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.in_channels
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif cfg.aognet.init_mode == 'avg':
                    n = m.kernel_size[0] * m.kernel_size[1] * (m.in_channels + m.out_channels) / 2
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif cfg.aognet.init_mode == 'kaiming':
                    nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    m.bias.data.zero_()                        
            if isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        if cfg.zero_gamma:
            #print("zero_gamma")
            for m in self.modules():
                if isinstance(m, Op):
                    nn.init.constant_(m.bn3.weight, 0)
        
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
                                use_node_lateral_connection_1=True if cfg.aognet.extra_node_hierarchy[i] == 6 else False,
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
            dim = cfg.aognet.dims[i]
            assert in_channels % dim == 0 and out_channels % dim == 0
            step_channels = (out_channels - in_channels) // cfg.aognet.units[i]
            if step_channels % dim != 0:
                low = (step_channels // dim) * dim
                high = (step_channels // dim + 1) * dim
                if (step_channels-low) <= (high-step_channels):
                    step_channels = low
                else:
                    step_channels = high

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

                if self.use_generated:
                    blocks.add_module(name_, eval('AOGBlock_{}_{}'.format(i, j))(i, j, aog, in_channels, outchannels, dropRate, use_stride))
                else:
                    blocks.add_module(name_, self.block(i, j, aog, in_channels, outchannels, dropRate, use_stride))
                in_channels = outchannels

        return blocks

    def forward(self, x):
        y = self.first_layer(x)
        if cfg.auxiliary:
            y, y_aux = self.aog_blocks(y)        
            if cfg.auxiliary and self.training:
                y_aux = self.aux_head(y_aux)
            y = self.output(y)
            return y, y_aux
        else:
            y = self.aog_blocks(y)
            y = self.output(y)
            return y


def aognet(**kwargs):
    '''
    Construct an AOGNet model
    '''
    return AOGNet(**kwargs)
