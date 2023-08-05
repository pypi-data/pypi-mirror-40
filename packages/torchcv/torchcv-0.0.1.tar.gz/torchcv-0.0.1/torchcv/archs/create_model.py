import os, sys
import torch

class createModel(torch.nn.Module):
    def name(self):
        return 'BaseModel'
    def __init__(self,arch):
        if arch == 'vae':   
            pass

        elif arch == 'cvae':
            pass
        elif arch == 'gan':
            pass
        elif arch == 'dcgan':
            pass
        elif arch == 'cvaegan':
            pass
        elif arch == 'crn':
            pass
        elif arch == 'pggan':
            pass
            
    def create(self, opt):    
        print(opt.model)            
        if opt.model == 'vid2vid':
            from .vid2vid_model_G import Vid2VidModelG
            modelG = Vid2VidModelG()    
            if opt.isTrain:
                from .vid2vid_model_D import Vid2VidModelD
                modelD = Vid2VidModelD()    
        else:
            raise ValueError("Model [%s] not recognized." % opt.model)

        if opt.isTrain:
            from .flownet import FlowNet
            flowNet = FlowNet()
        
        modelG.initialize(opt)
        if opt.isTrain and len(opt.gpu_ids):
            modelD.initialize(opt)
            flowNet.initialize(opt)        
            if opt.n_gpus_gen == len(opt.gpu_ids):
                modelG = nn.DataParallel(modelG, device_ids=opt.gpu_ids)
                modelD = nn.DataParallel(modelD, device_ids=opt.gpu_ids)
                flowNet = nn.DataParallel(flowNet, device_ids=opt.gpu_ids)
            else:             
                if opt.batchSize == 1:
                    gpu_split_id = opt.n_gpus_gen + 1
                    modelG = nn.DataParallel(modelG, device_ids=opt.gpu_ids[0:1])                
                else:
                    gpu_split_id = opt.n_gpus_gen
                    modelG = nn.DataParallel(modelG, device_ids=opt.gpu_ids[:gpu_split_id])
                modelD = nn.DataParallel(modelD, device_ids=opt.gpu_ids[gpu_split_id:] + [opt.gpu_ids[0]])
                flowNet = nn.DataParallel(flowNet, device_ids=[opt.gpu_ids[0]] + opt.gpu_ids[gpu_split_id:])
            return [modelG, modelD, flowNet]
        else:
            return modelG

    def initialize(self, opt):
        self.opt = opt
        self.gpu_ids = opt.gpu_ids
        self.isTrain = opt.isTrain
        self.Tensor = torch.cuda.FloatTensor if self.gpu_ids else torch.Tensor
        self.save_dir = os.path.join(opt.checkpoints_dir, opt.name)

    def set_input(self, input):
        self.input = input

    def forward(self):
        pass

    # used in test time, no backprop
    def test(self):
        pass

    def get_image_paths(self):
        pass

    def optimize_parameters(self):
        pass

    def get_current_visuals(self):
        return self.input

    def get_current_errors(self):
        return {}

    def save(self, label):
        pass

    # helper saving function that can be used by subclasses
    def save_network(self, network, network_label, epoch_label, gpu_ids):
        save_filename = '%s_net_%s.pth' % (epoch_label, network_label)
        save_path = os.path.join(self.save_dir, save_filename)
        torch.save(network.cpu().state_dict(), save_path)
        if len(gpu_ids) and torch.cuda.is_available():
            network.cuda(gpu_ids[0])

    def resolve_version(self):
        import torch._utils
        try:
            torch._utils._rebuild_tensor_v2
        except AttributeError:
            def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
                tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
                tensor.requires_grad = requires_grad
                tensor._backward_hooks = backward_hooks
                return tensor
            torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2

    # helper loading function that can be used by subclasses
    def load_network(self, network, network_label, epoch_label, save_dir=''):        
        self.resolve_version()    
        save_filename = '%s_net_%s.pth' % (epoch_label, network_label)
        if not save_dir:
            save_dir = self.save_dir
        save_path = os.path.join(save_dir, save_filename)        
        if not os.path.isfile(save_path):
            print('%s not exists yet!' % save_path)
            #if 'G' in network_label:
            #    raise('Generator must exist!')
        else:
            #network.load_state_dict(torch.load(save_path))
            try:
                network.load_state_dict(torch.load(save_path))
            except:   
                pretrained_dict = torch.load(save_path)                
                model_dict = network.state_dict()

                ### printout layers in pretrained model
                initialized = set()                    
                for k, v in pretrained_dict.items():                      
                    initialized.add(k.split('.')[0])                         
                #print('pretrained model has following layers: ')
                #print(sorted(initialized))                

                try:
                    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}                    
                    network.load_state_dict(pretrained_dict)
                    print('Pretrained network %s has excessive layers; Only loading layers that are used' % network_label)
                except:
                    print('Pretrained network %s has fewer layers; The following are not initialized:' % network_label)
                    if sys.version_info >= (3,0):
                        not_initialized = set()
                    else:
                        from sets import Set
                        not_initialized = Set()
                    for k, v in pretrained_dict.items():                      
                        if v.size() == model_dict[k].size():
                            model_dict[k] = v

                    for k, v in model_dict.items():
                        if k not in pretrained_dict or v.size() != pretrained_dict[k].size():
                            not_initialized.add(k.split('.')[0])                            
                    print(sorted(not_initialized))
                    network.load_state_dict(model_dict)                  

    def update_learning_rate():
        pass
