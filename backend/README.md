# 🧭 Shortest Path Travel Planner (Dijkstra’s Algorithm & Graph Integration)

## 📌 Project Overview
The **Shortest Path Travel Planner** is a web-based travel planning application that helps users find the **shortest travel route between two cities** using **Dijkstra’s Algorithm**.  
The application models cities as nodes and routes as weighted edges in a graph, where weights represent travel time. It also provides **route-wise travel insights** such as popular places to visit and famous foods to taste for all cities along the shortest path.

This project demonstrates the real-world application of **graph algorithms**, **data structures**, and **web technologies** in an interactive and user-friendly manner.

---

## 🎯 Problem Statement
To design and develop a travel planning platform that computes the **shortest travel path** between selected source and destination cities using **Dijkstra’s Algorithm** and provides **city-wise travel insights** for all cities in the computed route.

---

## 🚀 Features
✅ User Registration and Login  
✅ City Selection (Source & Destination)  
✅ Shortest Path Calculation using **Dijkstra’s Algorithm**  
✅ Displays total travel time and shortest route  
✅ Google Maps direction link for navigation  
✅ Route-wise travel insights:
- ⭐ Best places to visit  
- 🍴 Famous food to taste  
✅ Interactive UI with modal popups for cities  

---

## 🛠️ Technologies Used

### Frontend
- HTML5  
- CSS3  
- JavaScript  
- Tailwind CSS  

### Backend
- Python  
- Flask  
- Flask-CORS  

### Graph and Algorithm Tools
- NetworkX  
- JSON (for graph data storage)

---

## 🗂️ Project Structure
Travel_Planner_Guide/
│
├── graph_app.py
├── graph_logic.py
├── graph_data.json
├── travel_planner_users.db
├── .env (optional)
│
├── frontend/
│ ├── login.html
│ ├── register.html
│ ├── index.html
│
└── README.md 


---

## ⚙️ How to Run the Project

### ✅ Step 1: Install Required Modules
Open terminal / PowerShell inside the project folder and run:

```bash
pip install flask flask-cors networkx python-dotenv

Start Backend Server 
cd backend 
python graph_app.py


Run Frontend Server
cd frontend
python -m http.server 5500

Open in browser:
http://127.0.0.1:5500/login.html
