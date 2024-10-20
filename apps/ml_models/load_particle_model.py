from PIL import Image
from torchvision import transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import base64_to_pil_image


class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, omega=10):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.omega = omega

    def forward(self, x):
        x = torch.sin(self.fc1(x) * self.omega)
        x = self.fc2(x)
        return x


class FILMLayer(nn.Module):
    def __init__(self, hidden_size, num_features, omega=10):
        super(FILMLayer, self).__init__()

        self.gamma = MLP(1, hidden_size, num_features, omega)
        self.beta = MLP(1, hidden_size, num_features, omega)

    def forward(self, x, condition):
        gamma = self.gamma(condition)[:, :, None, None]
        beta = self.beta(condition)[:, :, None, None]

        return x + (gamma * x + beta)


class Small(nn.Module):
    def __init__(
            self,
            film_hidden_size,
            film_omega,
            width_scale,
            head_hidden_size,
    ):
        super().__init__()

        width_1 = int(8 * width_scale)
        width_2 = int(16 * width_scale)
        width_3 = int(32 * width_scale)

        self.conv1 = nn.Conv2d(3, width_1, 7, 4, padding=3)  ## 28
        self.maxpool1 = nn.MaxPool2d(2, stride=2)  ## 14
        self.film1 = FILMLayer(film_hidden_size, width_1, film_omega)

        self.conv2 = nn.Conv2d(width_1, width_2, 3, padding=1)
        self.maxpool2 = nn.MaxPool2d(2, stride=2)  ## 7
        self.film2 = FILMLayer(film_hidden_size, width_2, film_omega)

        self.conv3 = nn.Conv2d(width_2, width_3, 3, padding=1)
        self.maxpool3 = nn.MaxPool2d(2, stride=2)
        self.film3 = FILMLayer(film_hidden_size, width_3, film_omega)

        self.fc1 = nn.Linear(width_3 * 7 * 7, head_hidden_size)
        self.fc2 = nn.Linear(head_hidden_size, 1)

    def forward(self, x, concentration):
        B = x.shape[0]
        x = self.film1(self.maxpool1(F.relu(self.conv1(x))), concentration)
        x = self.film2(self.maxpool2(F.relu(self.conv2(x))), concentration)
        x = self.film3(self.maxpool3(F.relu(self.conv3(x))), concentration)

        x = x.view(B, -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = x.view(-1)
        return x


class TargetNormalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def state_dict(self):
        return {'mean': self.mean, 'std': self.std}

    def load_state_dict(self, state_dict):
        self.mean = state_dict['mean']
        self.std = state_dict['std']

    def denormalize(self, target):
        return target * self.std + self.mean

    def __call__(self, target):
        return (target - self.mean) / self.std

    def __repr__(self):
        return self.__class__.__name__ + f"(mean={self.mean}, std={self.std})"


def get_model():
    return Small(
        film_hidden_size=32,
        film_omega=32,
        width_scale=2,
        head_hidden_size=1024
    )


def get_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])


# Load function
def load_model_and_normalizer(model, normalizer, filepath):
    state = torch.load(filepath)
    model.load_state_dict(state['model_state_dict'])
    normalizer.load_state_dict(state['normalizer_state_dict'])
    return model, normalizer


def predict(model, image_path, transform, normalizer, concentration):
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)
    model.eval()
    with torch.no_grad():
        output = model(image, torch.tensor([[concentration]]))
        output = normalizer.denormalize(output.item())
    return output


class ParticleModelLoader:
    def __init__(self):
        model = get_model()
        normalizer = TargetNormalize(0.0, 1.0)
        self.model, self.normalizer = load_model_and_normalizer(model, normalizer, './ml_models/particle_model.pt')
        self.transform = get_transforms()

    def predict(self, base64_image, concentration):
        image = base64_to_pil_image(base64_image)
        image = self.transform(image)
        image = image.unsqueeze(0)
        self.model.eval()
        with torch.no_grad():
            output = self.model(image, torch.tensor([[concentration]]))
            output = self.normalizer.denormalize(output.item())
        return output


if __name__ == "__main__":
    IMAGE_PATH = "./data_cropped_std/0.001con_400nm_ps_loop0.jpg"
    CONCENTRATION = 0.001

    model = get_model()
    normalizer = TargetNormalize(0.0, 1.0)
    load_model_and_normalizer(model, normalizer, "./production_models/model_all.pt")

    output = predict(model, IMAGE_PATH, get_transforms(), normalizer, CONCENTRATION)



