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


class MultiDatasetFolder(data.Dataset):
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

    def __init__(self, root, folders, ext_names, loader, extensions, transforms=None, target_transforms=None):

        multi_samples = []
        multi_datasets = []
    	
        self.folders = folders
        # print(ext_names)
        for i, (folder, ext_name) in enumerate(zip(folders, ext_names)):
           
            data_root = os.path.join(root, folder)
           
            data_info = {}
            data_info['toot'] = data_root
            classes, class_to_idx = self._find_classes(data_root)
            # print('classes, class_to_idx', )

            data_info['classes'] = classes
            data_info['class_to_idx'] = class_to_idx

            if i > 0:
                # print(ext_name)
                self._compare_classes(classes, class_to_idx)
                
                data_info['samples'] = self._compare_filename(folder, ext_name)

                # self.samples
            else:
                
                self.main_folder = folder
                self.classes = classes
                self.class_to_idx = class_to_idx
                # print(data_root, class_to_idx, extensions)
                if isinstance(ext_name, str):
                    self.main_ext_name = ext_name
                    extensions = [ext_name]
                samples = make_dataset(data_root, class_to_idx, extensions)
                # print(samples)
                if len(samples) == 0:
                    raise(RuntimeError("Found 0 files in subfolders of: " + data_root + "\n"
                                        "Supported extensions are: " + ",".join(extensions)))
                
                self.samples = samples
                data_info['samples'] = samples

            multi_datasets.append(data_info)
        
        self.multi_datasets = multi_datasets

        self.root = root
        self.loader = loader
        self.extensions = extensions

       
        self.targets = [s[1] for s in samples]

        if transforms == None:
            transforms= range(len(folders))

        if target_transforms == None:
            target_transforms= range(len(folders))

        self.transforms = transforms
        self.target_transforms = target_transforms

    def _compare_classes(self, classes, class_to_idx):
        same_classes = (self.classes == classes) and (self.class_to_idx == class_to_idx)
        if not same_classes:
            raise(RuntimeError("self.classes different from other folder's classes; \n" +
                                   "self.classes : " + self.classes + " other classes: "+ classes ))
        return same_classes

    def _compare_filename(self, folder, ext_name=None):

        samples = []
        for i, sample in enumerate(self.samples):
            path, class_id = sample

            new_path = path.replace(self.main_folder, folder)
            # print(ext_name, self.main_ext_name)
            if not (ext_name == None):
                # print('replace')
                new_path = new_path.replace(self.main_ext_name, ext_name)
            # print(new_path)
            if not os.path.isfile(new_path):
                raise(RuntimeError("self.classes different from other folder's classes; \n" +
                                "self.classes : " + self.classes + " other classes: "+ classes ))
            item = (new_path, class_id)
            samples.append(item)
        
        return samples


    def _find_classes(self, dir):
        """
        Finds the class folders in a dataset.

        Args:
            dir (string): Root directory path.

        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.

        Ensures:
            No class is a subdirectory of another.
        """
        if sys.version_info >= (3, 5):
            # Faster and available in Python 3.5 and above
            classes = [d.name for d in os.scandir(dir) if d.is_dir()]
        else:
            classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx

    def __getitem__(self, index):
        # print(index)
        """
        Args:
            index (int): Index

        Returns:
            tuple: (samples, targets) where targets is a array of the class_index of the target class.
        examples ([samples1,samples2,samples3], [target1,samples2,samples3])
        """
        # path, target = self.samples[index]
        multi_samples = []
        multi_targets = []
        for dataset, transform, target_transform in zip(self.multi_datasets, self.transforms, self.target_transforms):
            path, target = dataset['samples'][index]
            # print(path, target)

            sample = self.loader(path)
            if not isinstance(transform, int):
                sample = transform(sample)
            if not isinstance(target_transform, int):
                target = target_transform(target)

            # print(sample.size)
            # img.convert('RGB')
            
            multi_samples.append(sample)
            multi_targets.append(target)

        return multi_samples, multi_targets

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


class MultiImageFolder(MultiDatasetFolder):
    """A generic data loader where the images are arranged in this way: ::

        root/folder/dog/xxx.png
        root/folder/dog/xxy.png
        root/folder/dog/xxz.png

        root/folder/cat/123.png
        root/folder/cat/nsdf3.png
        root/folder/cat/asd932_.png

    Args:
        root (string): Root directory path.
        folders (list): List of the folder names. E.g, ``['folder1','folder2', 'folder3']``
        ext_names (list): List of the filename ends with a extension names. E.g, ``['jpg', 'jpg','jpg']``
        transforms (list(callable, optional)): A list of function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.ToTensor``
        target_transforms (list(callable, optional)): A list of function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.

     Attributes:
        classes (list): List of the class names.
        class_to_idx (dict): Dict with items (class_name, class_index).
        imgs (list): List of (image path, class_index) tuples

    example：
        from torchvision import transforms
        datasets = MultiImageFolder('root',['folder1','folder2', 'folder3'],['jpg', 'jpg','jpg'],[transforms.ToTensor(), transforms.ToTensor(), transforms.ToTensor()])
        
        for i in datasets:
            samples, targets = i
            # print(targets) => [0, 0, 0]
            # print(len(samples)) => 3
            print(samples[0].size())
    """

    # root, folders, ext_names
    def __init__(self, root, folders, ext_names, transforms=None, target_transforms=None,
                 loader=default_loader):
        super(MultiImageFolder, self).__init__(root, folders, ext_names, loader, IMG_EXTENSIONS,
                                          transforms=transforms,
                                          target_transforms=target_transforms)
        self.imgs = self.samples


# from torch.utils.data import DataLoader
# from torchvision import transforms
# datasets = MultiImageFolder('root',['folder1','folder2','folder3', 'folder4'],['jpg', 'jpg', 'jpg', 'png'],[transforms.ToTensor(), transforms.ToTensor(),transforms.ToTensor(), transforms.ToTensor()])

# # data = datasets.getitem()


# dataloader = DataLoader(datasets,3)

# batch = next(iter(dataloader))
# # print(batch)
# (samples, targets) = batch
# print(samples[0].size())


# for i in DataLoader(datasets,2):
#     samples, targets = i
    # print('targets',targets) #=> [0, 0, 0]
    # print('samples', len(samples)) #=> 3
    # print(samples[0].size())
