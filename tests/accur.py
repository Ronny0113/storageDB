import numpy as np

# Функция для загрузки меток
def load_labels(filename):
    with open(filename, 'rb') as f:
        f.read(8)  # Пропустить заголовок
        labels = np.fromfile(f, dtype=np.uint8)
    return labels

# Функция для загрузки изображений
def load_images(filename):
    with open(filename, 'rb') as f:
        f.read(16)  # Пропустить заголовок
        images = np.fromfile(f, dtype=np.uint8).reshape(-1, 784)  # 28x28 = 784
        images = images / 255.0  # Нормализация
    return images

# Функция для загрузки весов
def load_weights(filename):
    return np.loadtxt(filename, delimiter=',')  # Загрузка весов из CSV

# Функция для Softmax
def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)

# Функция для предсказания классов
def predict(X, weights):
    linear_output = np.dot(X, weights)
    predictions = softmax(linear_output)
    return np.argmax(predictions, axis=1)

# Загрузка данных
test_images = load_images('t10k-images.idx3-ubyte')
test_labels = load_labels('t10k-labels.idx1-ubyte')

# Загрузка весов
weights = load_weights('perceptron_weights.csv')

# Предсказание
predicted_labels = predict(test_images, weights)

# Вычисление точности
accuracy = np.mean(predicted_labels == test_labels) * 100  # Процент правильных предсказаний

print(f"Точность проверки на тестовом наборе: {accuracy:.2f}%")
