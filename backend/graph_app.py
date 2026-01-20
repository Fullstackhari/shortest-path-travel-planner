
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import sqlite3
import json
import networkx as nx
from backend.graph_logic import find_shortest_path
from dotenv import load_dotenv
import os  
#from openai import OpenAI

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app, supports_credentials=True)

# Load environment variables
load_dotenv()  
# -------------------------------
# Load Graph
# -------------------------------
try:
    import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(BASE_DIR, "graph_data.json")

with open(GRAPH_PATH, "r") as f:
    graph_data = json.load(f)


    G = nx.Graph()

    # ✅ Handle both structures
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if nodes and isinstance(nodes[0], dict):
        for node in nodes:
            G.add_node(node["id"], **node.get("attributes", {}))
    else:
        for node in nodes:
            G.add_node(node)

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        weight = edge.get("weight", 1)
        G.add_edge(src, tgt, weight=weight)

    print(f"✅ Graph loaded: {len(G.nodes)} nodes, {len(G.edges)} edges")

except Exception as e:
    print("⚠️ Error loading graph_data.json:", e)
    G = nx.Graph()

# -------------------------------
# Database Helpers
# -------------------------------
def get_db_connection():
    conn = sqlite3.connect("travel_planner_users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------
# User Routes
# -------------------------------
@app.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"status": "error", "message": "All fields required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            conn.close()
            return jsonify({"status": "error", "message": "Email already registered"}), 400

        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Registration successful"}), 200

    except Exception as e:
        print("⚠️ /register error:", e)
        return jsonify({"status": "error", "message": "Server error"}), 500
        
@app.route("/")
def home():
    return "Shortest Path Travel Planner Backend is Running ✅", 200


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'status': 'error', 'message': 'Email and password required'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and user["password"] == password:
            session['user'] = dict(user)
            return jsonify({'status': 'success', 'message': 'Login successful'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    except Exception as e:
        print("❌ Login error:", e)
        return jsonify({'status': 'error', 'message': 'Server error, please try again later'}), 500


@app.route("/api/status", methods=["GET"])
def user_status():
    user = session.get("user")
    if user:
        return jsonify({
            "logged_in": True,
            "username": user["username"],
            "email": user["email"]
        }), 200
    else:
        return jsonify({"logged_in": False}), 200


@app.route("/api/logout", methods=["POST"])
def logout_user():
    session.pop("user", None)
    return jsonify({"status": "success", "message": "Logged out"}), 200

# -------------------------------
# Graph API Routes
# -------------------------------
@app.route("/api/cities", methods=["GET"])
def get_cities():
    try:
        return jsonify({"cities": sorted(list(G.nodes))}), 200
    except Exception as e:
        print("⚠️ /api/cities error:", e)
        return jsonify({"cities": []}), 500


@app.route("/api/path", methods=["POST"])
def shortest_path():
    try:
        data = request.get_json()
        source = data.get("source")
        target = data.get("destination")

        if not source or not target:
            return jsonify({"status": "error", "message": "Missing source or destination"}), 400

        path, total_time = find_shortest_path(G, source, target)
        if path is None:
            return jsonify({"status": "error", "message": "No path found"}), 404

        return jsonify({
            "status": "success",
            "path": path,
            "total_time": total_time,
            "unit": "hours"
        }), 200
    except Exception as e:
        print("⚠️ /api/path error:", e)
        return jsonify({"status": "error", "message": "Server error"}), 500


@app.route("/api/ai_insight", methods=["POST"])
def ai_insight():
    """
    Route-wise travel insights for ALL cities in the shortest path
    (places to visit + famous food)
    """
    try:
        data = request.get_json()
        route = data.get("route", [])

        if not route or len(route) < 2:
            return jsonify({
                "status": "error",
                "message": "Invalid route"
            }), 400

        # 🔹 City-wise insights (covers ALL nodes)
        city_insights = {
            "Ballari, Karnataka, India": {
                "places": ["Hampi (nearby)", "Bellary Fort"],
                "food": ["Jolada Rotti", "North Karnataka Meals"]
            }, 
            "Hospet, Karnataka, India": {
                "places": ["Hampi", "Tungabhadra Dam"],
                "food": ["Bisi Bele Bath", "South Indian Thali"]
            },
            "Hubballi, Karnataka, India": {
                "places": ["Unkal Lake", "Chandramouleshwara Temple"],
                "food": ["Dharwad Peda", "North Karnataka Cuisine"]
            },
            "Bengaluru, Karnataka, India": {
                "places": ["Lalbagh", "Cubbon Park", "Bangalore Palace"],
                "food": ["Masala Dosa", "Bisi Bele Bath"]
            },
            "Hyderabad, Telangana, India": {
                "places": ["Charminar", "Golconda Fort", "Hussain Sagar"],
                "food": ["Hyderabadi Biryani", "Haleem"]
            },
            "Kurnool, Andhra Pradesh, India": {
                "places": ["Belum Caves", "Konda Reddy Fort"],
                "food": ["Rayalaseema Spicy Curry"]
            },
            "Chitradurga, Karnataka, India": {
                "places": ["Chitradurga Fort"],
                "food": ["Akki Rotti"]
            },
            "Chennai, Tamil Nadu, India": {
                "places": ["Marina Beach", "Kapaleeshwarar Temple"],
                "food": ["Idli", "Dosa", "Filter Coffee"]
            },
            "Kochi, Kerala, India": {
                "places": ["Fort Kochi", "Chinese Fishing Nets"],
                "food": ["Kerala Sadya", "Seafood"]
            },
            "Thiruvananthapuram, Kerala, India": {
                "places": ["Padmanabhaswamy Temple", "Kovalam Beach"],
                "food": ["Appam", "Stew"]
            },
            "Visakhapatnam, Andhra Pradesh, India": {
                "places": ["RK Beach", "Kailasagiri"],
                "food": ["Andhra Fish Curry"]
            },
            "Mumbai, Maharashtra, India": {
                "places": ["Gateway of India", "Marine Drive"],
                "food": ["Vada Pav", "Pav Bhaji"]
            },
            "Pune, Maharashtra, India": {
                "places": ["Shaniwar Wada", "Sinhagad Fort"],
                "food": ["Misal Pav"]
            },
            "Ahmedabad, Gujarat, India": {
                "places": ["Sabarmati Ashram", "Kankaria Lake"],
                "food": ["Dhokla", "Thepla"]
            },
            "New Delhi, India": {
                "places": ["India Gate", "Qutub Minar"],
                "food": ["Chole Bhature", "Parathas"]
            },
            "Jaipur, Rajasthan, India": {
                "places": ["Hawa Mahal", "Amber Fort"],
                "food": ["Dal Baati Churma"]
            },
            "Lucknow, Uttar Pradesh, India": {
                "places": ["Bara Imambara"],
                "food": ["Lucknowi Biryani", "Kebabs"]
            },
            "Kolkata, West Bengal, India": {
                "places": ["Victoria Memorial", "Howrah Bridge"],
                "food": ["Rosogolla", "Fish Curry"]
            },
            "Bhubaneswar, Odisha, India": {
                "places": ["Lingaraj Temple"],
                "food": ["Dalma"]
            },
            "Patna, Bihar, India": {
                "places": ["Golghar"],
                "food": ["Litti Chokha"]
            },
            "Indore, Madhya Pradesh, India": {
                "places": ["Rajwada Palace"],
                "food": ["Poha", "Jalebi"]
            },
            "Nagpur, Maharashtra, India": {
                "places": ["Deekshabhoomi"],
                "food": ["Saoji Cuisine"]
            },
            "Guwahati, Assam, India": {
                "places": ["Kamakhya Temple"],
                "food": ["Assamese Thali"]
            },
            "Tirupati, Andhra Pradesh, India": {
                "places": ["Tirumala Temple"],
                "food": ["Laddu Prasadam"]
            },
            "Amritsar, Punjab, India": {
                "places": ["Golden Temple"],
                "food": ["Amritsari Kulcha"]
            },
            "Surat, Gujarat, India": {
                "places": ["Dumas Beach"],
                "food": ["Surti Locho"]
            },
            "Vadodara, Gujarat, India": {
                "places": ["Laxmi Vilas Palace"],
                "food": ["Gujarati Thali"]
            },
            "Nashik, Maharashtra, India": {
                "places": ["Trimbakeshwar Temple"],
                "food": ["Misal"]
            },
            "Bhopal, Madhya Pradesh, India": {
                "places": ["Upper Lake"],
                "food": ["Bhopali Gosht"]
            },
            "Kanpur, Uttar Pradesh, India": {
                "places": ["Allen Forest Zoo"],
                "food": ["Street Chaat"]
            },
            "Varanasi, Uttar Pradesh, India": {
                "places": ["Ghats of Ganga"],
                "food": ["Kachori Sabzi"]
            },
            "Coimbatore, Tamil Nadu, India": {
                "places": ["Marudhamalai Temple"],
                "food": ["Kongu Cuisine"]
            },
            "Madurai, Tamil Nadu, India": {
                "places": ["Meenakshi Temple"],
                "food": ["Jigarthanda"]
            },
            "Vijayawada, Andhra Pradesh, India": {
                "places": ["Kanaka Durga Temple"],
                "food": ["Andhra Meals"]
            },
            "Kozhikode, Kerala, India": {
                "places": ["Kappad Beach"],
                "food": ["Malabar Biryani"]
            },
            "Chandigarh, India": {
                "places": ["Rock Garden"],
                "food": ["Punjabi Thali"]
            },
            "Srinagar, Jammu and Kashmir, India": {
                "places": ["Dal Lake"],
                "food": ["Rogan Josh"]
            },
            "Leh, Ladakh, India": {
                "places": ["Pangong Lake"],
                "food": ["Thukpa"]
            },
            "Panaji, Goa, India": {
                "places": ["Miramar Beach"],
                "food": ["Goan Fish Curry"]
            },
            "Mangalore, Karnataka, India": {
                "places": ["Panambur Beach"],
                "food": ["Seafood"]
            },
            "Mysuru, Karnataka, India": {
                "places": ["Mysore Palace"],
                "food": ["Mysore Pak"]
            },
            "Agra, Uttar Pradesh, India": {
                "places": ["Taj Mahal"],
                "food": ["Petha"]
            },
            "Ranchi, Jharkhand, India": {
                "places": ["Dassam Falls"],
                "food": ["Rice-based Dishes"]
            },
            "Raipur, Chhattisgarh, India": {
                "places": ["Nandan Van Zoo"],
                "food": ["Chhattisgarhi Thali"]
            },
            "Dehradun, Uttarakhand, India": {
                "places": ["Robber’s Cave"],
                "food": ["Garhwali Cuisine"]
            },
            "Shimla, Himachal Pradesh, India": {
                "places": ["Mall Road"],
                "food": ["Himachali Dham"]
            }
        }

        insight_text = "🛣️ Overall Shortest Path Travel Insights\n\n"

        for city in route:
            info = city_insights.get(city)
            if info:
                insight_text += f"📍 {city}\n"
                insight_text += "⭐ Places to Visit:\n"
                for p in info["places"]:
                    insight_text += f"• {p}\n"
                insight_text += "🍴 Famous Food:\n"
                for f in info["food"]:
                    insight_text += f"• {f}\n"
                insight_text += "\n"

        return jsonify({
            "status": "success",
            "insight": insight_text
        }), 200

    except Exception as e:
        print("⚠️ /api/ai_insight error:", e)
        return jsonify({
            "status": "error",
            "message": "Insight generation failed"
        }), 500




if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

