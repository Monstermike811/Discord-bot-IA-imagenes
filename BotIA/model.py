from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def get_class(model_path, labels_path, image_path):
    np.set_printoptions(suppress=True)
    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r", encoding="utf-8").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]*100

    if class_name[2:].startswith("Objeto cortopunzante"):
        return f"Ese es un objeto cortopunzante, manejalo con cuidado y utiliza un estuche de preferencia, confianza del {confidence_score}"
    elif class_name[2:].startswith("Humo"):
        return f"Eso es humo, sus posibles causas es fuego, cigarrillos, vapers u objetos calientes, cuidado, confianza del {confidence_score}"
    elif class_name[2:].startswith("Arma de fuego"):
        return f"Esa es un arma de fuego, en extremo peligrosas, mejor no ser utilizadas, confianza del {confidence_score}"
    elif class_name[2:].startswith("Objeto contundente"):
        return f"Ese es un objeto contundente, manejelo responsablemente y con cuidado, confianza del {confidence_score}"
    