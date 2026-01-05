🚦 Smart Traffic Signal System

An AI-powered adaptive traffic signal control system that dynamically adjusts green signal time based on real-time traffic density estimation using computer vision.

🧠 Problem Statement

Traditional traffic signals operate on fixed timers, which leads to:

Unnecessary congestion

Increased waiting time

Poor handling of uneven traffic flow

This project aims to optimize traffic signal timing dynamically based on actual traffic density at an intersection.

💡 Solution Overview

The system uses:

Computer Vision (OpenCV) to estimate traffic density from images

Adaptive logic to allocate green signal time proportionally

Flask backend to connect the frontend and processing logic

Web-based UI for interaction and visualization

⚙️ How It Works (Flow)

User uploads traffic images from four directions (North, South, East, West)

Images are processed using OpenCV to estimate traffic density

A controller algorithm calculates green time for each direction

The road with the highest density gets priority

Signal states and countdown timer are updated in real time on the UI

🛠️ Tech Stack

Backend: Python, Flask

Computer Vision: OpenCV, NumPy

Frontend: HTML, CSS, JavaScript

Tools: VS Code, GitHub

📂 Project Structure
Smart-Traffic-Signal/
├── APP_traffic.py
├── traffic_density.py
├── traffic_controller.py
├── templates/
│   └── index.html
├── static/
│   ├── css_traffic.css
│   └── js_traffic.js
├── requirements.txt
└── README.md

▶️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the Flask application
python APP_traffic.py

3️⃣ Open in browser
http://localhost:5000

🚀 Features

Dynamic green signal allocation

Real-time traffic density estimation

Modular and scalable architecture

Simple and interactive web interface

🎯 Use Cases

Smart city traffic management

Congestion control at intersections

Simulation of adaptive traffic systems

📌 Future Improvements

Integrate real-time CCTV feed

Use deep learning (YOLO) for vehicle detection

Deploy system on cloud or edge devices

🏆 Hackathon Note

This project was developed as part of a hackathon to demonstrate the application of AI and computer vision in solving real-world traffic management problems.
