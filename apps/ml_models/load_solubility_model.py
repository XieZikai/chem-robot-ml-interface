import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import resnet18
from torchvision import transforms
from PIL import Image
from utils import base64_to_pil_image


def resnet(state_dict_path=None, n_classes=4):
    model = resnet18(weights='DEFAULT')
    model.fc = nn.Linear(model.fc.in_features, n_classes)
    if state_dict_path is not None:
        state_dict = torch.load(state_dict_path)
        model.load_state_dict(state_dict['model_state_dict'])

    return model


def load_model_solubility(model_path):
    model_dict = torch.load(model_path)
    model = resnet()
    model.load_state_dict(model_dict)

    return model


def get_transforms_solubility():
    test_transform = transforms.Compose([
        transforms.CenterCrop(1080),
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    return test_transform


def idx_to_class(idx, num_classes=4):
    classes = {
        2: ["soluble", "soluble", "insoluble", "insoluble"],
        3: ["colloidal", "soluble", "insoluble", "insoluble"],
        4: ["colloidal", "soluble", "insoluble", "partialsoluble"]
    }
    return classes[num_classes][idx]


class SolubilityModelLoader:
    def __init__(self):
        self.model = load_model_solubility('./ml_models/Production_fold_1.pt')
        self.transform = get_transforms_solubility()

    def predict(self, base64_image):
        image = base64_to_pil_image(base64_image)
        image = self.transform(image)
        image = image.unsqueeze(0)
        self.model.eval()
        with torch.no_grad():
            output = self.model(image)
            output = torch.argmax(output, dim=1)
        return idx_to_class(output.item())


def predict_solubility(model, image_path, transform):
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)
    model.eval()
    with torch.no_grad():
        output = model(image)
        output = torch.argmax(output, dim=1)
    return idx_to_class(output.item())
