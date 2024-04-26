import cv2
import os
from datetime import datetime
import schedule
import time

def capture_rtsp_stream(rtsp_url, output_dir):
    # Проверяем, существует ли выходная директория, если нет - создаем
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Устанавливаем соединение с RTSP потоком
    cap = cv2.VideoCapture(rtsp_url)

    # Проверяем, установлено ли соединение
    if not cap.isOpened():
        print("Ошибка: Не удалось установить соединение с RTSP потоком")
        return

    # Считываем кадр из потока
    ret, frame = cap.read()

    # Проверяем, успешно ли считан кадр
    if ret:
        # Генерируем имя файла на основе текущего времени
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"snapshot_{timestamp}.jpg")

        # Сохраняем скриншот в файл
        cv2.imwrite(filename, frame)
        print(f"Скриншот сохранен как {filename}")
    else:
        print("Ошибка: Не удалось получить кадр из RTSP потока")

    # Освобождаем захват видеопотока и закрываем окно
    cap.release()
    cv2.destroyAllWindows()

# Функция для создания скриншота по расписанию
def capture_screenshot_job(rtsp_url, output_dir):
    capture_rtsp_stream(rtsp_url, output_dir)

# Функция для настройки расписания
def setup_schedule(rtsp_url, output_dir, schedule_times):
    for time_str in schedule_times:
        schedule.every().day.at(time_str).do(capture_screenshot_job, rtsp_url, output_dir)

# Пример использования функции
rtsp_url = "ваш_rtsp_url"
output_dir = "путь_к_вашей_директории"
schedule_times = ["10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]

setup_schedule(rtsp_url, output_dir, schedule_times)

# Запускаем цикл выполнения расписания
while True:
    schedule.run_pending()
    time.sleep(1)
