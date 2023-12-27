from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit
import os
import shutil
import psutil
import datetime
import cv2 

app = Flask(__name__)
socketio = SocketIO(app)

#TODO: DONE!
@app.route('/')
def index():
    return render_template('index.html')

#TODO: DONE!
def send_update():
    """
    Отправка события update_files с текущими данными по сокету.
    """
    folder_path = os.path.join(os.getcwd(), "videos")
    files = []
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            file_name, file_extension = os.path.splitext(f)
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            file_info = {'name': file_name, 'extension': file_extension, 'creation_time': creation_time}
            files.append(file_info)

    # Получение информации о памяти
    memory_info = psutil.virtual_memory()
    total_memory = round(memory_info.total / (1024 ** 2), 2)  # в мегабайтах
    used_memory = round(memory_info.used / (1024 ** 2), 2)
    free_memory = round(memory_info.available / (1024 ** 2), 2)

    socketio.emit('update_files', {'files': files, 'total_memory': total_memory, 'used_memory': used_memory, 'free_memory': free_memory})

#TODO: DONE!
def background_task():
    while True:
        send_update()
        socketio.sleep(2)

#TODO: DONE!
@app.route('/get_files', methods=['GET'])
def get_files_route():
    """
    Обертка для send_update, используемая для HTTP-запросов.
    """
    send_update()
    return jsonify({'message': 'Data sent successfully'})

#TODO: DONE!
@app.route('/delete_file/<token>', methods=['DELETE'])
def delete_file(token):
    """
    Удаление файла по токену (по названию файла - filename)
    """
    folder_path = os.path.join(os.getcwd(), "videos")
    
    for f in os.listdir(folder_path):
        file_name, file_extension = os.path.splitext(f)
        if file_name == token:
            file_path = os.path.join(folder_path, f"{file_name}{file_extension}")
            print(file_path)
            if os.path.exists(file_path):
                os.remove(file_path)

                send_update()
                return jsonify({'message': 'File deleted successfully'})
            else:
                return jsonify({'error': 'File not found'})
        
    return jsonify({'error': 'File not found'})
    
#TODO: DONE!
def get_filename_by_token(token):
    """
    Получаем путь к файлу, по токену (названию файла)
    """
    listdir = os.path.join(os.getcwd(), 'videos')
    dir = os.listdir(listdir)
    for file in dir:
        if file.split(".")[0] == token:
            return file
            break

#TODO: DONE!
@app.route('/download/<filename>')
def download_file(filename):
    """
    Получение файла по ссылке, для скачивания
    """

    folder_path = os.path.join(os.getcwd(), 'videos')
    return send_from_directory(folder_path, filename, as_attachment=True)


# GENERATION SVD
def generate_video(frames, output_path):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()

def process_image(image_data, parameters):
    # Реализуйте обработку изображения в видео с использованием модели stabilityai/stable-video-diffusion-img2vid-xt
    # И верните кадры видео

    # Пример: создание видео из случайных кадров
    # frames = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8) for _ in range(30)]
    frames = "Есть"
    return frames

@socketio.on('process_image')
def handle_process_image(data):
    image_data = data['image']
    parameters = data['parameters']

    frames = process_image(image_data, parameters)

    output_path = 'output.mp4'
    generate_video(frames, output_path)
    emit('video_ready', {'video_path': output_path})


if __name__ == '__main__':
    socketio.start_background_task(target=background_task)
    socketio.run(app, debug=True)