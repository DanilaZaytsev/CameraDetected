import cv2
import os
import asyncio
import time
from datetime import datetime
import aiortc

async def capture_rtsp_stream(rtsp_url, output_dir, identifier):
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
    else:
        print(f"Ошибка: Не удалось получить кадр из RTSP потока {rtsp_url}")

    cap.release()

# Функция для создания скриншотов по расписанию
async def capture_screenshots(rtsp_streams, output_dir):
    tasks = [capture_rtsp_stream(rtsp_url, output_dir, identifier) for identifier, rtsp_url in rtsp_streams.items()]
    await asyncio.gather(*tasks)

async def start_screenshot_scheduler(rtsp_streams, output_dir, schedule_times):
    while True:

        now = datetime.now().strftime("%H:%M")
        if now in schedule_times:
            await capture_screenshots(rtsp_streams, output_dir)
        await asyncio.sleep(30)

rtsp_streams = {
    "alias1": "ваш_rtsp_url1",
    "alias22": "ваш_rtsp_url2"
}  # словарь с идентификаторами и RTSP потоками
output_dir = "путь_к_вашей_директории"
schedule_times = {"10:00", "12:00", "14:00", "16:00", "18:00", "20:00"}


asyncio.run(start_screenshot_scheduler(rtsp_streams, output_dir, schedule_times))
