from torch import nn
from torchvision import models, transforms
from PIL import Image
import torch
import base64
from io import BytesIO


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


def load_model(model_path, num_features=256):
    # Model mimarisini yeniden oluştur
    model = models.resnet50(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_features)  # Son katmanı güncelle

    # Modelin ağırlıklarını yükle
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def test_model_on_new_image(model, image_path, transform, device):
    image = Image.open(image_path)  # Görüntüyü yükle
    image = transform(image).unsqueeze(0)  # Transform uygula ve boyut ekle

    # Tahmin yap
    with torch.no_grad():
        outputs = model(image.to(device))
        _, predicted = torch.max(outputs, 1)

    return predicted


def test_model_on_base64_image(model, img, device):
    image_data = base64.b64encode(img)
    image = Image.open(BytesIO(image_data))
    image = val_test_transforms(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image.to(device))
        _, predicted = torch.max(outputs, 1)

    return predicted
