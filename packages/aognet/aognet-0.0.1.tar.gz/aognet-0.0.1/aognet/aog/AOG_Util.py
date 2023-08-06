from __future__ import absolute_import
from __future__ import division
from __future__ import print_function  # force to use print as function print(args)
from __future__ import unicode_literals

import numpy as np
from .AOG import *


class AOG_Util(object):

    def __init__(self, aog):
        self.aog = aog

    def get_matrix_form(self):
        """
        compact matrix form representing an AOG
        :return: matrix with each row [node.id, node.node_type, ornodeIdxInBFS, nb_children, child_ids]
        """

        node_set = self.aog.node_set

        max_num_children = 0
        for node in node_set:
            max_num_children = max(max_num_children, len(node.child_ids))

        matrix_form = np.zeros((len(node_set), 3 + max_num_children + 1), dtype=np.float32)

        for i, node in enumerate(node_set):
            matrix_form[i, 0] = node.id
            if node.node_type == NodeType.OrNode:
                matrix_form[i, 1] = 0
                matrix_form[i, 2] = self.aog.OrNodeIdxInBFS[node.id]
            elif node.node_type == NodeType.AndNode:
                matrix_form[i, 1] = 1
                matrix_form[i, 2] = -1
            else:
                matrix_form[i, 1] = 2
                matrix_form[i, 2] = -1

            matrix_form[i, 3] = len(node.child_ids)
            matrix_form[i, 4:4 + len(node.child_ids)] = node.child_ids

        return matrix_form

    def get_primitives(self):
        """
        :return:
        prim_type: the list of primitive types, a primitive type is defined by [height,width]
        prim_instance: the matrix of primitive instances, a primitive instance (a row) is defined by [x,y,height,width]
        prim_instance_with_type: the matrix of primitive instances with types, a row [x,y,height,width,idx_in_prim_type]
        """
        assert len(self.aog.node_set) > 0

        prim_type = []
        prim_instance = np.empty((0, 4), dtype=np.float32)
        prim_instance_with_type = np.empty((0, 5), dtype=np.float32)

        for id_ in self.aog.BFS:
            node = self.aog.node_set[id_]
            if node.node_type == NodeType.TerminalNode:
                rect = self.aog.primitive_set[node.rect_idx]
                prim_instance = np.vstack((prim_instance, np.array([rect.x1, rect.y1, rect.x2, rect.y2])))
                p = [rect.Height(), rect.Width()]
                if p not in prim_type:
                    prim_type.append(p)
                idx = prim_type.index(p)
                prim_instance_with_type = np.vstack((prim_instance_with_type,
                                                     np.array([rect.x1, rect.y1, rect.x2, rect.y2, idx])))

        return prim_type, prim_instance, prim_instance_with_type

    def get_configuration(self, det, pg, tnode_scores, offset, trans_std):
        wd = det[2] - det[0] + 1
        ht = det[3] - det[1] + 1
        cell_wd = wd / self.param.grid_wd
        cell_ht = ht / self.param.grid_ht

        # get the parse graph
        configuration = np.empty((0, 4), dtype=np.float32)
        colors = np.empty((0, 3), dtype=np.float32)
        tnode_score = []
        BFS = [self.BFS[0]]
        # print('---------------------------------------------------')
        while len(BFS):
            id = BFS.pop()
            node = self.node_set[id]
            if node.node_type == NodeType.OrNode:
                idx = self.OrNodeIdxInBFS[node.id]
                BFS.append(node.child_ids[int(pg[idx])])
            elif node.node_type == NodeType.AndNode:
                BFS += node.child_ids
            else:
                # if self.param.use_tnode_as_alpha_channel and len(node.parent_ids) == 1 and self.node_set[
                #     node.parent_ids[0]].node_type == NodeType.AndNode:
                #     continue
                rect = self.primitive_set[node.rect_idx]
                if offset is not None:
                    offset_ind = 0
                    if offset.shape[1] == len(self.part_type):
                        offset_ind = self.part_type.index([rect.Height(), rect.Width()])
                    elif offset.shape[1] == self.part_instance.shape[0]:
                        for node1 in self.node_set:
                            if node1.node_type == NodeType.TerminalNode:  # change to BFS after _part_instance is changed to BFS
                                if node1.id == node.id:
                                    break
                                offset_ind += 1
                    else:
                        raise ValueError("Wrong offsets")

                    # print(offset[0, offset_ind, 0], offset[1, offset_ind, 0])
                    offset_x = offset[0, offset_ind, 0] * trans_std * wd
                    offset_y = offset[1, offset_ind, 0] * trans_std * ht

                    tile_half_w = (rect.x2 - rect.x1 + 1) * cell_wd / 2.0
                    tile_half_h = (rect.y2 - rect.y1 + 1) * cell_ht / 2.0

                    # offset_x = min(max(offset_x, -tile_half_w), tile_half_w)
                    # offset_y = min(max(offset_y, -tile_half_h), tile_half_h)
                    #
                    # offset_x = 0
                    # offset_y = 0

                else:
                    offset_x = 0
                    offset_y = 0

                box = [det[0] + rect.x1 * cell_wd + offset_x,
                       det[1] + rect.y1 * cell_ht + offset_y,
                       det[0] + (rect.x2 + 1) * cell_wd + offset_x,
                       det[1] + (rect.y2 + 1) * cell_ht + offset_y]
                configuration = np.vstack((configuration, box))
                colors = np.vstack((colors, self.TNodeColors[node.id]))

                idx = self.TNodeIdxInBFS[node.id]
                score = tnode_scores[idx]
                tnode_score.append(score)

        return configuration, colors, tnode_score
