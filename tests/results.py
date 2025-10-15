import numpy as np
import matplotlib.pyplot as plt

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
    return np.argmax(predictions, axis=1)  # Получаем класс с максимальной вероятностью

# Загрузка данных
test_images = load_images('t10k-images.idx3-ubyte')
test_labels = load_labels('t10k-labels.idx1-ubyte')

# Загрузка весов
weights = load_weights('perceptron_weights.csv')

# Предсказание
predicted_labels = predict(test_images, weights)

# Визуализация результатов
def plot_predictions(images, true_labels, predicted_labels, num_images=10):
    plt.figure(figsize=(10, 10))
    random_indices = np.random.choice(len(images), num_images, replace=False)  # Случайные индексы
    for i, idx in enumerate(random_indices):
        plt.subplot(5, 5, i + 1)
        plt.imshow(images[idx].reshape(28, 28), cmap='gray')
        plt.axis('off')
        plt.title(f'True: {true_labels[idx]}\nPred: {predicted_labels[idx]}', fontsize=12)
    plt.tight_layout()
    plt.show()

# Отображаем 10 случайных изображений с истинными и предсказанными метками
plot_predictions(test_images, test_labels, predicted_labels, num_images=10)

print("Проверка завершена, результаты визуализированы.")
