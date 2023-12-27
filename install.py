import os
import subprocess

subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
subprocess.run(['pip', 'install', '.'])
os.makedirs('checkpoints', exist_ok=True)

# Скачивание модели обученной на 25 кадрах
subprocess.run(['wget', '-O', './checkpoints/svd_xt.safetensors', 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true'])

# Скачивание более легкой модели обученной на 14 кадрах
subprocess.run(['wget', '-O', './checkpoints/svd.safetensors', 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/resolve/main/svd.safetensors?download=true'])