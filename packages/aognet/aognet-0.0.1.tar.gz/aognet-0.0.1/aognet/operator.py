from __future__ import absolute_import
from __future__ import division
from __future__ import print_function  # force to use print as function print(args)
from __future__ import unicode_literals

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from .config import cfg         # new cfg


_bias = False
_inplace = True

########################################### Op ################################################

OPS = {
        'residual_bottleneck': lambda cin, cout, stride, dp, group, extra_bn: NodeOp_1(cin, cout, stride, dp, group, extra_bn),
        'residual_bottleneck_lateral': lambda cin, cout, stride, dp, group, extra_bn: NodeOp_Lateral(cin, cout, stride, dp, group, extra_bn),
        'skip': lambda cin, cout, stride, dp, group: Skip(cin, cout, stride),
        'add': lambda cin, cout, stride, dp, group: Add(),
        'avg_pool_3x3' : lambda cin, cout, stride, dp, group: nn.AvgPool2d(3, stride=stride, padding=1, count_include_pad=False),
        'max_pool_3x3' : lambda cin, cout, stride, dp, group: nn.MaxPool2d(3, stride=stride, padding=1),
        'sep_conv_3x3' : lambda cin, cout, stride, dp, group: SepConv(cin, cout, 3, stride, 1, dp),
        'residual_sep_conv_3x3' : lambda cin, cout, stride, dp, group: ResSepConv(cin, cout, 3, stride, 1, dp),
        'sep_conv_5x5' : lambda cin, cout, stride, dp, group: SepConv(cin, cout, 5, stride, 2, dp),
        'sep_conv_7x7' : lambda cin, cout, stride, dp, group: SepConv(cin, cout, 7, stride, 3, dp),
        'dil_conv_3x3' : lambda cin, cout, stride, dp, group: DilConv(cin, cout, 3, stride, 2, 2),
        'dil_conv_5x5' : lambda cin, cout, stride, dp, group: DilConv(cin, cout, 5, stride, 4, 2),
        'conv_7x1_1x7' : lambda cin, cout, stride, dp, group: nn.Sequential(
            nn.ReLU(inplace=_inplace),
            nn.Conv2d(cin, cout, (1,7), stride=(1, stride), padding=(0, 3), bias=_bias),
            nn.Conv2d(cout, cout, (7,1), stride=(stride, 1), padding=(3, 0), bias=_bias),
            nn.BatchNorm2d(cout)
            ),
}

OPS_NAME = {'residual_bottleneck': 'NodeOp',
            'residual_bottleneck_lateral': 'NodeOp_Lateral'}


### Activation 
class AC(nn.Module):
    def __init__(self, mode):
        super(AC, self).__init__()
        if mode == 1:
            self.ac = nn.LeakyReLU(inplace=_inplace)
        elif mode == 6:
            self.ac = nn.ReLU6(inplace=_inplace)
        else:
            self.ac = nn.ReLU(inplace=_inplace)

    def forward(self, x):
        x = self.ac(x)
        return x

    
### first layer 
class CIFARFirstLayer(nn.Module):    
    def __init__(self, inchannels, outchannels):
        super(CIFARFirstLayer, self).__init__()        
        self.conv1 = nn.Conv2d(inchannels, outchannels, kernel_size=3, padding=1, bias=_bias)        
        self.bn1 = nn.BatchNorm2d(outchannels, eps=cfg.eps)
        self.relu = AC(cfg.activation_mode)            
            
    def forward(self, x):
        y = self.conv1(x)        
        y = self.bn1(y)
        y = self.relu(y)
        return y


class ImageNetFirstLayer(nn.Module):
    def __init__(self, inchannels, outchannels):
        super(ImageNetFirstLayer, self).__init__()
        self.head7x7 = cfg.imagenet_head7x7
        if self.head7x7:
            self.conv1 = nn.Conv2d(inchannels, outchannels, 7, 2, 3, bias=_bias)
            self.bn1 = nn.BatchNorm2d(outchannels, eps=cfg.eps)
        else:
            plane = outchannels // 2
            self.conv1 = nn.Conv2d(inchannels, plane, 3, 2, 1, bias=_bias)
            self.bn1 = nn.BatchNorm2d(plane, eps=cfg.eps)
            self.conv2 = nn.Conv2d(plane, plane, 3, 1, 1, bias=_bias)
            self.bn2 = nn.BatchNorm2d(plane, eps=cfg.eps)
            self.conv3 = nn.Conv2d(plane, outchannels, 3, 1, 1, bias=_bias)
            self.bn3 = nn.BatchNorm2d(outchannels, eps=cfg.eps)

        self.relu1 = AC(cfg.activation_mode) #nn.ReLU(inplace=_inplace)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1) # kernel_size=2 ? the same as stride
                    
    def forward(self, x):
        y = self.conv1(x)
        y = self.bn1(y)
        if not self.head7x7:
            y = self.relu1(y)
            y = self.conv2(y)
            y = self.bn2(y)
            y = self.relu1(y)
            y = self.conv3(y)
            y = self.bn3(y)            
        y = self.relu1(y)
        y = self.maxpool1(y)
        return y

    
