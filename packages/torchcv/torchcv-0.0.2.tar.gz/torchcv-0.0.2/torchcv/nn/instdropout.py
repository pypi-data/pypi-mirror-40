import torch
import torch.nn as nn
from torch.autograd import Variable
from itertools import repeat
class instDropout(nn.Module):
    r"""
    in_channel, out_channel, n_hidden,
    condition image (128, 64)
    label_channel=3,label_out_channel=64, label_kernel=7, label_stride=2, label_padding=3,
    label_channel=64,label_out_channel=64, label_kernel=3, label_stride=2, label_padding=1,
    is_training=True
    condition_conv:
        # input condition: 128*64
        # conv out: 16*8 
        # channel 32
        # n_condition = 32x16x8
    
    batch_size = 2
    in_channel = 3
    out_channel = 16
    n_hidden = 512

    x = torch.randn([batch_size,in_channel,128,64])
    one_hot = torch.zeros([batch_size,in_channel,128,64])

    model = instDropout(in_channel, out_channel, 512)
    
    x = Variable(x)
    condition = Variable(one_hot)
   
    out = model(x,condition,True)

    m = nn.Conv2d(in_channel, out_channel, out_channel, 3, groups=out_channel, stride=1, padding=1)

    """

    def __init__(self, in_channel, out_channel, n_hidden=None, activation=nn.ReLU, use_conv_condition=False,  is_training=True):
        super(instDropout, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.num_features = in_channel * out_channel
        self.use_conv_condition = use_conv_condition
        self.is_training = is_training
        self.activation = activation

        #Affine transform parameters
        # self.gamma = nn.Parameter(torch.Tensor(num_features), requires_grad = True) 
        self.dropout_mask = nn.Parameter(torch.Tensor(1, self.num_features), requires_grad = True)   
        
        #Parameter initilization
        self.reset_parameters()
     
      
        if use_conv_condition:
            #MLP parameters
            self.n_condition = 128
            self.n_hidden = n_hidden
            # input condition: 128*64
            # conv out: 16*8 
            # channel 32
            # n_condition = 32x16x8
            self.conv_condition = nn.Sequential(
                nn.Conv2d(1,32,7,2,padding=3),
                nn.ReLU(inplace=True),
                nn.Conv2d(32,64,3,2,padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(64,32,3,2,padding=1),
                nn.ReLU(inplace=True),
                )
            self.n_condition = 32*16*8
            # MLP used to predict betas and gammas
            self.fc_condition = nn.Sequential(
                nn.Linear(self.n_condition, self.n_hidden),
                nn.ReLU(inplace=True),
                nn.Linear(self.n_hidden, self.num_features),
                nn.ReLU(inplace=True),
                )

        self.train = False
        self.inplace = False
        # Initialize weights using Xavier initialization and biases with constant value
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0.1)
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0.1)
        # print("Initialize")

    def reset_parameters(self):
        self.dropout_mask.data.uniform_()
        # self.dropout_mask.data.fill_(1)

    def _make_noise2d(self, input, condition):
        mask = self.activation(self.dropout_mask)
        if self.use_conv_condition:
            conv = self.conv_condition(condition)
            # print('conv', conv.size())
            conv = conv.view(condition.size(0),-1)
            # print('conv_condition', conv.size())
            condi_mask = self.fc_condition(conv)
            # print('fc_condi_mask', condi_mask.size())
            # print('self.num_features', self.num_features)
            #  256*256 = 65536
            mask = mask.expand(input.size())+ condi_mask
        else:
            mask = mask.expand(input.size(0), self.num_features)
            # print('mask', mask.size())
            # print(mask)
        
        return mask.view(input.size(0), self.num_features, 1, 1).expand(input.size(0) ,self.num_features, input.size(2),input.size(3))
        # return mask

    def forward(self, input, condition=None, train=False, inplace=False):

        print('instDropout', input.size(), condition.size())
        self.train = train
        self.inplace = inplace

        if self.inplace:
            output = input
        else:
            output = input.clone()

        self.noise = self._make_noise2d(input, condition)
        # print('noise.size', self.noise.size()) 
        # print(self.noise) 
        output = output.repeat(1, self.out_channel,1,1)
        # print('output', output.size())
        output.mul_(self.noise)

        return output 



if __name__ == '__main__':

    batch_size = 2
    x = torch.randn([batch_size,3,128,64])
    one_hot = torch.zeros([batch_size,3,64,32])

    model = instDropout(3,128,512)
    GModel = 'G_model.log'
    with open(GModel,'w') as file:
        file.write(model)
    # one_hot[0,0] = 1
    # one_hot[1,1] = 1
    # one_hot[2,1] = 1
    # one_hot[3,0] = 1
    
    x = Variable(x)
    # one_hot = Variable(one_hot.cuda())
    condition = Variable(one_hot)
   
    out = model(x,condition,True)
    print('ouput',out.size())

    m = nn.Conv2d(3*128, 128, 3, groups=128,stride=1, padding=1)
    
    print(m(out).size())
    print(model.state_dict)