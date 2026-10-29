from io import BytesIO
from PIL import Image
import torch
from torchvision import transforms

# Стандартная трансформация для картинок на входе MobileNet_V2 / ResNet:
# Изменение размера, обрезка по центру, перевод в тензор и нормализация по ImageNet
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

def preprocess_image(file_bytes: bytes) -> torch.Tensor:
    """
    Принимает байты загруженного файла,
    конвертирует в RGB PIL Image и применяет пайплайн трансформаций.
    """
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    tensor = transform(image)
    # Добавляем batch dimension: [C, H, W] -> [1, C, H, W]
    return tensor.unsqueeze(0)