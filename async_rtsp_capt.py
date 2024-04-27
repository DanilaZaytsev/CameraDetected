import cv2
import os
import asyncio
import time
import requests
from datetime import datetime

async def capture_rtsp_stream(rtsp_url, output_dir, identifier, api_url):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Ошибка: Не удалось установить соединение с RTSP потоком {rtsp_url}")
        return

    ret, frame = cap.read()

    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"snapshot_{identifier}_{timestamp}.jpg")

        cv2.imwrite(filename, frame)
        print(f"Скриншот от RTSP потока {rtsp_url} сохранен как {filename}")

        # Отправка файла на сервер Flask
        files = {'file': open(filename, 'rb')}
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            print("Файл успешно отправлен на сервер Flask")
        else:
            print("Произошла ошибка при отправке файла на сервер Flask")

    else:
        print(f"Ошибка: Не удалось получить кадр из RTSP потока {rtsp_url}")

    cap.release()

# Функция для создания скриншотов по расписанию
async def capture_screenshots(rtsp_streams, output_dir, api_url):
    tasks = [capture_rtsp_stream(rtsp_url, output_dir, identifier, api_url) for identifier, rtsp_url in rtsp_streams.items()]
    await asyncio.gather(*tasks)

async def start_screenshot_scheduler(rtsp_streams, output_dir, schedule_times, api_url):
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in schedule_times:
            await capture_screenshots(rtsp_streams, output_dir, api_url)
        await asyncio.sleep(30)

rtsp_streams = {
    "alias1": "rtsp_url1",
    "alias22": "rtsp_url2"
}  # список rtsp потоков с камер  и их алиасы(к прим.номера аудиторий)
output_dir = "куда складывать"
schedule_times = {"10:00", "12:00", "14:00", "16:00", "18:00", "20:00"}
api_url = "http://localhost:порт/detect_objects"

asyncio.run(start_screenshot_scheduler(rtsp_streams, output_dir, schedule_times, api_url))
