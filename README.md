# 🧭 Shortest Path Travel Planner (Dijkstra’s Algorithm & Graph Integration)

A web-based travel planning system that finds the **shortest route between cities** using **Dijkstra’s Algorithm** and provides **route-wise travel insights** (places to visit + famous foods) for **all cities along the shortest path**.

---

## 📌 Project Overview
The **Shortest Path Travel Planner** is a web application that helps users select a **source city** and **destination city**, then calculates the **shortest travel path** based on travel-time weights stored in a graph.  
The system models:

- **Cities → Nodes**
- **Routes → Edges**
- **Travel Time → Weights**

The project uses **Dijkstra’s Algorithm** for shortest path computation and enhances travel planning by displaying **city-wise insights** for every city present in the computed route.

---

## 🎯 Problem Statement
To design and develop a travel planning platform that computes the **shortest travel path** between cities using **Dijkstra’s Algorithm** and provides **route-wise travel recommendations** such as tourist attractions and local foods.

---

## 🚀 Features
✅ User Registration & Login (SQLite database)  
✅ Source & Destination City Selection  
✅ Shortest Path Calculation using **Dijkstra’s Algorithm**  
✅ Displays:
- shortest route (city-to-city)
- total travel time  

✅ Google Maps Direction Link  
✅ Route-wise Travel Insights for all cities in path:
- ⭐ Best places to visit
- 🍴 Famous food to taste  

✅ Clean UI + city modal popups  
✅ REST API Backend (Flask)

---

## 🛠️ Technologies Used

### ✅ Frontend
- HTML5
- CSS3
- JavaScript
- Tailwind CSS

### ✅ Backend
- Python
- Flask
- Flask-CORS
- SQLite3

### ✅ Graph & Algorithm
- NetworkX
- JSON (`graph_data.json`)

---

## 🗂️ Project Structure
Travel_Planner_Guide/
│
├── graph_app.py # Flask backend API
├── graph_logic.py # Graph loading + shortest path logic
├── graph_data.json # Cities and routes (nodes & edges)
├── travel_planner_users.db # SQLite database (auto-created)
│
├── frontend/
│ ├── login.html # Login page
│ ├── register.html # Registration page
│ ├── index.html # Main travel planner page
│
└── README.md 


---

## ⚙️ How to Run the Project

### ✅ Step 1: Open Project Folder
Open terminal / PowerShell inside:


---

### ✅ Step 2: Install Required Python Packages
```bash
pip install flask flask-cors networkx python-dotenv

Start Backend (Flask API)
cd backend
python graph_app.py

Start Frontend Server
cd frontend
python -m http.server 5500

Open in browser:
http://127.0.0.1:5500/login.html

