# Stability AI | Stable Video Deffusion (SVD)
 
![sample1](assets/000.jpg)


## 1. Установка зависимостей

```python
pip install -r requirements.txt
```
```python
pip install .
```
```python
mkdir checkpoints
```

## 2. Скачиваем нужные модели
для скачивания большой модели обученой на 25 кадровых видео
$: wget -O ./checkpoints/svd_xt.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true'

для скачивания модели обученой на 14 кадровых видео, + она более облегчёная, если VRAM сильно будет прожирать, берите это
$: wget -O ./checkpoints/svd.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/resolve/main/svd.safetensors?download=true'
-----------------------------------------


## 3. Попробовать запустить на сервере start_local.py

```python
python3 start_local.py
```