### final classifier layer
class FinalLayer(nn.Module):
    def __init__(self, inchannels, numclasses):
        super(FinalLayer, self).__init__()
        self.avgpool = nn.AdaptiveAvgPool2d(1)        
        self.fc = nn.Linear(inchannels, numclasses) 
        #self.fc = nn.Conv2d(inchannels, numclasses, kernel_size=1,
        #                    stride=1, padding=0, bias=True)
        if cfg.classifier_dropout:
            self.dp = nn.Dropout2d(p=cfg.classifier_dropout, inplace=_inplace)

    def forward(self, x):
        y = self.avgpool(x)
        # add dropout here only
        if cfg.classifier_dropout:
            y = self.dp(y)
        y = y.view(y.size(0), -1) 
        y = self.fc(y)       
        #y = y.view(y.size(0), -1) 
        return y


### SE https://github.com/moskomule/senet.pytorch/blob/master/se_module.py
class SELayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
                nn.Linear(channel, channel // reduction),
                nn.ReLU(inplace=True),
                nn.Linear(channel // reduction, channel),
                nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y

# TODO: debug and test it
class SimpleSELayer(nn.Module):
    def __init__(self, channel, eps=cfg.eps):
        super(SimpleSELayer, self).__init__()
        self.eps = eps
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        b, c, ht, wd = x.size()
        x = x.view(b, c, -1)
        mean = x.mean(-1, keepdim=True)
        var = x.var(-1, keepdim=True)

        x = x.view(b, -1)
        mean_all = x.mean(-1, keepdim=True)
        var_all = x.var(-1, keepdim=True)

        w0 = mean_all / (var_all.sqrt() + self.eps)
        w0 = w0.view(b, 1)
        
        w = mean / (var.sqrt() + self.eps) / w0
        w = self.sigmoid(w)
        x = x.view(b, c, ht, wd)
        w = w.view(b, c, 1, 1)
        return x * w


### node operator: ResNet Bottleneck
class Shortcut(object):
    def __init__(self, inchannels, outchannels, stride):
        self.shortcut = None
        if cfg.aognet.downsampler == 0:
            if inchannels != outchannels or stride > 1:
                self.shortcut = nn.Sequential()
                self.shortcut.add_module('shortcut_conv', nn.Conv2d(inchannels, outchannels, kernel_size=1, stride=stride, bias=_bias))
                self.shortcut.add_module('shortcut_bn',  nn.BatchNorm2d(outchannels, eps=cfg.eps))            
        else:            
            if stride > 1:
                self.shortcut = nn.Sequential()            
                if cfg.aognet.downsampler == 1:
                    self.shortcut.add_module('shortcut_maxpool', nn.MaxPool2d(stride, stride))  
                else:
                    self.shortcut.add_module('shortcut_avgpool', nn.AvgPool2d(stride, stride))
                self.shortcut.add_module('shortcut_conv',    nn.Conv2d(inchannels, outchannels, kernel_size=1, stride=1, bias=_bias))
                self.shortcut.add_module('shortcut_bn',      nn.BatchNorm2d(outchannels, eps=cfg.eps))
            elif inchannels != outchannels:
                self.shortcut = nn.Sequential()                        
                self.shortcut.add_module('shortcut_conv',    nn.Conv2d(inchannels, outchannels, kernel_size=1, stride=1, bias=_bias))
                self.shortcut.add_module('shortcut_bn',      nn.BatchNorm2d(outchannels, eps=cfg.eps))


class Op(nn.Module):
    """ Bottleneck Operator
    """

    def __init__(self, inchannels, outchannels, stride, dropRate, groups=1):
        super(Op, self).__init__()
        self.inchannels = inchannels
        self.outchannels = outchannels
        self.stride = stride
        self.plane = max(4, int(outchannels * cfg.aognet.bottleneck_ratio)) # need to ensure > cfg.aognet.base_width ?
        self.conv1 = nn.Conv2d(inchannels, self.plane, kernel_size=1, bias=_bias)
        self.bn1 = nn.BatchNorm2d(self.plane, eps=cfg.eps)
        
        self.groups = groups
        self.conv2 = nn.Conv2d(self.plane, self.plane, kernel_size=3, stride=stride, padding=1, bias=_bias,
                               groups = groups)
        self.bn2 = nn.BatchNorm2d(self.plane, eps=cfg.eps)
        self.conv3 = nn.Conv2d(self.plane, outchannels, kernel_size=1, bias=_bias)
        self.bn3 = nn.BatchNorm2d(outchannels, eps=cfg.eps)
        self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
        self.dropRate = dropRate
        if self.dropRate > 0: 
            self.dp1 = nn.Dropout2d(p=self.dropRate, inplace=_inplace)

    def forward(self, x):
        y = self.conv1(x)
        y = self.bn1(y)
        y = self.relu(y)

        y = self.conv2(y)
        y = self.bn2(y)
        #if self.dropRate > 0: # dropout here, better on cifar100 with small model
        #    y = self.dp1(y)
        y = self.relu(y) 

        y = self.conv3(y)
        y = self.bn3(y)
        if self.dropRate > 0: # better on imagenet 
            y = self.dp1(y)
        
        # add SE here ?
        # or, we can use a modified BN to play the role of SE

        
        
        return y


class NodeOp(nn.Module):
    """ Bottleneck w/ residual
    """
    def __init__(self, inchannels, outchannels, stride, dropRate, groups=1, extra_bn=False):
        super(NodeOp, self).__init__()
        self.op = Op(inchannels, outchannels, stride, dropRate, groups)
        self.shortcut = Shortcut(inchannels, outchannels, stride).shortcut
        self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
        self.extra_bn = extra_bn
        if self.extra_bn:
            self.bn = nn.BatchNorm2d(outchannels, eps=cfg.eps)

    def forward(self, x):
        res = x
        y = self.op(x)
        if cfg.curr_drop_prob:
            y = drop_path(y, cfg.curr_drop_prob)
        if self.shortcut is not None:
            res = self.shortcut(x)
        y += res  # may have issues when combined with inplace relu below
        y = self.relu(y) 
        if self.extra_bn: # or before the previous relu
            y = self.bn(y)
            y = self.relu(y)
            
        return y

class NodeOp_1(nn.Module):
    """ Bottleneck w/ residual
    """
    def __init__(self, inchannels, outchannels, stride, dropRate, groups=1, extra_bn=False):
        super(NodeOp_1, self).__init__()
        self.op = Op(inchannels, outchannels, stride, dropRate, groups)
        self.shortcut = Shortcut(inchannels, outchannels, stride).shortcut
        self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
        self.extra_bn = extra_bn
        if self.extra_bn:
            self.bn = nn.BatchNorm2d(outchannels, eps=cfg.eps)

    def forward(self, x_op, x_res=None):
        res = x_op if x_res is None else x_res
        y = self.op(x_op)
        if cfg.curr_drop_prob:
            y = drop_path(y, cfg.curr_drop_prob)
        if self.shortcut is not None:
            res = self.shortcut(res)
        y += res  # may have issues when combined with inplace relu below
        y = self.relu(y) 
        if self.extra_bn: # or before the previous relu
            y = self.bn(y)
            y = self.relu(y)
            
        return y

class Skip(nn.Module):
    def __init__(self, cin, cout, stride):
        super(Skip, self).__init__()
        self.cin = cin
        self.cout = cout
        self.stride = stride
        if cin != cout or stride > 1:
            self.conv = nn.Conv2d(cin, cout, kernel_size=1, stride=stride, bias=_bias)

    def forward(self, x):
        if self.cin != self.cout or self.stride > 1:
            x = self.conv(x)
        return x


class NodeOp_Lateral(nn.Module):
    def __init__(self, inchannels, outchannels, stride, dropRate, groups=1, extra_bn=False):
        super(NodeOp_Lateral, self).__init__()
        self.op = Op(inchannels, outchannels, stride, dropRate, groups)
        self.shortcut = Shortcut(inchannels, outchannels, stride).shortcut
        self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
        self.extra_bn = extra_bn
        if self.extra_bn:
            self.bn = nn.BatchNorm2d(outchannels, eps=cfg.eps)

    def forward(self, x, xall):
        res = x
        y = self.op(xall)
        if cfg.curr_drop_prob:
            y = drop_path(y, cfg.aognet.curr_drop_prob)
        if self.shortcut is not None:
            res = self.shortcut(x)
        y += res  # may have issues when combined with inplace relu below
        y = self.relu(y)
        if self.extra_bn:
            y = self.bn(y)
            y = self.relu(y)
        return y

class Add(nn.Module):
    def __init__(self):
        super(Add, self).__init__()

    def forward(self, x, y):
        return x + y


class DilConv(nn.Module):
    
  def __init__(self, C_in, C_out, kernel_size, stride, padding, dilation):
    super(DilConv, self).__init__()
    self.op = nn.Sequential(
      nn.Conv2d(C_in, C_in, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, groups=C_in, bias=_bias),
      nn.Conv2d(C_in, C_out, kernel_size=1, padding=0, bias=_bias),
      nn.BatchNorm2d(C_out),
      nn.ReLU(inplace=False),
      )

  def forward(self, x):
    return self.op(x)


class SepConv(nn.Module):
    
  def __init__(self, C_in, C_out, kernel_size, stride, padding, dropRate=0.1):
    super(SepConv, self).__init__()
    self.dropRate = dropRate
    self.op1 = nn.Sequential(
      nn.Conv2d(C_in, C_in, kernel_size=kernel_size, stride=stride, padding=padding, groups=C_in, bias=_bias),
      nn.Conv2d(C_in, C_in, kernel_size=1, padding=0, bias=_bias),
      nn.BatchNorm2d(C_in),
      )
    self.op2 = nn.Sequential(
      nn.Conv2d(C_in, C_in, kernel_size=kernel_size, stride=1, padding=padding, groups=C_in, bias=_bias),
      nn.Conv2d(C_in, C_out, kernel_size=1, padding=0, bias=_bias),
      nn.BatchNorm2d(C_out),
      )

    self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
    if self.dropRate > 0: 
      self.dp = nn.Dropout2d(p=self.dropRate, inplace=_inplace)

  def forward(self, x):
    y = self.op1(x)
    y = self.relu(y)
    y = self.op2(y)
    if self.dropRate > 0:
      y = self.dp(y)

    return y


class ResSepConv(nn.Module):
    """ Bottleneck w/ residual
    """
    def __init__(self, C_in, C_out, kernel_size, stride, padding, dropRate=0.1):
        super(ResSepConv, self).__init__()
        self.op = SepConv(C_in, C_out, kernel_size, stride, padding, dropRate)
        self.shortcut = Shortcut(C_in, C_out, stride).shortcut
        self.relu = AC(cfg.activation_mode) # nn.ReLU(inplace=_inplace)
        
    def forward(self, x):
        res = x
        y = self.op(x)
        if self.shortcut is not None:
            res = self.shortcut(x)
        y += res  # may have issues when combined with inplace relu below
        y = self.relu(y) 

        return y


def drop_path(x, drop_prob):
    if drop_prob > 0.:
        keep_prob = 1.-drop_prob
        mask = Variable(torch.cuda.FloatTensor(x.size(0), 1, 1, 1).bernoulli_(keep_prob))
        x.div_(keep_prob)
        x.mul_(mask)
    return x


class AuxHeadCIFAR(nn.Module):

  def __init__(self, C, num_classes):
    """assuming input size 8x8"""
    super(AuxHeadCIFAR, self).__init__()
    self.features = nn.Sequential(
      nn.BatchNorm2d(C),
      nn.ReLU(inplace=True),
      nn.AvgPool2d(5, stride=3, padding=0, count_include_pad=False), # image size = 2 x 2
      nn.Conv2d(C, 128, 1, bias=False),
      nn.BatchNorm2d(128),
      nn.ReLU(inplace=True),
      nn.Conv2d(128, 768, 2, bias=False),
      nn.BatchNorm2d(768),
      nn.ReLU(inplace=True)
    )
    self.classifier = nn.Linear(768, num_classes)

  def forward(self, x):
    x = self.features(x)
    x = self.classifier(x.view(x.size(0),-1))
    return x
