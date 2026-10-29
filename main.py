from fastapi import FastAPI, UploadFile, File, HTTPException, status
from model import classifier

app = FastAPI(
    title="AI Image Classifier API",
    description="API для классификации изображений с использованием предобученной нейросети MobileNetV2",
    version="1.0.0"
)

# Разрешенные MIME-типы файлов
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/webp"}


@app.get("/", summary="Проверка работоспособности сервиса")
async def root():
    return {
        "status": "online",
        "message": "AI Image Classifier API готов к работе. Перейдите на /docs для интерактивной документации."
    }


@app.post("/predict", summary="Классификация загруженного изображения")
async def predict_image(file: UploadFile = File(...)):
    """
    Принимает файл изображения (JPEG, PNG, WEBP),
    выполняет предобработку и инференс нейросетью MobileNetV2,
    возвращает Top-3 наиболее вероятных классов объектов.
    """
    # Валидация типа файла
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Неподдерживаемый формат файла '{file.content_type}'. Разрешены только: JPEG, PNG, WEBP."
        )

    try:
        # Чтение байтов из загруженного файла
        contents = await file.read()

        # Вызов классификатора
        predictions = classifier.predict(contents, top_k=3)

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "predictions": predictions
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обработке изображения: {str(e)}"
        )