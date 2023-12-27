# Скачиваем ласт модель, можно в целом и 2 скачать, я в UI добавил возможность выбрать модель

$ - знак будет означать как команду в консоли, саму команду копировать без этого символа


-----------------------------------------
1.  

$ pip install -r requirements.txt
$ pip install .
$ cd ..
$ mkdir checkpoints
-----------------------------------------


-----------------------------------------
2.  
для скачивания большой модели обученой на 25 кадровых видео
$: wget -O ./checkpoints/svd_xt.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true'

для скачивания модели обученой на 14 кадровых видео, + она более облегчёная, если VRAM сильно будет прожирать, берите это
$: wget -O ./checkpoints/svd.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/resolve/main/svd.safetensors?download=true'
-----------------------------------------


3. Попробовать запустить на сервере start_local.py
python3 start_local.py

! если ругается за CUDA
$ pip install torch==2.1.0+cu118 torchvision==2.1.0+cu118 torchaudio==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html
