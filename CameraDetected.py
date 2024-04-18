import json
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from imageai.Detection import VideoObjectDetection

app = Flask(__name__)

def is_allowed_filename(filename):
    # Возвращает True, если имя файла допустимо
    return "." in filename


unique_persons = set()


def count_unique_persons(frame_number, output_array, output_count, returned_frame):
    global unique_persons
    if "person" in output_count:
        unique_persons.update(["person_" + str(i) for i in range(output_count["person"])])
        # Используем множество для хранения уникальных идентификаторов

def detect_objects_from_video(video_file_path):
    # Функция для обнаружения объектов в видеофайле
    execution_path = os.getcwd()
    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
    detector.loadModel()

    video_path = detector.detectObjectsFromVideo(
        input_file_path=video_file_path,
        output_file_path=os.path.join(execution_path, "pidors_detected"),
        frames_per_second=10, log_progress=True, per_frame_function=count_unique_persons, return_detected_frame=True
    )

    unique_persons_list = list(unique_persons)
    unique_persons_count = len(unique_persons_list)

    json_data = {"unique_persons_count": unique_persons_count, "unique_persons": unique_persons_list}
    with open(os.path.join(execution_path, "unique_persons.json"), "w") as json_file:
        json.dump(json_data, json_file)

    return unique_persons_count, video_path

@app.route("/detect_objects", methods=["POST"])
def detect_objects():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and is_allowed_filename(file.filename):
        filename = secure_filename(file.filename)
        video_file_path = os.path.join("uploads", filename)
        file.save(video_file_path)
        unique_persons_count, video_path = detect_objects_from_video(video_file_path)
        return jsonify({"unique_persons_count": unique_persons_count, "video_path": video_path})
    else:
        return jsonify({"error": "Invalid file name"})

if __name__ == "__main__":
    app.run(debug=False)