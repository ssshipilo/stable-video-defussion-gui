FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install einops opencv-python fire omegaconf openai-clip pytorch-lightning kornia open-clip-torch invisible-watermark scipy -f https://download.pytorch.org/whl/torch_stable.html xformers Flask Flask-SocketIO Flask-SQLAlchemy Flask-Migrate transformers

RUN mkdir -p ./checkpoints

RUN wget -O ./checkpoints/svd_xt.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true' && \
    wget -O ./checkpoints/svd.safetensors 'https://huggingface.co/stabilityai/stable-video-diffusion-img2vid/resolve/main/svd.safetensors?download=true'

CMD ["python3", "server.py"]