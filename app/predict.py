# import packages for project

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import PIL
import scipy.ndimage as nd
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# data augmentation with torchvision.transforms
transformers = {'train_transforms' : transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.RandomRotation(20),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
]),
'test_transforms' : transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
]),
'valid_transforms' : transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
])}

trans = ['train_transforms', 'valid_transforms', 'test_transforms']
categories = ['train', 'val', 'test']
path = os.path.join(CURR_DIR, "pneumonia-pytorch-localization/chest_xray/")
# dset = {x: torchvision.datasets.ImageFolder(path+x, transform=transformers[y]) for x, y in zip(categories, trans)}
dset = {x: str(x) for x in categories}  # Passing alternative for deployment - Comment this while fitting
dataset_sizes = {x: len(dset[x]) for x in categories}

# Build model
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.model = torchvision.models.resnet152(pretrained=True)
        self.classifier = nn.Sequential(
            nn.Linear(self.model.fc.in_features, 2),
            nn.LogSoftmax(dim=1)
        )
        for params in self.model.parameters():
            params.requires_grad = False
        self.model.fc = self.classifier

    def forward(self, x):
        return self.model(x)

    def fit(self, dataloaders, num_epochs):
        train_on_gpu = torch.cuda.is_available()
        optimizer = optim.Adam(self.model.fc.parameters())
        scheduler = optim.lr_scheduler.StepLR(optimizer, 4)
        criterion = nn.NLLLoss()
        since = time.time()

        best_model_wts = copy.deepcopy(self.model.state_dict())
        best_acc = 0.0
        if train_on_gpu:
            self.model = self.model.cuda()
        for epoch in range(1, num_epochs + 1):
            print("epoch {}/{}".format(epoch, num_epochs))
            print("-" * 10)

            for phase in ['train', 'test']:
                if phase == 'train':
                    scheduler.step()
                    self.model.train()
                else:
                    self.model.eval()

                running_loss = 0.0
                running_corrects = 0.0

                for inputs, labels in dataloaders[phase]:
                    if train_on_gpu:
                        inputs = inputs.cuda()
                        labels = labels.cuda()
                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = self.model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]
                print("{} loss:  {:.4f}  acc: {:.4f}".format(phase, epoch_loss, epoch_acc))

                if phase == 'test' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(self.model.state_dict())

        time_elapsed = time.time() - since
        print('time completed: {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 600))
        print("best val acc: {:.4f}".format(best_acc))

        self.model.load_state_dict(best_model_wts)
        return self.model


model = Model()
# Loading the saved model for prediction
state_dict = torch.load(os.path.join(CURR_DIR, "./pneumonia-pytorch-localization/weights/best_pnemonia_model.pth"), map_location='cpu')
model.load_state_dict(state_dict)
model_ft = model.model
model_ft = model_ft.eval()
loader = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(),
                            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])


def image_loader(image_name):
    image = PIL.Image.open(image_name).convert("RGB")
    image = loader(image).float()
    image = image.unsqueeze(0)
    return image


class LayerActivations():
    features = []

    def __init__(self, model):
        self.hooks = []
        self.hooks.append(model.layer4.register_forward_hook(self.hook_fn))

    def hook_fn(self, module, input, output):
        self.features.append(output)

    def remove(self):
        for hook in self.hooks:
            hook.remove()


def predict_img(path):
    image_path = path
    img = image_loader(image_path)
    acts = LayerActivations(model_ft)
    # img = img.cuda()
    logps = model_ft(img)
    ps = torch.exp(logps)
    out_features = acts.features[0]
    out_features = torch.squeeze(out_features, dim=0)
    out_features = np.transpose(out_features.cpu(), axes=(1, 2, 0))
    W = model_ft.fc[0].weight
    top_probs, top_classes = torch.topk(ps, k=2)
    pred = np.argmax(ps.detach().cpu())
    w = W[pred,:]
    cam = np.dot(out_features.cpu(), w.detach().cpu())
    class_activation = nd.zoom(cam, zoom=(32, 32), order=1)
    img = img.cpu()
    img = torch.squeeze(img, 0)
    img = np.transpose(img, (1, 2, 0))
    mean = np.array([0.5, 0.5, 0.5])
    std = np.array([0.5, 0.5, 0.5])
    img = img.numpy()
    img = (img + mean) * std
    img = np.clip(img, a_max=1, a_min=0)
    return img, class_activation, pred
