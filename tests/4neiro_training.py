import numpy as np
import matplotlib.pyplot as plt  # Импортируем matplotlib для построения графиков
import time  # Импортируем модуль time для измерения времени выполнения

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

# Перцептрон
class SimplePerceptron:
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) * 0.01  # Инициализация весов
        self.bias = np.zeros((1, output_size))  # Инициализация смещений

    def train(self, X, y, epochs, learning_rate):
        accuracy_history = []  # Список для хранения точности
        for epoch in range(epochs):
            # Прямое распространение
            linear_output = np.dot(X, self.weights) + self.bias
            predictions = self.softmax(linear_output)

            # Обратное распространение
            self.update_weights(X, predictions, y, learning_rate)

            # Вычисление точности после каждой эпохи
            accuracy = self.calculate_accuracy(predictions, y)
            accuracy_history.append(accuracy)
            print(f'Эпоха {epoch + 1}/{epochs}, Точность: {accuracy:.4f}')  # Вывод точности

        return accuracy_history  # Возвращаем историю точности

    def update_weights(self, X, predictions, y, learning_rate):
        # Вычисляем градиент
        m = y.shape[0]  # количество примеров
        gradient = np.dot(X.T, (predictions - y)) / m
        self.weights -= learning_rate * gradient
        self.bias -= learning_rate * np.sum(predictions - y, axis=0, keepdims=True) / m

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / np.sum(e_x, axis=1, keepdims=True)

    def calculate_accuracy(self, predictions, y):
        # Вычисление точности
        predicted_classes = np.argmax(predictions, axis=1)  # Получаем классы с максимальной вероятностью
        true_classes = np.argmax(y, axis=1)  # Истинные классы
        accuracy = np.mean(predicted_classes == true_classes)  # Расчет точности
        return accuracy

    def save_weights(self, filename):
        np.savetxt(filename, self.weights, delimiter=',')  # Сохранение весов в файл

# Загрузка данных
train_images = load_images('train-images.idx3-ubyte')
train_labels = load_labels('train-labels.idx1-ubyte')

test_images = load_images('t10k-images.idx3-ubyte')
test_labels = load_labels('t10k-labels.idx1-ubyte')

# Преобразование меток в один-к многим (one-hot encoding)
num_classes = 10
train_labels_one_hot = np.zeros((train_labels.size, num_classes))
train_labels_one_hot[np.arange(train_labels.size), train_labels] = 1

# Обучение перцептрона
input_size = 784  # Для изображений 28x28 пикселей
output_size = num_classes
perceptron = SimplePerceptron(input_size, output_size)

# Параметры обучения
epochs = 10000
learning_rate = 0.01

# Замер времени выполнения
start_time = time.time()  # Начало замера времени

# Обучаем перцептрон и получаем историю точности
accuracy_history = perceptron.train(train_images, train_labels_one_hot, epochs, learning_rate)

# Завершение замера времени
end_time = time.time()  # Завершение замера времени
elapsed_time = end_time - start_time  # Расчет времени выполнения

# Сохранение весов
perceptron.save_weights('perceptron_weights.csv')

# Построение графика точности
plt.plot(range(1, epochs + 1), accuracy_history)
plt.title('Зависимость точности от количества эпох')
plt.xlabel('Эпохи')
plt.ylabel('Точность')
plt.grid()
plt.show()

print(f"Обучение завершено и веса сохранены в 'perceptron_weights.csv'. Время выполнения: {elapsed_time:.2f} секунд.")