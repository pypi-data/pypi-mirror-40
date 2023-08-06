from __future__ import absolute_import
from __future__ import division
from __future__ import print_function  # force to use print as function print(args)
from __future__ import unicode_literals

import os
import numpy as np

from AOG import *
from AOG_Viz import *


def vis_aog(param):
    param.get_tag()
    g = AOGrid(param)
    g.Create()
    viz = AOG_Viz(g)

    file_name = viz.Visualize(os.path.dirname(os.path.abspath(__file__)), dir_back=True, layout_rank=True)
    save_name = file_name + param.tag
    os.system('dot -Tpdf {} -o {}.pdf'.format(file_name, save_name))


if __name__ == '__main__':
    param = Param(grid_ht=1, grid_wd=4, min_size=1, max_split=2, overlap_ratio=0.,
                  not_use_large_TerminalNode=False, turn_off_size_ratio_TerminalNode=0,
                  not_use_intermediate_TerminalNode=False,
                  use_root_TerminalNode=True, use_tnode_as_alpha_channel=0,
                  use_tnode_topdown_connection=False,
                  use_tnode_bottomup_connection=False,
                  use_tnode_bottomup_connection_layerwise=False,
                  use_tnode_bottomup_connection_sequential=False,
                  use_node_lateral_connection=False,
                  use_node_lateral_connection_1=False,
                  use_super_OrNode=False,
                  remove_single_child_or_node=False,
                  remove_symmetric_children_of_or_node=0,
                  mark_symmetric_syntatic_subgraph = False,
                  max_children_kept_for_or=1001)
    wds = [4]
    for wd in wds:
        param.grid_wd = wd
        for max_split in range(2, 3):
            for tnode_as_alpha in range(0, 1):
                for remove_symmetric_child_node in range(1, 3):
                    param.max_split = max_split
                    param.use_tnode_as_alpha_channel = tnode_as_alpha
                    param.remove_symmetric_children_of_or_node = remove_symmetric_child_node

                    param.use_tnode_topdown_connection = False
                    param.use_tnode_bottomup_connection = False
                    param.use_tnode_bottomup_connection_layerwise = False
                    param.use_tnode_bottomup_connection_sequential = False
                    param.use_node_lateral_connection = False
                    param.use_node_lateral_connection_1 = False
                    vis_aog(param)

                    continue
                
                    param.use_tnode_topdown_connection = True
                    param.use_tnode_bottomup_connection_layerwise = False
                    param.use_tnode_bottomup_connection_sequential = False
                    param.use_node_lateral_connection = False
                    vis_aog(param)

                    param.use_tnode_topdown_connection = False
                    param.use_tnode_bottomup_connection_layerwise = True
                    param.use_tnode_bottomup_connection_sequential = False
                    param.use_node_lateral_connection = False
                    vis_aog(param)

                    param.use_tnode_topdown_connection = False
                    param.use_tnode_bottomup_connection_layerwise = False
                    param.use_tnode_bottomup_connection_sequential = True
                    param.use_node_lateral_connection = False
                    vis_aog(param)

                    param.use_tnode_topdown_connection = False
                    param.use_tnode_bottomup_connection_layerwise = False
                    param.use_tnode_bottomup_connection_sequential = False
                    param.use_node_lateral_connection = True
                    vis_aog(param)





