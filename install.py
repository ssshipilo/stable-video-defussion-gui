import os
import subprocess

print("\033[92m[AUTO INSTALL]\033[0m Dependencies from requirements.txt are set")
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
print("\033[92m[AUTO INSTALL]\033[0m Successful!!!")
print("\033[92m[AUTO INSTALL]\033[0m Install SVD as a package (Stable Video Diffusion Package)")
subprocess.run(['pip', 'install', '.'])
print("\033[92m[AUTO INSTALL]\033[0m Successful!!!")
print("\033[92m[AUTO INSTALL]\033[0m Update pip if needed")
subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

# Requirements (те которые не хотят тянутся с requirements.txt)
subprocess.run(['pip', 'install', 'einops'])
subprocess.run(['pip', 'install', 'opencv-python'])
subprocess.run(['pip', 'install', 'fire'])
subprocess.run(['pip', 'install', 'omegaconf'])
subprocess.run(['pip', 'install', 'openai-clip'])
subprocess.run(['pip', 'install', 'pytorch-lightning'])
subprocess.run(['pip', 'install', 'kornia'])
subprocess.run(['pip', 'install', 'open-clip-torch'])
subprocess.run(['pip', 'install', 'invisible-watermark'])
subprocess.run(['pip', 'install', 'SciPy'])
subprocess.run(['pip', 'install', 'torch==2.1.0+cu118', 'torchvision==2.1.0+cu118', 'torchaudio==2.1.0+cu118', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
subprocess.run(['pip', 'install', 'xformers'])
subprocess.run(['pip', 'install', '--ignore-installed', 'Flask'])
subprocess.run(['pip', 'install', 'Flask-SocketIO'])

# CUDA ограничитель 128, потому что ему хоть дай 80 гб, он всё сожрёт
subprocess.run(['PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:128'])

print("\033[92m[AUTO INSTALL]\033[0m Successful!!!")
os.makedirs('checkpoints', exist_ok=True)

# Скачивание модели обученной на 25 кадрах
print("\033[92m[AUTO INSTALL]\033[0m Download an enlarged model trained on video at 25 fps")
try:
    result = subprocess.run(['wget', '-O', './checkpoints/svd_xt.safetensors', 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true'], check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
print("\033[92m[AUTO INSTALL]\033[0m Successful!!!")

# Скачивание более легкой модели обученной на 14 кадрах
print("\033[92m[AUTO INSTALL]\033[0m Download an enlarged model trained on video at 14 fps")
try:
    result = subprocess.run(['wget', '-O', './checkpoints/svd.safetensors', 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/resolve/main/svd.safetensors?download=true'], check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
print("\033[92m[AUTO INSTALL]\033[0m Successful!!!")