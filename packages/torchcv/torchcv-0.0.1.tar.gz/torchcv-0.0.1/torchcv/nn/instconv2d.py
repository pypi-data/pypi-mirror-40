# coding=utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.modules import conv
from torch.nn.modules.utils import _pair


class InstConv2d(conv._ConvNd):

    r"""Applies a 2D convolution over an input signal composed of several input
    planes.

    In the simplest case, the output value of the layer with input size
    :math:`(N, C_{in}, H, W)` and output :math:`(N, C_{out}, H_{out}, W_{out})`
    can be precisely described as:

    .. math::

        \begin{array}{ll}
        out(N_i, C_{out_j})  = bias(C_{out_j})
                       + \sum_{{k}=0}^{C_{in}-1} weight(C_{out_j}, k)  \star input(N_i, k)
        \end{array}

    where :math:`\star` is the valid 2D `cross-correlation`_ operator,
    :math:`N` is a batch size, :math:`C` denotes a number of channels,
    :math:`H` is a height of input planes in pixels, and :math:`W` is
    width in pixels.

    | :attr:`stride` controls the stride for the cross-correlation, a single
      number or a tuple.
    | :attr:`padding` controls the amount of implicit zero-paddings on both
    |  sides for :attr:`padding` number of points for each dimension.
    | :attr:`dilation` controls the spacing between the kernel points; also
      known as the à trous algorithm. It is harder to describe, but this `link`_
      has a nice visualization of what :attr:`dilation` does.
    | :attr:`groups` controls the connections between inputs and outputs.
      `in_channels` and `out_channels` must both be divisible by `groups`.
    |       At groups=1, all inputs are convolved to all outputs.
    |       At groups=2, the operation becomes equivalent to having two conv
                 layers side by side, each seeing half the input channels,
                 and producing half the output channels, and both subsequently
                 concatenated.
            At groups=`in_channels`, each input channel is convolved with its
                 own set of filters (of size `out_channels // in_channels`).

    The parameters :attr:`kernel_size`, :attr:`stride`, :attr:`padding`, :attr:`dilation` can either be:

        - a single ``int`` -- in which case the same value is used for the height and width dimension
        - a ``tuple`` of two ints -- in which case, the first `int` is used for the height dimension,
          and the second `int` for the width dimension

    .. note::

         Depending of the size of your kernel, several (of the last)
         columns of the input might be lost, because it is a valid `cross-correlation`_,
         and not a full `cross-correlation`_.
         It is up to the user to add proper padding.

    .. note::

         The configuration when `groups == in_channels` and `out_channels = K * in_channels`
         where `K` is a positive integer is termed in literature as depthwise convolution.

         In other words, for an input of size :math:`(N, C_{in}, H_{in}, W_{in})`, if you want a
         depthwise convolution with a depthwise multiplier `K`,
         then you use the constructor arguments
         :math:`(in\_channels=C_{in}, out\_channels=C_{in} * K, ..., groups=C_{in})`

    Args:
        in_channels (int): Number of channels in the input image
        out_channels (int): Number of channels produced by the convolution
        kernel_size (int or tuple): Size of the convolving kernel
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1
        bias (bool, optional): If ``True``, adds a learnable bias to the output. Default: ``True``

    Shape:
        - Input: :math:`(N, C_{in}, H_{in}, W_{in})`
        - Output: :math:`(N, C_{out}, H_{out}, W_{out})` where
          :math:`H_{out} = floor((H_{in}  + 2 * padding[0] - dilation[0] * (kernel\_size[0] - 1) - 1) / stride[0] + 1)`
          :math:`W_{out} = floor((W_{in}  + 2 * padding[1] - dilation[1] * (kernel\_size[1] - 1) - 1) / stride[1] + 1)`

    Attributes:
        weight (Tensor): the learnable weights of the module of shape
                         (out_channels, in_channels,
                          kernel_size[0], kernel_size[1])
        bias (Tensor):   the learnable bias of the module of shape (out_channels)

        W(Tensor): Spectrally normalized weight

        u (Tensor): the right largest singular value of W.

    .. _cross-correlation:
        https://en.wikipedia.org/wiki/Cross-correlation

    .. _link:
        https://github.com/vdumoulin/conv_arithmetic/blob/master/README.md
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)
        super(InstConv2d, self).__init__(
            in_channels, out_channels, kernel_size, stride, padding, dilation,
            False, _pair(0), groups, bias)
        # self.register_buffer('dropout_mask', torch.Tensor(1, out_channels).normal_())
       
        self.activation = nn.ReLU()
        self.weight_size = (1, in_channels) + kernel_size

       

        self.out_channels = out_channels
        self.in_channels = in_channels
        self.num_features = in_channels * out_channels
        #Affine transform parameters
        self.dropout_mask = nn.Parameter(torch.Tensor(
            out_channels, in_channels))  
        # self.weight = Parameter(torch.Tensor(
        #     in_channels, out_channels // groups, *kernel_size)) 
        
        
        #Parameter dropout initilization
        self.set_dropout_parameters()

    def set_dropout_parameters(self):
        self.dropout_mask.data.uniform_()

    def _inst_dropout(self,input,channel_mask):
        # input size n c h w
        # print('input', input.size())
        # print(channel_mask)
        channel_mask = self.activation(channel_mask)
        channel_mask = channel_mask.view(1,self.in_channels,1,1).expand(input.size())
        # print('channel_mask', channel_mask.size())
        # print(channel_mask)
        # channel_mask = channel_mask
        # print(channel_mask)
        # print('channel_mask', channel_mask.size())
        # x = F.dropout(input)
        return input * channel_mask
        # return input.mul_(channel_mask)

    def forward(self, input):
        # print('weight',self.weight.data)
        # print('size',self.weight.size())
        # w_ = torch.split(self.weight.data,3,dim=0)
        # print('w_',w_[0].size())
        # print(self.weight.size())
        # print(self.weight[0].view(1,2,3,3).size())
        # print(input.size())
        x = self._inst_dropout(input, self.dropout_mask[0])
        channel_output = F.conv2d(x, self.weight[0].view(self.weight_size), self.bias[0].view(1), self.stride,
                        self.padding, self.dilation, self.groups)
        # self.weight.size(0): output channel size 
        # self.weight.size(0)
        # W_ = torch.split(self.weight,1)
        for i in range(1, self.out_channels):
            # print(i)
            x = self._inst_dropout(input, self.dropout_mask[i])
            channel_output = torch.cat([channel_output,F.conv2d(x, self.weight[i].view(self.weight_size), self.bias[i].view(1), self.stride,
                        self.padding, self.dilation, self.groups)], 1)

        # print('channel_output', channel_output.size())
        return channel_output
        # return F.conv2d(input, self.weight[0].view(1,2,3,3), self.bias[0].view(1), self.stride,
        #                 self.padding, self.dilation, self.groups)

class InstConv2dv2(conv._ConvNd):
    r'''
        _inst_dropout weight
    '''

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)
        super(InstConv2dv2, self).__init__(
            in_channels, out_channels, kernel_size, stride, padding, dilation,
            False, _pair(0), groups, bias)
        # self.register_buffer('dropout_mask', torch.Tensor(1, out_channels).normal_())
       
        self.activation = nn.ReLU(True)
        self.weight_size = (1, in_channels) + kernel_size

       

        self.out_channels = out_channels
        self.in_channels = in_channels
        self.num_features = in_channels * out_channels
        #Affine transform parameters
        self.dropout_mask = nn.Parameter(torch.Tensor(
            out_channels, in_channels))  
        # self.weight = Parameter(torch.Tensor(
        #     in_channels, out_channels // groups, *kernel_size)) 
        
        
        #Parameter dropout initilization
        self.set_dropout_parameters()

    def set_dropout_parameters(self):
        self.dropout_mask.data.fill_(1)

    def _inst_dropout(self,input,channel_mask):
        # input size n c h w
        # print('input', input.size())
        # print(channel_mask)
        channel_mask = self.activation(channel_mask)
        channel_mask = channel_mask.view(1,self.in_channels,1,1).expand(input.size())
        # print('channel_mask', channel_mask.size())
        # print(channel_mask)
        # channel_mask = channel_mask
        # print(channel_mask)
        # print('channel_mask', channel_mask.size())
        # x = F.dropout(input)
        return input * channel_mask
        # return input.mul_(channel_mask)

    def forward(self, input):
        # print('weight',self.weight.data)
        # print('size',self.weight.size())
        # w_ = torch.split(self.weight.data,3,dim=0)
        # print('w_',w_[0].size())
        # print(self.weight.size())
        # print(self.weight[0].view(1,2,3,3).size())
        # print(input.size())
        x = self._inst_dropout(input, self.dropout_mask[0])
        channel_output = F.conv2d(x, self.weight[0].view(self.weight_size), self.bias[0].view(1), self.stride,
                        self.padding, self.dilation, self.groups)
        # self.weight.size(0): output channel size 
        # self.weight.size(0)
        # W_ = torch.split(self.weight,1)
        for i in range(1, self.out_channels):
            # print(i)
            x = self._inst_dropout(input, self.dropout_mask[i])
            channel_output = torch.cat([channel_output,F.conv2d(x, self.weight[i].view(self.weight_size), self.bias[i].view(1), self.stride,
                        self.padding, self.dilation, self.groups)], 1)

        print('channel_output', channel_output.size())
        return channel_output
        # return F.conv2d(input, self.weight[0].view(1,2,3,3), self.bias[0].view(1), self.stride,
        #                 self.padding, self.dilation, self.groups)

class InstConv2dv3(nn.Module):
    r'''
        __setattr__ conv
    '''
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
        super(InstConv2dv3, self).__init__()
        if in_channels % groups != 0:
            raise ValueError('in_channels must be divisible by groups')
        if out_channels % groups != 0:
            raise ValueError('out_channels must be divisible by groups')
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.activation = nn.ReLU()
        self.weight = Parameter(torch.Tensor(
            out_channels, in_channels))

       
        
        for i in range(out_channels):
            self.__setattr__('conv_%d'%i,nn.Conv2d(in_channels, 1,kernel_size,stride,padding))
        
        # self.reset_parameters()

        # for m in self.modules():
        #     if isinstance(m, nn.Conv2d):
        #         nn.init.xavier_uniform_(m.weight)
        #         nn.init.constant_(m.bias, 0.1)

    def reset_parameters(self):
        self.weight.data.fill_(1)

    def _dropout(self,input,_weight):
        
        # print(_weight.size())
        _w0 = self.activation(_weight)
        _w1 = _w0.view(1,_weight.size(0),1,1).expand_as(input)
        return input.mul_(_w1)
        # return input*_weight

    def forward(self, input):
        ouput = self.__getattr__('conv_0')(input)
        for i in range(1, self.out_channels):
            x = self._dropout(input, self.weight[i])
            ouput = torch.cat((ouput,self.__getattr__('conv_%d'%i)(x)),1)
        return ouput


class InstConv2dv5(conv._ConvNd):

    r"""Applies a 2D convolution over an input signal composed of several input
    planes.

    In the simplest case, the output value of the layer with input size
    :math:`(N, C_{in}, H, W)` and output :math:`(N, C_{out}, H_{out}, W_{out})`
    can be precisely described as:

    .. math::

        \begin{array}{ll}
        out(N_i, C_{out_j})  = bias(C_{out_j})
                       + \sum_{{k}=0}^{C_{in}-1} weight(C_{out_j}, k)  \star input(N_i, k)
        \end{array}

    where :math:`\star` is the valid 2D `cross-correlation`_ operator,
    :math:`N` is a batch size, :math:`C` denotes a number of channels,
    :math:`H` is a height of input planes in pixels, and :math:`W` is
    width in pixels.

    | :attr:`stride` controls the stride for the cross-correlation, a single
      number or a tuple.
    | :attr:`padding` controls the amount of implicit zero-paddings on both
    |  sides for :attr:`padding` number of points for each dimension.
    | :attr:`dilation` controls the spacing between the kernel points; also
      known as the à trous algorithm. It is harder to describe, but this `link`_
      has a nice visualization of what :attr:`dilation` does.
    | :attr:`groups` controls the connections between inputs and outputs.
      `in_channels` and `out_channels` must both be divisible by `groups`.
    |       At groups=1, all inputs are convolved to all outputs.
    |       At groups=2, the operation becomes equivalent to having two conv
                 layers side by side, each seeing half the input channels,
                 and producing half the output channels, and both subsequently
                 concatenated.
            At groups=`in_channels`, each input channel is convolved with its
                 own set of filters (of size `out_channels // in_channels`).

    The parameters :attr:`kernel_size`, :attr:`stride`, :attr:`padding`, :attr:`dilation` can either be:

        - a single ``int`` -- in which case the same value is used for the height and width dimension
        - a ``tuple`` of two ints -- in which case, the first `int` is used for the height dimension,
          and the second `int` for the width dimension

    .. note::

         Depending of the size of your kernel, several (of the last)
         columns of the input might be lost, because it is a valid `cross-correlation`_,
         and not a full `cross-correlation`_.
         It is up to the user to add proper padding.

    .. note::

         The configuration when `groups == in_channels` and `out_channels = K * in_channels`
         where `K` is a positive integer is termed in literature as depthwise convolution.

         In other words, for an input of size :math:`(N, C_{in}, H_{in}, W_{in})`, if you want a
         depthwise convolution with a depthwise multiplier `K`,
         then you use the constructor arguments
         :math:`(in\_channels=C_{in}, out\_channels=C_{in} * K, ..., groups=C_{in})`

    Args:
        in_channels (int): Number of channels in the input image
        out_channels (int): Number of channels produced by the convolution
        kernel_size (int or tuple): Size of the convolving kernel
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1
        bias (bool, optional): If ``True``, adds a learnable bias to the output. Default: ``True``

    Shape:
        - Input: :math:`(N, C_{in}, H_{in}, W_{in})`
        - Output: :math:`(N, C_{out}, H_{out}, W_{out})` where
          :math:`H_{out} = floor((H_{in}  + 2 * padding[0] - dilation[0] * (kernel\_size[0] - 1) - 1) / stride[0] + 1)`
          :math:`W_{out} = floor((W_{in}  + 2 * padding[1] - dilation[1] * (kernel\_size[1] - 1) - 1) / stride[1] + 1)`

    Attributes:
        weight (Tensor): the learnable weights of the module of shape
                         (out_channels, in_channels, kernel_size[0], kernel_size[1])
        bias (Tensor):   the learnable bias of the module of shape (out_channels)

        W(Tensor): Spectrally normalized weight

        u (Tensor): the right largest singular value of W.

    .. _cross-correlation:
        https://en.wikipedia.org/wiki/Cross-correlation

    .. _link:
        https://github.com/vdumoulin/conv_arithmetic/blob/master/README.md
    """
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)
        super(InstConv2dv5, self).__init__(
            in_channels, out_channels, kernel_size, stride, padding, dilation,
            False, _pair(0), groups, bias)
        self.register_buffer('dropout_mask',nn.Parameter(torch.Tensor(
            out_channels, in_channels, 1, 1)))
        # self.dropout_mask = nn.Parameter(torch.Tensor(
        #     out_channels, in_channels, 1, 1))  
        # self.weight = Parameter(torch.Tensor(
        #     in_channels, out_channels // groups, *kernel_size)) 
        self.activation = nn.ReLU(True)
        
        #Parameter dropout initilization
        self.set_dropout_parameters()

    def set_dropout_parameters(self):
        self.dropout_mask.data.fill_(1)
    
    @property
    def W_(self):
        _m = self.activation(self.self.dropout_mask.data)
        w_mask = _m.expand_as(self.weight.data)
        return self.weight.data.mul_(w_mask)

    def forward(self, input):
        return F.conv2d(input, self.W_, self.bias, self.stride,
                        self.padding, self.dilation, self.groups)




class InstConv2dv4(conv._ConvNd):

    r"""Applies a 2D convolution over an input signal composed of several input
    planes.

    In the simplest case, the output value of the layer with input size
    :math:`(N, C_{in}, H, W)` and output :math:`(N, C_{out}, H_{out}, W_{out})`
    can be precisely described as:

    .. math::

        \begin{array}{ll}
        out(N_i, C_{out_j})  = bias(C_{out_j})
                       + \sum_{{k}=0}^{C_{in}-1} weight(C_{out_j}, k)  \star input(N_i, k)
        \end{array}

    where :math:`\star` is the valid 2D `cross-correlation`_ operator,
    :math:`N` is a batch size, :math:`C` denotes a number of channels,
    :math:`H` is a height of input planes in pixels, and :math:`W` is
    width in pixels.

    | :attr:`stride` controls the stride for the cross-correlation, a single
      number or a tuple.
    | :attr:`padding` controls the amount of implicit zero-paddings on both
    |  sides for :attr:`padding` number of points for each dimension.
    | :attr:`dilation` controls the spacing between the kernel points; also
      known as the à trous algorithm. It is harder to describe, but this `link`_
      has a nice visualization of what :attr:`dilation` does.
    | :attr:`groups` controls the connections between inputs and outputs.
      `in_channels` and `out_channels` must both be divisible by `groups`.
    |       At groups=1, all inputs are convolved to all outputs.
    |       At groups=2, the operation becomes equivalent to having two conv
                 layers side by side, each seeing half the input channels,
                 and producing half the output channels, and both subsequently
                 concatenated.
            At groups=`in_channels`, each input channel is convolved with its
                 own set of filters (of size `out_channels // in_channels`).

    The parameters :attr:`kernel_size`, :attr:`stride`, :attr:`padding`, :attr:`dilation` can either be:

        - a single ``int`` -- in which case the same value is used for the height and width dimension
        - a ``tuple`` of two ints -- in which case, the first `int` is used for the height dimension,
          and the second `int` for the width dimension

    .. note::

         Depending of the size of your kernel, several (of the last)
         columns of the input might be lost, because it is a valid `cross-correlation`_,
         and not a full `cross-correlation`_.
         It is up to the user to add proper padding.

    .. note::

         The configuration when `groups == in_channels` and `out_channels = K * in_channels`
         where `K` is a positive integer is termed in literature as depthwise convolution.

         In other words, for an input of size :math:`(N, C_{in}, H_{in}, W_{in})`, if you want a
         depthwise convolution with a depthwise multiplier `K`,
         then you use the constructor arguments
         :math:`(in\_channels=C_{in}, out\_channels=C_{in} * K, ..., groups=C_{in})`

    Args:
        in_channels (int): Number of channels in the input image
        out_channels (int): Number of channels produced by the convolution
        kernel_size (int or tuple): Size of the convolving kernel
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1
        bias (bool, optional): If ``True``, adds a learnable bias to the output. Default: ``True``

    Shape:
        - Input: :math:`(N, C_{in}, H_{in}, W_{in})`
        - Output: :math:`(N, C_{out}, H_{out}, W_{out})` where
          :math:`H_{out} = floor((H_{in}  + 2 * padding[0] - dilation[0] * (kernel\_size[0] - 1) - 1) / stride[0] + 1)`
          :math:`W_{out} = floor((W_{in}  + 2 * padding[1] - dilation[1] * (kernel\_size[1] - 1) - 1) / stride[1] + 1)`

    Attributes:
        weight (Tensor): the learnable weights of the module of shape
                         (out_channels, in_channels, kernel_size[0], kernel_size[1])
        bias (Tensor):   the learnable bias of the module of shape (out_channels)

        W(Tensor): Spectrally normalized weight

        u (Tensor): the right largest singular value of W.

    .. _cross-correlation:
        https://en.wikipedia.org/wiki/Cross-correlation

    .. _link:
        https://github.com/vdumoulin/conv_arithmetic/blob/master/README.md
    """
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)
        super(InstConv2dv4, self).__init__(
            in_channels, out_channels, kernel_size, stride, padding, dilation,
            False, _pair(0), groups, bias)
     
        self.dropout_mask = nn.Parameter(torch.Tensor(
            out_channels, in_channels,1,1))  
        self.size = out_channels* in_channels
        self.activation = nn.ReLU(True)
        
        #Parameter dropout initilization
        self.set_dropout_parameters()
        self.m = torch.Tensor(out_channels, in_channels,1,1).fill_(1).cuda(0)

    def set_dropout_parameters(self):
        self.dropout_mask.data.uniform_()
    def getinfo(self):
        # print(self.dropout_mask.data)
        idx = self.dropout_mask.data<=0
        idx = idx.resize_(self.size).type_as(self.m)
        # print(idx.size())
        # print(idx)
        m1 = self.m.clone().resize_(self.size)
        # print(m1.size())
        # print(m1)
        print('idx:',torch.dot(idx,m1),self.dropout_mask.data[0])
    @property
    def W_(self):    

        # print(self.dropout_mask.size())
        # print(self.m.size())
        y = self.dropout_mask * self.m

        # print(y.size())
        return  self.weight * self.activation(y).expand_as(self.weight)
        # return self.weight *  self.activation(self.dropout_mask.data).expand_as(self.weight)


    def forward(self, input):
        self.getinfo()
        return F.conv2d(input, self.W_, self.bias, self.stride,
                        self.padding, self.dilation, self.groups)

from torch.autograd import Variable
if __name__ == '__main__':

    model = InstConv2dv4(3,1,1,1,0,bias=False)
    # print(model)
    x = torch.ones([1,3,3,3])
    # x = torch.split(x,2,dim=1)
    # print('x',x,x[0].size())
    x = Variable(x)
   
    print(model(x))

    # m1 = torch.Tensor(2,2,1,1).fill_(2)
    # m2 = torch.Tensor(2,2,1,1).fill_(2)
    # print(m1.resize_(4))
    # print(torch.dot(m1.resize_(1),m2.resize_(1)))
