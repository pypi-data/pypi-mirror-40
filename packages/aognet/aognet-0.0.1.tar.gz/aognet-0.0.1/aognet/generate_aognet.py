import os
from .aognet import *

_fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'aog_blocks_gen.py')
indent = '    '

class AOGBlock_(AOGBlock):
    def __init__(self, stage, unit, aog, inchannels, outchannels, dropRate, stride,
            norm_layer=None, norm_kwargs={}, last_gamma=False):
        super(AOGBlock_, self).__init__(stage, unit, aog, inchannels, outchannels, dropRate, stride)

        with open(_fname, 'a+') as f:
            class_name = 'AOGBlock_{}_{}'.format(stage, unit)
            f.write('class {}(nn.Module):\n'.format(class_name))
            f.write(indent + 'def __init__(self, stage, unit, aog, inchannels, outchannels, dropRate, stride):\n')
            f.write(indent*2 + 'super({}, self).__init__()\n'.format(class_name))

            for d in self.define_summary:
                f.write(indent*2 + 'self.node_{} = {}({}, {}, {}, {}, {}, {})\n'.format(
                    d['id'], d['op'], d['cin'], d['cout'], d['stride'], dropRate, d['groups'], d['extra_bn']))
            if not cfg.aognet.extra_bn:
                f.write(indent*2 + 'self.bn = nn.BatchNorm2d({}, eps={})\n'.format(outchannels, cfg.eps))
                if cfg.auxiliary and self.is_last:
                    f.write(indent*2 + 'self.bn1 = nn.BatchNorm2d({}, eps={})\n'.format(outchannels, cfg.eps))
                f.write(indent*2 + 'self.relu = nn.ReLU(inplace=True)\n')

            f.write('\n')

        self.construct_foward()


    def construct_foward(self):
        with open(_fname, 'a+') as f:
            f.write(indent + 'def forward(self, x):\n')

            for id_ in self.DFS:
                node = self.node_set[id_]
                if node.node_type == NodeType.TerminalNode:
                    f.write(indent*2 + '# Terminal-Node {}\n'.format(node.id))
                    arr = self.primitive_set[node.rect_idx]
                    right, left = self.in_slices[arr.x2 + 1], self.in_slices[arr.x1]                       
                    if cfg.aognet.terminal_node_no_slice[self.stage]:
                        tnode_tensor = x
                        f.write(indent*2 + 'out_{} = self.node_{}(x)\n'.format(node.id, node.id))
                    else:
                        f.write(indent*2 + 'out_{} = x[:, {}:{}, :, :].contiguous()\n'.format(node.id, left, right))
                        f.write(indent*2 + 'out_{} = self.node_{}(out_{})\n'.format(node.id, node.id, node.id))

            # AND- and OR-nodes
            for id_ in self.DFS:
                node = self.node_set[id_]
                arr = self.primitive_set[node.rect_idx]
                if node.node_type == NodeType.AndNode:               
                    f.write(indent*2 + '# And-Node {}\n'.format(node.id))
                    child_tensor = []
                    for chid in node.child_ids:
                        ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                        if arr.Width() > ch_arr.Width():
                            child_tensor.append('out_{}'.format(chid) )                   
                    lst = child_tensor[0]
                    for cid in child_tensor[1:]:
                        lst += (', ' + cid)
                    f.write(indent*2 + 'out_{} = torch.cat([{}], 1)\n'.format(node.id, lst))

                    if self.hasLateral[node.id]:
                        parent_ids1 = set(node.parent_ids)                    
                        for chid in node.child_ids:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) == 0: # need to check if they share non-root ancestor(s)
                                f.write(indent*2 + 'out_{} = out_{} + out_{}\n'.format(node.id, node.id, chid))
                                
                        f.write(indent*2 + 'out_{}_all = out_{}\n'.format(node.id, node.id))
                        for chid in node.child_ids:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if arr.Width() == ch_arr.Width() and len(parent_ids1.intersection(parent_ids2)) > 0:
                                f.write(indent*2 + 'out_{}_all = out_{}_all + out_{}\n'.format(node.id, node.id, chid))
                                
                        f.write(indent*2 + 'out_{} = self.node_{}(out_{}, out_{}_all)\n'.format(node.id, node.id, node.id, node.id))
                    else:
                        f.write(indent*2 + 'out_{} = self.node_{}(out_{})\n'.format(node.id, node.id, node.id))

                elif node.node_type == NodeType.OrNode:
                    f.write(indent*2 + '# Or-Node {}\n'.format(node.id))
                    f.write(indent*2 + 'out_{} = out_{}\n'.format(node.id, node.child_ids[0]))
                    for chid in node.child_ids[1:]:
                        if self.node_set[chid].node_type != NodeType.OrNode:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            if arr.Width() == ch_arr.Width(): 
                                f.write(indent*2 + 'out_{} = out_{} + out_{}\n'.format(node.id, node.id, chid))
                                                
                    if self.hasLateral[node.id]:
                        parent_ids1 = set(node.parent_ids) 
                        for chid in node.child_ids[1:]:
                            parent_ids2 = self.node_set[chid].parent_ids
                            if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) == 0:
                                f.write(indent*2 + 'out_{} = out_{} + out_{}\n'.format(node.id, node.id, chid))

                        f.write(indent*2 + 'out_{}_all = out_{}\n'.format(node.id, node.id))
                        for chid in node.child_ids[1:]:
                            ch_arr = self.primitive_set[self.node_set[chid].rect_idx]
                            parent_ids2 = self.node_set[chid].parent_ids
                            if self.node_set[chid].node_type == NodeType.OrNode and len(parent_ids1.intersection(parent_ids2)) > 0:
                                f.write(indent*2 + 'out_{}_all = out_{}_all + out_{}\n'.format(node.id, node.id, chid))
                            elif self.node_set[chid].node_type == NodeType.TerminalNode and arr.Width() < ch_arr.Width():
                                raise NotImplementedError
                                ch_left = self.out_slices[arr.x1] - self.out_slices[ch_arr.x1]
                                ch_right = self.out_slices[arr.x2 + 1] - self.out_slices[ch_arr.x1]                                
                                onode_tensor_all = onode_tensor_all + NodeIdTensorDict[chid][:, ch_left:ch_right, :, :].contiguous()
                            
                        f.write(indent*2 + 'out_{} = self.node_{}(out_{}, out_{}_all)\n'.format(node.id, node.id, node.id, node.id))
                    else:
                        f.write(indent*2 + 'out_{} = self.node_{}(out_{})\n'.format(node.id, node.id, node.id))

            if not cfg.aognet.extra_bn:
                f.write(indent*2 + 'output = self.bn(out_{})\n'.format(self.aog.BFS[0]))
                f.write(indent*2 + 'output = self.relu(output)\n')
            if cfg.auxiliary and self.is_last:
                if not cfg.aognet.extra_bn:
                    f.write(indent*2 + 'output1 = self.bn1(out_{})\n'.format(self.largest_tnode_idx))
                    f.write(indent*2 + 'output1 = self.relu(output1)\n')
                    f.write(indent*2 + 'return output, output1\n')
                else:
                    f.write(indent*2 + 'return output, out_{}\n'.format(self.largest_tnode_idx))
                    
            f.write(indent*2 + 'return output\n')
            f.write('\n\n')





class AOGNet_(AOGNet):
    def __init__(self, num_classes):
        with open(_fname, 'w+') as f:
            f.write('from .operator import *\n')
            f.write('from cfgs.config import cfg\n')
            f.write('import torch\n')
            f.write('import torch.nn as nn\n')
            f.write('import torch.nn.functional as F\n')
            f.write('from torch.autograd import Variable\n')
            f.write('\n\n')

        super(AOGNet_, self).__init__(num_classes, block=AOGBlock_)

        with open(_fname, 'r') as f:
            print(f.read())
    

def generate_aognet(**kwargs):
    return AOGNet_(**kwargs)
