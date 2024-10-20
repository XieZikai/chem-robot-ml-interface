from torch import nn
from torchvision import models, transforms
from PIL import Image
import torch
import base64
import io
from io import BytesIO
import os
from utils import base64_to_pil_image


def load_hsp_model(model_path=None):
    if model_path is None:
        base_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(base_path, './ml_models/hsp_model.pth')
    # loads the model, sets to eval, moves to cpu, and returns the model
    model = torch.load(model_path)
    model.eval()
    model.to('cpu')
    return model


class HSPModelLoader:
    def __init__(self):
        self.model = load_hsp_model()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def predict(self, base64_image):
        image = base64_to_pil_image(base64_image)
        image = self.transform(image).unsqueeze(0)
        # todo: finish the prediction
