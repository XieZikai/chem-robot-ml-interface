from torch import nn
from torchvision import models, transforms
from PIL import Image
import torch
import base64
import io
from io import BytesIO
import os


if torch.cuda.is_available():
    torch.backends.cudnn.deterministic = True
    device = torch.device('cuda')
else:
    device = torch.device('cpu')


mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
val_test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])


def load_solubility_model(model_path=None, num_features=256):
    if model_path is None:
        base_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(base_path, 'solubility_model.pth')
    # Model mimarisini yeniden oluştur
    model = models.resnet50(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_features)  # Son katmanı güncelle

    # Modelin ağırlıklarını yükle
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def predict_solubility_on_new_image(image_path, transform, device='cpu'):
    model = load_solubility_model()
    image = Image.open(image_path)  # Görüntüyü yükle
    image = transform(image).unsqueeze(0)  # Transform uygula ve boyut ekle

    # Tahmin yap
    with torch.no_grad():
        outputs = model(image.to(device))
        _, predicted = torch.max(outputs, 1)

    return predicted


def predict_solubility_on_base64_image(img, device='cpu'):
    model = load_solubility_model()
    image_data = base64.b64decode(img)
    image = Image.open(BytesIO(image_data)).convert('RGB')
    image = val_test_transforms(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image.to(device))
        _, predicted = torch.max(outputs, 1)

    return predicted.detach().numpy()[0]


def load_hsp_model(model_path=None):
    if model_path is None:
        base_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(base_path, '../ml_models/hsp_model.pth')
    # loads the model, sets to eval, moves to cpu, and returns the model
    model = torch.load(model_path)
    model.eval()
    model.to('cpu')
    return model


def predict_hsp_on_base64_image(img, concentration, device='cpu'):
    trans = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    model = load_hsp_model()
    image_data = base64.b64decode(img)
    image = Image.open(BytesIO(image_data)).convert('RGB')

    image = trans(image).unsqueeze(0)
    concentration = torch.tensor([[concentration]])

    # ensure the inputs are the correct data type
    image_tensor = image.float()
    concentration = concentration.float()

    # run inference
    with torch.no_grad():
        outputs = model.forward(image_tensor, concentration)

    # return prediction
    return outputs.item()

