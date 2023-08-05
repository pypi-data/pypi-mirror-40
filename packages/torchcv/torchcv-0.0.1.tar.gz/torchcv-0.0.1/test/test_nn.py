import torch
import cvlib.nn as cvnn
cvnn.ConditionalBatchNorm2d(10,20,30)

# gradient check
cvnn.SpectralNorm(torch.nn.Conv2d(1, 1, 4, 2, 1))
cvnn.ConvLSTM(input_channels=512, hidden_channels=[128, 64, 64, 32, 32], kernel_size=3, step=5, effective_step=[4])
# loss_fn = torch.nn.MSELoss()

# input = torch.randn(1, 512, 64, 32)
# target = torch.randn(1, 32, 64, 32)

# output = convlstm(input)
# output = output[0][0]
# res = torch.autograd.gradcheck(loss_fn, (output, target), raise_exception=True)
# print(res)