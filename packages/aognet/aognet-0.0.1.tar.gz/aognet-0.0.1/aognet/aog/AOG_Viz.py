from __future__ import absolute_import
from __future__ import division
from __future__ import print_function  # force to use print as function print(args)
from __future__ import unicode_literals

import os
import numpy as np
import math
import shutil
from collections import deque

from AOG import *


class AOG_Viz(object):

    def __init__(self, aog):
        self.aog = aog

    def PictureNodes(self, save_dir, input_bbox=None):
        assert os.path.exists(save_dir), 'not found {}'.format(save_dir)

        if input_bbox is None:
            input_bbox = np.array([self.aog.param.grid_ht, self.aog.param.grid_wd]) * 20

        bin_ht = min(40, max(20, int(round(input_bbox[0] / self.aog.param.grid_ht))))
        bin_wd = min(40, max(20, int(round(input_bbox[1] / self.aog.param.grid_wd))))

        line_wd = 3

        ht = self.aog.param.grid_ht * (bin_ht + line_wd) + line_wd
        wd = self.aog.param.grid_wd * (bin_wd + line_wd) + line_wd

        save_dir = os.path.join(save_dir, 'pictureAOG')
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)    
        os.makedirs(save_dir)

        templ = np.ones((ht, wd, 3), dtype=np.uint8) * 255
        xx = 0
        for x in range(self.aog.param.grid_wd + 1):
            templ[:, xx:(xx + line_wd), :] = 0
            xx += bin_wd + line_wd

        yy = 0
        for y in range(self.aog.param.grid_ht + 1):
            templ[yy:(yy + line_wd), :, :] = 0
            yy += bin_ht + line_wd

        filename = os.path.join(save_dir, 'grid.png')
        cv2.imwrite(filename, templ)

        # images for T-nodes and Or-nodes
        for node in self.aog.node_set:
            if node.node_type == NodeType.AndNode or node.rect_idx == -1:
                continue

            rect = self.aog.primitive_set[node.rect_idx]
            x1 = int(rect.x1 * (bin_wd + line_wd) + line_wd)
            y1 = int(rect.y1 * (bin_ht + line_wd) + line_wd)
            x2 = int((rect.x2 + 1) * (bin_wd + line_wd) + 1)
            y2 = int((rect.y2 + 1) * (bin_ht + line_wd) + 1)

            img = templ.copy()
            if node.node_type == NodeType.TerminalNode:
                diff = 120
            else:
                diff = 80
            img[y1:y2, x1:x2, :] -= diff

            filename = os.path.join(save_dir, '{:04d}.png'.format(node.id))
            cv2.imwrite(filename, img)

        # images for And-nodes
        margin = 1

        import colorsys
        HSV_tuples = [(x * 1.0 / self.aog.param.max_split, 0.5, 0.5) for x in range(self.aog.param.max_split)]
        RGB_colors = []
        for rgb in HSV_tuples:
            rgb = map(lambda x: int(x * 255 + 0.5), colorsys.hsv_to_rgb(*rgb))
            RGB_colors.append(list(rgb))

        for node in self.aog.node_set:
            if node.node_type != NodeType.AndNode: #or node.split_type==SplitType.Unknown:
                continue

            img = templ.copy()
            pixel_value_diff = 120 / len(node.child_ids)
            ch_rects = []

            for i, ch_id in enumerate(node.child_ids):
                if self.aog.node_set[ch_id].node_type != NodeType.OrNode:
                    continue

                ch = self.aog.node_set[ch_id]
                rect = self.aog.primitive_set[ch.rect_idx]

                x1 = int(rect.x1 * (bin_wd + line_wd) + line_wd)
                y1 = int(rect.y1 * (bin_ht + line_wd) + line_wd)
                x2 = int((rect.x2 + 1) * (bin_wd + line_wd) + 1)
                y2 = int((rect.y2 + 1) * (bin_ht + line_wd) + 1)

                tx1 = min(x1 + margin, wd - 1)
                ty1 = min(y1 + margin, ht - 1)
                tx2 = max(x2 - margin, 0)
                ty2 = max(y2 - margin, 0)

                ch_rects.append([x1, y1, x2, y2])

                img[ty1:ty2, tx1:tx2, :] -= int(100 + pixel_value_diff * i)

                img[y1:y2, x1, :] = RGB_colors[i]
                img[y1:y2, x2, :] = RGB_colors[i]
                img[y1, x1:x2, :] = RGB_colors[i]
                img[y2, x2:x2, :] = RGB_colors[i]

            # overlap
            i = j = 0
            for ch1 in range(len(node.child_ids)):
                if self.aog.node_set[node.child_ids[ch1]].node_type != NodeType.OrNode:
                    continue
                for ch2 in range(i + 1, len(node.child_ids)):
                    if self.aog.node_set[node.child_ids[ch2]].node_type != NodeType.OrNode:
                        continue
                    ox1 = max(ch_rects[i][0], ch_rects[j][0])
                    oy1 = max(ch_rects[i][1], ch_rects[j][1])
                    ox2 = min(ch_rects[i][2], ch_rects[j][2])
                    oy2 = min(ch_rects[i][3], ch_rects[j][3])

                    if ox1 <= ox2 and oy1 <= oy2:
                        tx1 = min(ox1 + margin, wd - 1)
                        ty1 = min(oy1 + margin, ht - 1)
                        tx2 = max(ox2 - margin, 0)
                        ty2 = max(oy2 - margin, 0)

                        img[ty1:ty2, tx1:tx2, :] -= 200
                    j += 1
                i += 1

            # # first child
            # ch = self.node_set[node.child_ids[0]]
            # rect = self.primitive_set[ch.rect_idx]
            #
            # x1 = int(rect.x1 * (bin_wd + line_wd) + line_wd)
            # y1 = int(rect.y1 * (bin_ht + line_wd) + line_wd)
            # x2 = int((rect.x2 + 1) * (bin_wd + line_wd) + 1)
            # y2 = int((rect.y2 + 1) * (bin_ht + line_wd) + 1)
            #
            # tx1 = min(x1 + margin, wd - 1)
            # ty1 = min(y1 + margin, ht - 1)
            # tx2 = max(x2 - margin, 0)
            # ty2 = max(y2 - margin, 0)
            #
            #
            # img[ty1:ty2, tx1:tx2, :] -= 100
            #
            # # second child
            # ch = self.node_set[node.child_ids[1]]
            # rect = self.primitive_set[ch.rect_idx]
            #
            # xx1 = int(rect.x1 * (bin_wd + line_wd) + line_wd)
            # yy1 = int(rect.y1 * (bin_ht + line_wd) + line_wd)
            # xx2 = int((rect.x2 + 1) * (bin_wd + line_wd) + 1)
            # yy2 = int((rect.y2 + 1) * (bin_ht + line_wd) + 1)
            #
            # tx1 = min(xx1 + margin, wd - 1)
            # ty1 = min(yy1 + margin, ht - 1)
            # tx2 = max(xx2 - margin, 0)
            # ty2 = max(yy2 - margin, 0)
            #
            # img[ty1:ty2, tx1:tx2, :] -= 160
            #
            # # overlapping area
            # val = 200
            #
            # img[y1:y2, x1, :] = [0, val, val]
            # img[y1:y2, x2, :] = [0, val, val]
            # img[y1, x1:x2, :] = [0, val, val]
            # img[y2, x2:x2, :] = [0, val, val]
            #
            # img[yy1:yy2, xx1, :] = [val, val, 0]
            # img[yy1:yy2, xx2, :] = [val, val, 0]
            # img[yy1, xx1:xx2, :] = [val, val, 0]
            # img[yy2, xx1:xx2, :] = [val, val, 0]

            # ox1 = max(x1, xx1)
            # oy1 = max(y1, yy1)
            # ox2 = min(x2, xx2)
            # oy2 = min(y2, yy2)
            #
            # if ox1 <= ox2 and oy1 <= oy2:
            #     tx1 = min(ox1 + margin, wd - 1)
            #     ty1 = min(oy1 + margin, ht - 1)
            #     tx2 = max(ox2 - margin, 0)
            #     ty2 = max(oy2 - margin, 0)
            #
            #     img[ty1:ty2, tx1:tx2, :] -= val

            filename = os.path.join(save_dir, '{:04d}.png'.format(node.id))
            cv2.imwrite(filename, img)

        return save_dir

    def PictureWhichClassesVisitedNodes(self, save_dir, color_map):
        import matplotlib.pyplot as plt

        save_dir = os.path.join(save_dir, 'pictureWhichClassesVisitedNodes')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # # pie slice
        # N = len(color_map)
        # theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        # width = np.pi * 1.8 / N
        #
        # for i in range(len(self.node_set)):
        #     if len(self.node_set[i].which_classes_visited):
        #         # Compute pie slices
        #         radii = []
        #         colors = []
        #         labels = []
        #         for k in self.node_set[i].which_classes_visited.keys():
        #             radii.append(self.node_set[i].which_classes_visited[k])
        #             colors.append(color_map[k])
        #             labels.append(k)
        #
        #         for j in range(len(radii), N):
        #             radii.append(0)
        #             colors.append((1.0, 1.0, 1.0))
        #             labels.append('')
        #
        #         ax = plt.subplot(111, projection='polar')
        #         bars = ax.bar(theta, radii, width=width, bottom=0.0, tick_label=labels)
        #
        #         # Use custom colors and opacity
        #         j = 0
        #         for r, bar in zip(radii, bars):
        #             bar.set_facecolor(colors[j])
        #             bar.set_alpha(0.5)
        #             j += 1
        #
        #         # plt.axis('equal')
        #         plt.tight_layout()
        #         #plt.show()
        #         plt.savefig(os.path.join(save_dir, '{:4d}.png'.format(self.node_set[i].id)))
        #         plt.clf()

        width = 0.9
        ind = range(len(color_map))
        name2id = {}

        for i, k in enumerate(color_map.keys()):
            name2id[k] = int(i)

        for i in range(len(self.aog.node_set)):
            if len(self.aog.node_set[i].which_classes_visited):
                # Compute pie slices
                val = np.zeros((len(ind),), dtype=np.float)
                colors = [np.ones((3,), dtype=np.float) for _ in range(len(ind))]
                labels = ['' for _ in range(len(ind))]
                for j, k in enumerate(self.aog.node_set[i].which_classes_visited.keys()):
                    cur_ind = name2id[k]
                    val[cur_ind] = self.aog.node_set[i].which_classes_visited[k]
                    colors[cur_ind] = color_map[k]
                    labels[cur_ind] = k

                ax = plt.subplot(111)
                bars = ax.bar(ind, val, width=width, bottom=0.0)

                ax.set_xticks(ind)
                ax.set_xticklabels(labels, rotation=45)

                # Use custom colors and opacity
                for j, bar in enumerate(bars):
                    bar.set_facecolor(colors[j])
                    # bar.set_alpha(0.5)

                # plt.axis('equal')
                plt.tight_layout()
                # plt.show()
                plt.savefig(os.path.join(save_dir, '{:04d}.png'.format(self.aog.node_set[i].id)))
                plt.clf()

    def Visualize(self, save_dir, file_name=None, use_weighted_edge=False, dir_back=False, layout_rank=True,
                  vis_removed_symm=False, vis_dfs_bfs=True):
        if not os.path.exists(save_dir):
            print("Not found {}".format(save_dir))
            return

        if file_name is None:
            file_name = os.path.join(save_dir, "AOG.dot")

        node_img_dir = self.PictureNodes(save_dir)

        class_distr_img_dir = os.path.join(save_dir, 'pictureWhichClassesVisitedNodes')

        vis_nodes = []
        if vis_removed_symm:
            BFS = deque()
            BFS.append(self.aog.BFS[0])
            while len(BFS) > 0:
                id_ = BFS.popleft()
                vis_nodes.append(id_)
                node = self.aog.node_set[id_]
                if node.node_type == NodeType.OrNode:
                    for chid in node.child_ids:
                        chnode = self.aog.node_set[chid]
                        sz = self.aog.primitive_set[chnode.rect_idx].Width()
                        if chnode.node_type == NodeType.TerminalNode:
                            BFS.append(chid)
                        else:
                            if chnode.split_step1 <= sz//2:
                                BFS.append(chid)
                elif node.node_type == NodeType.AndNode:
                    for chid in node.child_ids:
                        BFS.append(chid)

        removed_color='yellow2'
        with open(file_name, "w") as f:
            f.write("digraph AOG {\n")
            for node in self.aog.node_set:
                # rect = self.aog.primitive_set[node.rect_idx]
                # node_tag = [rect_idx for rect_idx in range(rect.x1, rect.x2 + 1)]
                if node.on_off:
                    img_file = os.path.join(node_img_dir, '{:04d}.png'.format(node.id))
                    clss_distr_img_file = os.path.join(class_distr_img_dir, '{:04d}.png'.format(node.id))
                    if node.node_type == NodeType.OrNode:
                        node_color = removed_color if vis_removed_symm and node.id not in vis_nodes else 'green'
                        if node.rect_idx == -1:  # super-OR node
                            f.write(
                                'node{} [shape=ellipse, style=bold, color={}, label=\"\"]\n'.format(node.id, node_color))
                        else:
                            if node.id == 0 or node.id == self.aog.BFS[0]:
                                img_file = os.path.join(node_img_dir, 'grid.png')
                            if not os.path.exists(clss_distr_img_file) or len(node.child_ids) == 1:
                                if vis_dfs_bfs and node.id in self.aog.DFS:
                                    f.write(
                                        'node{} [shape=ellipse, style=bold, color={}, label=<'
                                        '<TABLE border=\"0\" cellborder=\"0\">'
                                        '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                        '<TR><TD PORT=\"f0\">{}, {}, {}, {}, {}</TD></TR>'
                                        '</TABLE>>]\n'.format(node.id, node_color, img_file, self.aog.DFS.index(node.id),
                                                              self.aog.BFS.index(node.id), node.npaths, node.is_symmetric, node.has_dbl_counting))
                                else:
                                        f.write(
                                        'node{} [shape=ellipse, style=bold, color={}, label=<'
                                        '<TABLE border=\"0\" cellborder=\"0\">'
                                        '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                        '</TABLE>>]\n'.format(node.id, node_color, img_file))
                            else:
                                f.write(
                                    'node{} [shape=ellipse, style=bold, color={}, label=<'
                                    '<TABLE border=\"0\" cellborder=\"0\">'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '</TABLE>>]\n'.format(
                                        node.id, node_color, img_file, clss_distr_img_file))

                    elif node.node_type == NodeType.AndNode:
                        node_color = removed_color if vis_removed_symm and node.id not in vis_nodes else 'blue'
                        if node.id == self.aog.node_set[self.aog.BFS[0]].id:
                            img_file = os.path.join(node_img_dir, 'grid.png')
                        if not os.path.exists(clss_distr_img_file):
                            if vis_dfs_bfs and node.id in self.aog.DFS:
                                f.write(
                                    'node{} [shape=ellipse, style=filled, color={}, label=<'
                                    '<TABLE border=\"0\" cellborder=\"0\">'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '<TR><TD PORT=\"f0\">{}, {}, {}, {}, {}</TD></TR>'
                                    '</TABLE>>]\n'.format(
                                        node.id, node_color, img_file, self.aog.DFS.index(node.id), self.aog.BFS.index(node.id), node.npaths, node.is_symmetric, node.has_dbl_counting))
                            else:
                                    f.write(
                                    'node{} [shape=ellipse, style=filled, color={}, label=<'
                                    '<TABLE border=\"0\" cellborder=\"0\">'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '</TABLE>>]\n'.format(
                                        node.id, node_color, img_file))
                        else:
                            f.write(
                                'node{} [shape=ellipse, style=filled, color={}, label=<'
                                '<TABLE border=\"0\" cellborder=\"0\">'
                                '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                '</TABLE>>]\n'.format(
                                    node.id, node_color, img_file, clss_distr_img_file))
                    elif node.node_type == NodeType.TerminalNode:
                        # if self.param.use_tnode_as_alpha_channel and len(node.parent_ids) == 1 and self.node_set[
                        #     node.parent_ids[0]].node_type == NodeType.AndNode:
                        #     continue
                        node_color = removed_color if vis_removed_symm and node.id not in vis_nodes else 'red'
                        if not os.path.exists(clss_distr_img_file):
                            if vis_dfs_bfs:
                                f.write(
                                    'node{} [shape=box, style=bold, color={}, label=<'
                                    '<TABLE border=\"0\" cellborder=\"0\">'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '<TR><TD PORT=\"f0\">{}, {}, {}, {}, {}</TD></TR>'
                                    '</TABLE>>]\n'.format(
                                        node.id, node_color, img_file, self.aog.DFS.index(node.id), self.aog.BFS.index(node.id), node.npaths, node.is_symmetric, node.has_dbl_counting))
                            else:
                                f.write(
                                    'node{} [shape=box, style=bold, color={}, label=<'
                                    '<TABLE border=\"0\" cellborder=\"0\">'
                                    '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                    '</TABLE>>]\n'.format(
                                        node.id, node_color, img_file))

                        else:
                            f.write(
                                'node{} [shape=box, style=bold, color={}, label=<'
                                '<TABLE border=\"0\" cellborder=\"0\">'
                                '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                '<TR><TD PORT=\"f0\"><IMG SRC=\"{}\"/></TD></TR>'
                                '</TABLE>>]\n'.format(
                                    node.id, node_color, img_file, clss_distr_img_file))
                    else:
                        print("Wrong node type")
                        raise RuntimeError

            if layout_rank:
                for ht in range(1, self.aog.param.grid_ht+1):
                    for wd in range(1, self.aog.param.grid_wd+1):
                        prim_type = [ht, wd]
                        ids = self.aog.find_node_ids_with_given_prim_type(prim_type, node_type=NodeType.TerminalNode)
                        if len(ids) > 1:
                            str_ids = ""
                            for id_ in ids:
                                str_ids += 'node{} '.format(id_)

                            f.write('{')
                            f.write('rank=same; {}'.format(str_ids))
                            f.write('}\n')

                        ids = self.aog.find_node_ids_with_given_prim_type(prim_type, node_type=NodeType.AndNode)
                        if len(ids) > 1:
                            str_ids = ""
                            for id_ in ids:
                                if self.aog.node_set[id_].split_type != SplitType.Unknown:
                                    str_ids += 'node{} '.format(id_)
                            f.write('{')
                            f.write('rank=same; {}'.format(str_ids))
                            f.write('}\n')

                        ids = self.aog.find_node_ids_with_given_prim_type(prim_type, node_type=NodeType.OrNode)
                        if len(ids) > 1:
                            str_ids = ""
                            for id_ in ids:
                                if self.aog.node_set[id_].rect_idx != -1:
                                    str_ids += 'node{} '.format(id_)
                            f.write('{')
                            f.write('rank=same; {}'.format(str_ids))
                            f.write('}\n')

            for node in self.aog.node_set:
                if node.on_off:

                    for c, i in enumerate(node.child_ids):
                        # if self.param.use_tnode_as_alpha_channel and node.node_type==NodeType.AndNode \
                        #         and self.node_set[i].node_type == NodeType.TerminalNode:
                        #     continue
                        isGray = vis_removed_symm and (node.id not in vis_nodes or i not in vis_nodes)
                        if node.node_type == NodeType.OrNode:
                            node_color = removed_color if isGray else 'green'
                            if self.aog.node_set[i].node_type == NodeType.OrNode:
                                f.write('edge [style=dashed, color=deeppink1]\n')
                            else:
                                f.write('edge [style=bold, color={}]\n'.format(node_color))
                        elif node.node_type == NodeType.AndNode:
                            node_color = removed_color if isGray else 'blue'
                            if self.aog.node_set[i].node_type != NodeType.OrNode:
                                f.write('edge [style=dashed, color=deeppink1]\n')
                            else:
                                f.write('edge [style=bold, color={}]\n'.format(node_color))
                        elif node.node_type == NodeType.TerminalNode:
                            node_color = removed_color if isGray else 'red'
                            f.write('edge [style=bold, color={}]\n'.format(node_color))
                        else:
                            print("Wrong node type")
                            raise RuntimeError


                        if self.aog.node_set[i].on_off:
                            if len(node.out_edge_visited_count) and node.out_edge_visited_count[
                                c] > 0 and use_weighted_edge:
                                penwidth = max(1, math.log10(node.out_edge_visited_count[c]))
                                f.write(
                                    'node{} -> node{} [penwidth={}, label=\"{:.4f}\"]\n'.format(node.id, i, penwidth,
                                                                                                node.out_edge_visited_count[
                                                                                                    c]))
                            else:
                                if dir_back:
                                    f.write('node{} -> node{} [dir=back] \n'.format(node.id, i))
                                else:
                                    f.write('node{} -> node{} \n'.format(node.id, i))

            f.write('}')

        # shutil.rmtree(node_img_dir)

        return file_name

    def PictureConfiguration(self, config, save_name, input_bbox=None):
        save_dir = os.path.split(save_name)[0]
        assert os.path.exists(save_dir), 'not found {}'.format(save_dir)

        if input_bbox is None:
            input_bbox = np.array([self.aog.param.grid_ht, self.aog.param.grid_wd]) * 20

        bin_ht = min(40, max(20, int(round(input_bbox[0] / self.aog.param.grid_ht))))
        bin_wd = min(40, max(20, int(round(input_bbox[1] / self.aog.param.grid_wd))))

        line_wd = 3

        ht = self.aog.param.grid_ht * (bin_ht + line_wd) + line_wd
        wd = self.aog.param.grid_wd * (bin_wd + line_wd) + line_wd

        templ = np.ones((ht, wd, 3), dtype=np.uint8) * 255
        xx = 0
        for x in range(self.aog.param.grid_wd + 1):
            templ[:, xx:(xx + line_wd), :] = 0
            xx += bin_wd + line_wd

        yy = 0
        for y in range(self.aog.param.grid_ht + 1):
            templ[yy:(yy + line_wd), :, :] = 0
            yy += bin_ht + line_wd

        for id in config[:]:
            if id == -1:
                break
            node = self.aog.node_set[id]
            assert node.node_type == NodeType.TerminalNode

            rect = self.aog.primitive_set[node.rect_idx]
            x1 = int(rect.x1 * (bin_wd + line_wd) + line_wd)
            y1 = int(rect.y1 * (bin_ht + line_wd) + line_wd)
            x2 = int((rect.x2 + 1) * (bin_wd + line_wd) + 1)
            y2 = int((rect.y2 + 1) * (bin_ht + line_wd) + 1)

            for c in range(3):
                templ[y1:y2, x1:x2, c] = int(min(255, self.aog.TNodeColors[id][c] * 255))

        cv2.imwrite(save_name, templ)
