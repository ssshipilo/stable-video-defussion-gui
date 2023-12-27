from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit
import os
import uuid
import psutil
import datetime
import cv2 
from model import sample
from fire import Fire
import os
import shutil

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
#TODO: DONE!
@app.route('/')
def index():
    return render_template('index.html')

#TODO: DONE!
def send_update():
    """
    Отправка события update_files с текущими данными по сокету.
    """
    folder_path = os.path.join(os.getcwd(), "outputs")
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
    folder_path = os.path.join(os.getcwd(), "outputs")
    
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
    listdir = os.path.join(os.getcwd(), 'outputs')
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

    folder_path = os.path.join(os.getcwd(), 'outputs')
    return send_from_directory(folder_path, filename, as_attachment=True)

# GENERATION SVD
def allowed_file(filename):
    """
    Проверка разрешенных расширений файлов
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#TODO: DONE!
@app.route('/generatevideo', methods=['POST'])
def generate_video():
    """
    ### Генерация видео, запрос принимает запросы

    #### Путь к картинке - Это путь к изображению, которое будет использоваться для создания видео.\n
    `input_path`          = os.path.join(os.getcwd(), "assets", "example.jpg")\n
    `num_frames`          = 25    # Количесвто фреймов\n
    `num_steps`           = 15    # Количество шагов - Это параметр, указывающий, сколько шагов выполнить при создании видео.\n
    `version`             = "svd_xt" # or 'svd_xt'\n
    `fps_id`              = 6     # Число кадров в секунду - Это количество кадров в секунду для создаваемого видео.\n
    `motion_bucket_id`    = 127   # Идентификатор "motion bucket" - Это идентификатор, связанный с движением, который влияет на результат видео.\n
    `cond_aug`            = 0.02  # Условное увеличение - Это параметр, связанный с аугментацией данных.\n
    `seed`                = 23    # Зерно для генерации случайных чисел - Это начальное значение для генератора случайных чисел.\n
    `decoding_t`          = 5    # Количество кадров, декодируемых за один раз! Это съедает больше всего VRAM. При необходимости уменьшите.
    `device`              = "cuda" # or 'cpu'
    `output_folder`       =  os.path.join(os.getcwd(), "outputs")
    """

    try:
        uploaded_files = []
        if 'file' not in request.files:
            return jsonify({"message": "No file part", "status": False}), 400

        uploads_folder = os.path.join(os.getcwd(), "uploads")
        for file_name in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                return jsonify({"message": f"Failed to delete {file_path}. Reason: {e}", "status": False}), 400

        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                uploaded_files.append(filename)

        if len(uploaded_files) == 0:
            return jsonify({"message": "No file part", "status": False}), 400

        select_version = request.form.get('select_version')
        fps_version = request.form.get('fps_version')
        num_steps = request.form.get('num_steps')
        fps_id = request.form.get('fps_id')
        motion_bucket = request.form.get('motion_bucket')
        cond_aug = request.form.get('cond_aug')
        seed = request.form.get('seed')
        decoding_t = request.form.get('decoding_t')

        # GENERATE
        print(select_version)
        input_path          = os.path.join(os.getcwd(), "uploads", uploaded_files[0])
        num_frames          = int(fps_version)          # Количесвто фреймов
        num_steps           = int(num_steps)            # Количество шагов - Это параметр, указывающий, сколько шагов выполнить при создании видео.
        version             = str(select_version)       # or 'svd_xt'
        fps_id              = int(fps_id)               # Число кадров в секунду - Это количество кадров в секунду для создаваемого видео.
        motion_bucket_id    = int(motion_bucket)        # Идентификатор "motion bucket" - Это идентификатор, связанный с движением, который влияет на результат видео.
        cond_aug            = float(cond_aug)           # Условное увеличение - Это параметр, связанный с аугментацией данных.
        seed                = int(seed)                 # Зерно для генерации случайных чисел - Это начальное значение для генератора случайных чисел.
        decoding_t          = int(decoding_t)           # Количество кадров, декодируемых за один раз! Это съедает больше всего VRAM. При необходимости уменьшите.
        device              = "cuda"                    # or 'cpu'
        output_folder       =  os.path.join(os.getcwd(), "outputs")

        Fire(sample(
            input_path,
            num_frames,
            num_steps,
            version,
            fps_id,
            motion_bucket_id,
            cond_aug,
            seed,
            decoding_t,
            device,
            output_folder
        ))

        return jsonify({"message": "Success!", "status": True})
    except Exception as e:
        return jsonify({"message": str(e), "status": False}), 400

def generate_video(frames, output_path):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()

if __name__ == '__main__':
    socketio.start_background_task(target=background_task)
    socketio.run(app, debug=True)