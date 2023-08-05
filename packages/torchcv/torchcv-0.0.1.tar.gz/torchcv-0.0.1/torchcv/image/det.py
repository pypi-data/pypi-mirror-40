import torch.utils.data as data

from PIL import Image

import os
import os.path
import sys


def has_file_allowed_extension(filename, extensions):
    """Checks if a file is an allowed extension.

    Args:
        filename (string): path to a file
        extensions (iterable of strings): extensions to consider (lowercase)

    Returns:
        bool: True if the filename ends with one of given extensions
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in extensions)


def is_image_file(filename):
    """Checks if a file is an allowed image extension.

    Args:
        filename (string): path to a file

    Returns:
        bool: True if the filename ends with a known image extension
    """
    return has_file_allowed_extension(filename, IMG_EXTENSIONS)


def make_dataset(dir, class_to_idx, extensions):
    images = []
    dir = os.path.expanduser(dir)
    for target in sorted(class_to_idx.keys()):
        d = os.path.join(dir, target)
        if not os.path.isdir(d):
            continue

        for root, _, fnames in sorted(os.walk(d)):
            for fname in sorted(fnames):
                if has_file_allowed_extension(fname, extensions):
                    path = os.path.join(root, fname)
                    item = (path, class_to_idx[target])
                    images.append(item)

    return images

def read_list(path_in):
    with open(path_in) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            line = [i.strip() for i in line.strip().split('\t')]
            line_len = len(line)
            if line_len < 3:
                print('lst should at least has three parts, but only has %s parts for %s' %(line_len, line))
                continue
            try:
                item = [int(line[0])] + [line[-1]] + [float(i) for i in line[1:-1]]
            except Exception as e:
                print('Parsing lst met error for %s, detail: %s' %(line, e))
                continue
            yield item

class DatasetDetection(data.Dataset):
    """A generic data loader where the samples are arranged in this way: ::

        root/class_x/xxx.ext
        root/class_x/xxy.ext
        root/class_x/xxz.ext

        root/class_y/123.ext
        root/class_y/nsdf3.ext
        root/class_y/asd932_.ext

    Args:
        root (string): Root directory path.
        loader (callable): A function to load a sample given its path.
        extensions (list[string]): A list of allowed extensions.
        transform (callable, optional): A function/transform that takes in
            a sample and returns a transformed version.
            E.g, ``transforms.RandomCrop`` for images.
        target_transform (callable, optional): A function/transform that takes
            in the target and transforms it.

     Attributes:
        classes (list): List of the class names.
        class_to_idx (dict): Dict with items (class_name, class_index).
        samples (list): List of (sample path, class_index) tuples
        targets (list): The class_index value for each image in the dataset
    """

    def __init__(self, root, loader, image_folders, lable_lst, extensions, phase=None, transform=None, target_transform=None):
        # classes, class_to_idx = self._find_classes(root)
        samples = read_list(os.path.join(root, lable_lst))
        # samples = make_dataset(root, class_to_idx, extensions)
        if len(samples) == 0:
            raise(RuntimeError("Found 0 files in subfolders of: " + root + "\n"
                               "Supported extensions are: " + ",".join(extensions)))

        self.root = root
        self.loader = loader
        self.extensions = extensions

        self.classes = classes
        self.class_to_idx = class_to_idx
        self.samples = samples
        # self.targets = [s[1] for s in samples]
        self.images_path = [s[1] for s in samples]

        self.transform = transform
        self.target_transform = target_transform

    def _check_valid_label(self, label):
        """Validate label and its shape."""
        if len(label.shape) != 2 or label.shape[1] < 5:
            msg = "Label with shape (1+, 5+) required, %s received." % str(label)
            raise RuntimeError(msg)
        valid_label = np.where(np.logical_and(label[:, 0] >= 0, label[:, 3] > label[:, 1],
                                              label[:, 4] > label[:, 2]))[0]
        if valid_label.size < 1:
            raise RuntimeError('Invalid label occurs.')

    def _estimate_label_shape(self):
        """Helper function to estimate label shape"""
        max_count = 0
        self.reset()
        try:
            while True:
                label, _ = self.next_sample()
                label = self._parse_label(label)
                max_count = max(max_count, label.shape[0])
        except StopIteration:
            pass
        self.reset()
        return (max_count, label.shape[1])

    def _parse_label(self, label):
        """Helper function to parse object detection label.

        Format for raw label:
        n \t k \t ... \t [id \t xmin\t ymin \t xmax \t ymax \t ...] \t [repeat]
        where n is the width of header, 2 or larger
        k is the width of each object annotation, can be arbitrary, at least 5
        """
        if isinstance(label, nd.NDArray):
            label = label.asnumpy()
        raw = label.ravel()
        if raw.size < 7:
            raise RuntimeError("Label shape is invalid: " + str(raw.shape))
        header_width = int(raw[0])
        obj_width = int(raw[1])
        if (raw.size - header_width) % obj_width != 0:
            msg = "Label shape %s inconsistent with annotation width %d." \
                %(str(raw.shape), obj_width)
            raise RuntimeError(msg)
        out = np.reshape(raw[header_width:], (-1, obj_width))
        # remove bad ground-truths
        valid = np.where(np.logical_and(out[:, 3] > out[:, 1], out[:, 4] > out[:, 2]))[0]
        if valid.size < 1:
            raise RuntimeError('Encounter sample with no valid label.')
        return out[valid, :]

    def reshape(self, data_shape=None, label_shape=None):
        """Reshape iterator for data_shape or label_shape.

        Parameters
        ----------
        data_shape : tuple or None
            Reshape the data_shape to the new shape if not None
        label_shape : tuple or None
            Reshape label shape to new shape if not None
        """
        if data_shape is not None:
            self.check_data_shape(data_shape)
            self.provide_data = [(self.provide_data[0][0], (self.batch_size,) + data_shape)]
        if label_shape is not None:
            self.check_label_shape(label_shape)
            self.provide_label = [(self.provide_label[0][0], (self.batch_size,) + label_shape)]


    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        path, target = self.samples[index]
        sample = self.loader(path)
        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

    def __len__(self):
        return len(self.samples)

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of datapoints: {}\n'.format(self.__len__())
        fmt_str += '    Root Location: {}\n'.format(self.root)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        tmp = '    Target Transforms (if any): '
        fmt_str += '{0}{1}'.format(tmp, self.target_transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str


IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif']


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


def accimage_loader(path):
    import accimage
    try:
        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)


def default_loader(path):
    from torchvision import get_image_backend
    if get_image_backend() == 'accimage':
        return accimage_loader(path)
    else:
        return pil_loader(path)


class ImageDetection(DatasetDetection):
    """A generic data loader where the images are arranged in this way: ::

        root/dog/xxx.png
        root/dog/xxy.png
        root/dog/xxz.png

        root/cat/123.png
        root/cat/nsdf3.png
        root/cat/asd932_.png

    Args:
        root (string): Root directory path.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.

     Attributes:
        classes (list): List of the class names.
        class_to_idx (dict): Dict with items (class_name, class_index).
        imgs (list): List of (image path, class_index) tuples
    """
    def __init__(self, root, transform=None, target_transform=None,
                 loader=default_loader):
        super(ImageFolder, self).__init__(root, loader, IMG_EXTENSIONS,
                                          transform=transform,
                                          target_transform=target_transform)
        self.imgs = self.samples
