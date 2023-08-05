import os.path
import random
import torch
from PIL import Image
import torch.utils.data as data
import torchvision.transforms as transforms

from .image_folder import make_dataset

class CityscapesDataset(data.Dataset):
    r'''

    CityscapesDataset(root, phase, loadSize, fineSize, no_flip=False, gray=False, direction='BtoA')

    '''

    def __init__(self, root, phase, loadSize, fineSize, no_flip=False, gray=False, direction='BtoA'):
        super(BaseDataset, self).__init__()

        self.root = root
        self.dir_AB = os.path.join(dataroot, phase)
        self.loadSize = loadSize
        self.fineSize = fineSize
        self.no_flip = no_flip
        self.direction = direction
        self.AB_paths = sorted(make_dataset(self.dir_AB))
        assert(opt.resize_or_crop == 'resize_and_crop')

        
    def __getitem__(self, index):
        AB_path = self.AB_paths[index]
        AB = Image.open(AB_path).convert('RGB')
        w, h = AB.size
        w2 = int(w / 2)
        A = AB.crop((0, 0, w2, h)).resize((self.loadSize, self.loadSize), Image.BICUBIC)
        B = AB.crop((w2, 0, w, h)).resize((self.loadSize, self.loadSize), Image.BICUBIC)
        A = transforms.ToTensor()(A)
        B = transforms.ToTensor()(B)
        w_offset = random.randint(0, max(0, self.loadSize - self.fineSize - 1))
        h_offset = random.randint(0, max(0, self.loadSize - self.fineSize - 1))

        A = A[:, h_offset:h_offset + self.opt.fineSize, w_offset:w_offset + self.opt.fineSize]
        B = B[:, h_offset:h_offset + self.opt.fineSize, w_offset:w_offset + self.opt.fineSize]

        A = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(A)
        B = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(B)

        if (not self.opt.no_flip) and random.random() < 0.5:
            idx = [i for i in range(A.size(2) - 1, -1, -1)]
            idx = torch.LongTensor(idx)
            A = A.index_select(2, idx)
            B = B.index_select(2, idx)

        if self.gray :  # RGB to gray
            tmp = A[0, ...] * 0.299 + A[1, ...] * 0.587 + A[2, ...] * 0.114
            A = tmp.unsqueeze(0)

        if self.gray:  # RGB to gray
            tmp = B[0, ...] * 0.299 + B[1, ...] * 0.587 + B[2, ...] * 0.114
            B = tmp.unsqueeze(0)

        return {'A': A, 'B': B, 'A_paths': AB_path, 'B_paths': AB_path}

    def __len__(self):
        return len(self.AB_paths)

    def name(self):
        return 'CityscapesDataset'
