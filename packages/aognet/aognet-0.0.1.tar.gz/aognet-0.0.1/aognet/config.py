from yacs.config import CfgNode as CN

_C = CN()
_C.model = 'aognet'
_C.train_batch_size = 128
_C.val_batch_size = 100
_C.num_epoch = 300
_C.dataset = 'cifar10'
_C.imagenet_head7x7 = True
_C.imagenet_extra_aug = False
_C.optimizer = 'SGD'
_C.gamma = 0.1 # decay_rate
_C.use_cosine_lr = False # cosine lr
_C.cosine_lr_min = 0
_C.lr = 0.1
_C.lr_schedule = [150, 225]
_C.momentum = 0.9
_C.wd = 5e-4
_C.nesterov = False
_C.dropout = 0.0
_C.activation_mode = 0 # 1: leakyReLU, 6: ReLU6 , other: ReLU
_C.classifier_dropout = 0.0
_C.use_cutout = False
_C.cutout_length = 16
_C.use_grad_clip = False
_C.grad_clip = 5.0
_C.drop_path_prob = 0.0
_C.curr_drop_prob = 0.0    # not a hyper-parameter
_C.eps = 1e-5
_C.auxiliary = 0.0
_C.zero_gamma = False

# resnet
_C.resnet = CN()
_C.resnet.depth = 110

# resnext
_C.resnext = CN()
_C.resnext.depth = 29
_C.resnext.cardinality = 8
_C.resnext.widen_factor = 4
_C.resnext.drop = 0.
_C.resnext.base_width = 4

# aognet
_C.aognet = CN()
_C.aognet.genotype = []
_C.aognet.filter_list = [16, 64, 128, 256]
_C.aognet.units = [1, 1, 1]
_C.aognet.dims = [4, 4, 4]
_C.aognet.max_split = [2, 2, 2] # must >= 2
_C.aognet.terminal_node_as_alpha_channel = [0, 0, 0]
_C.aognet.extra_node_hierarchy = [0, 0, 0]  # 0: none, 1: tnode topdown, 2: tnode bottomup layerwise, 3: tnode bottomup sequential, 4: or node lateral, 5: tnode bottomup
_C.aognet.turn_off_unit_or_node = False
_C.aognet.remove_symmetric_children_of_or_node = [0, 0, 0]
_C.aognet.mark_symmetric_syntatic_subgraph = False 
_C.aognet.or_node_max_num_children_kept = 100
#_C.aognet.terminal_node_operator = ['ResNet_Bottleneck', 'ResNet_Bottleneck', 'ResNet_Bottleneck']
#_C.aognet.and_node_operator = ['ResNet_Bottleneck', 'ResNet_Bottleneck', 'ResNet_Bottleneck'] 
#_C.aognet.or_node_operator = ['ResNet_Bottleneck', 'ResNet_Bottleneck', 'ResNet_Bottleneck'] 
_C.aognet.node_op = 'residual_bottleneck'
_C.aognet.node_op_lateral = 'residual_bottleneck_lateral'
_C.aognet.extra_bn = False
_C.aognet.handle_dbl_cnt = False
_C.aognet.use_group_conv = False
_C.aognet.dropRate = [0.0, 0.0, 0.0]
_C.aognet.stride = [1, 2, 2]
_C.aognet.building_block = 'AOGBlock'
_C.aognet.fix_bottleneck_channels_in_a_stage = False
_C.aognet.bottleneck_ratio = 0.25
_C.aognet.cardinality = 8
_C.aognet.base_width = 4
_C.aognet.terminal_node_no_slice = [0, 0, 0]
_C.aognet.terminal_node_dilation = False
_C.aognet.first_layer_version = 0 #0: default, 1: add BatchNorm, 2: BN+ReLU, 3: PreResNet_Bottleneck, 4: BN+ResNet_Bottleneck, 5: BN+ReLU+ResNet_Bottleneck
_C.aognet.extra_BN_ReLU = 0 # 0: a BN+ReLU in the final layer, 
                             # 1: added to the output of each AOGBlock, 
                             # 2: added to all or-nodes with multiple children
                             # 3: added to all and-nodes with multiple children
                             # 4: added to all t-nodes with multiple children
                             # 5: added to all nodes with multiple children
                             # TODO: add BN only??
_C.aognet.init_mode = 'fan_out'
_C.aognet.dropout_in_the_last_block = 0 # 0: follow _C.dropout, 
                                         # 1: only apply _C.droput in the last block, 
                                         # 2: only apply for or-nodes in the last block 
                                         # 3: only for root or-nodes in the last block 
                                         # 4: only for non-terminal nodes in the last block 
                                         # 5: only for t-nodes in the last block 
_C.aognet.when_downsample = 0 # 0: at T-nodes (less memory), 1: before a aogblock
_C.aognet.downsampler = 0 # 0: default by stride, 1: maxpool with stride, 2: avgpool with stride
# _C.aognet.spatial = [0, 0, 0] # (grid_ht, grid_wd, channels) if the first two > 0, use it to replace avgpool
_C.aognet.aggregation_stage = -1 # -1: default, the last stage, 

# search
_C.search = CN()
_C.search.arch_learning_rate = 3e-4
_C.search.arch_weight_decay = 1e-3
_C.search.train_portion = 0.5
_C.search.unrolled = False
_C.search.op_candidates = ['residual_bottleneck', 'skip'] # residual_bottoleneck, skip, avg_pool_3x3, max_pool_3x3, sep_conv_3x3, sep_conv_5x5, sep_conv_7x7, dil_conv_3x3, dil_conv_5x5, conv_7x1_1x7
_C.search.op_candidates_lateral = ['residual_bottleneck_lateral', 'add']
_C.search.mode = 'individual' # choices: individual, shared, normal-reduce
_C.search.space = ['operator', 'structure'] # 'operator', 'structure'

cfg = _C
