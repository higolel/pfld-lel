import time
import torch
import numpy as np
from options.train_options import TrainOptions
from data.wflw_dataset import createDatasets
from models.pfld_model import createModel
#from models.pfld_model import print_networks
from util.visualizer import Visualizer

if __name__ == '__main__':
    opt = TrainOptions().parse()
    trainDataLoader, valDataLoader = createDatasets(opt)
    pfldNet, auxiliaryNet = createModel(opt)

    print('---------- Networks initialized -------------')
    num_params = 0
    for param in pfldNet.parameters():
        num_params += param.numel()
    if opt.verbose:
        print(pfldNet)

    print('pfldNet Total number of parameters : %.3f M' % (num_params / 1e6))

    num_params = 0
    for param in auxiliaryNet.parameters():
        num_params += param.numel()
    if opt.verbose:
        print(auxiliaryNet)

    print('auxiliaryNet Total number of parameters : %.3f M' % (num_params / 1e6))
    print('-----------------------------------------------')

    optimizer = torch.optim.Adam(
        [{'params': pfldNet.parameters()}, {'params': auxiliaryNet.parameters()}],
        lr = opt.lr,
        weight_decay = opt.weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode = 'min', patience = opt.lr_patience, verbose = True)

    visualizer = Visualizer(opt)        # create a visualizer that display/save images and plots



