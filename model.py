import torch
import torchvision.models as models
from torchvision.models import MobileNet_V2_Weights
from utils import preprocess_image


class ImageClassifier:
    def __init__(self):
        # Используем легкую и быструю предобученную нейросеть MobileNetV2
        self.weights = MobileNet_V2_Weights.DEFAULT
        self.model = models.mobilenet_v2(weights=self.weights)
        self.model.eval()  # Переводим в режим оценивания (evaluation)

        # Получаем названия классов ImageNet (1000 классов)
        self.categories = self.weights.meta["categories"]

    def predict(self, file_bytes: bytes, top_k: int = 3) -> list[dict]:
        """
        Предобрабатывает картинку, выполняет инференс и возвращает Top-K вероятностей.
        """
        # Предобработка
        input_tensor = preprocess_image(file_bytes)

        # Выполнение предсказания (без вычисления градиентов для ускорения)
        with torch.no_grad():
            output = self.model(input_tensor)
            # Применяем Softmax для получения вероятностей (от 0 до 1)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Получаем индексы и значения для top_k наибольших вероятностей
        top_prob, top_catid = torch.topk(probabilities, top_k)

        results = []
        for i in range(top_k):
            class_name = self.categories[top_catid[i]]
            score = float(top_prob[i])
            results.append({
                "rank": i + 1,
                "label": class_name,
                "confidence": round(score, 4),
                "confidence_percentage": f"{round(score * 100, 2)}%"
            })

        return results


# Синглтон модели для повторного использования
classifier = ImageClassifier()