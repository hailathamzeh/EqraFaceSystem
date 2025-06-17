FROM python:3.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install all system dependencies for Qt, OpenCV, and X11 GUI support
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxrender-dev \
    libxcb1 \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-util0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5core5a \
    qt5-default \
    qtbase5-dev \
    libfontconfig1 \
    libfreetype6 \
    libxkbcommon0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    x11-apps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the correct Qt plugin path (for PyQt5 apps)
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ✅ Remove OpenCV's broken Qt plugin folder to avoid conflict with PyQt5
RUN rm -rf /usr/local/lib/python3.7/site-packages/cv2/qt

# Copy application files
COPY ./app /app

# Run the application
CMD ["python", "UserInterface.py"]
