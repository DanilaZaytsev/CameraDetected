import cv2
import os
from datetime import datetime
import schedule
import time

def capture_rtsp_stream(rtsp_url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Ошибка: Не удалось установить соединение с RTSP потоком")
        return

    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"snapshot_{timestamp}.jpg")

        cv2.imwrite(filename, frame)
        print(f"Скриншот сохранен как {filename}")
    else:
        print("Ошибка: Не удалось получить кадр из RTSP потока")

    cap.release()
    cv2.destroyAllWindows()

def capture_screenshot_job(rtsp_url, output_dir):
    capture_rtsp_stream(rtsp_url, output_dir)

def setup_schedule(rtsp_url, output_dir, schedule_times):
    for time_str in schedule_times:
        schedule.every().day.at(time_str).do(capture_screenshot_job, rtsp_url, output_dir)

# Параметры
rtsp_url = "rtsp_url"
output_dir = "путь_к_директории"
schedule_times = ["09:00", "09:40", "10:10"] #время пар

setup_schedule(rtsp_url, output_dir, schedule_times)

while True:
    schedule.run_pending()
    time.sleep(1)
