from flask import Flask, render_template, Response, jsonify, request
import cv2, os, sqlite3, base64, time
from datetime import datetime
from deepface import DeepFace

app = Flask(__name__)

# --- CONFIG ---
UPLOAD_FOLDER = "reference_images"
DB_FILE = "surveillance.db"
THRESHOLD = 0.45  # Accuracy Threshold
AI_PROCESS_INTERVAL = 15 # Har 15ve frame par AI chalega, video ekdum smooth chalegi

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

# Fast Detector for tracking
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time TEXT, conf TEXT, captured_img TEXT)''')
    conn.commit(); conn.close()

init_db()

def generate_frames():
    global last_seen
    cap = cv2.VideoCapture(0)
    frame_count = 0
    
    # Active targets ki memory banayenge taaki box drag ho sake
    active_targets = [] 

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. FAST DETECTION: Har frame par chalega (No Lag)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

        # 2. HEAVY AI RECOGNITION: Har 15th frame par chalega
        if frame_count % AI_PROCESS_INTERVAL == 0:
            try:
                # DeepFace saare faces ek sath detect karke list of DataFrames return karta hai
                results = DeepFace.find(img_path=frame, db_path=UPLOAD_FOLDER, model_name="ArcFace", 
                                        detector_backend="opencv", enforce_detection=False, silent=True)

                new_targets = []
                # Multiple faces handle karne ke liye loop
                for res_df in results:
                    if not res_df.empty:
                        match = res_df.iloc[0]
                        dist = match['distance']
                        if dist < THRESHOLD:
                            name = os.path.basename(match['identity']).split('.')[0].replace('_', ' ')
                            x, y, w, h = int(match['source_x']), int(match['source_y']), int(match['source_w']), int(match['source_h'])
                            conf = f"{round((1 - dist) * 100)}%"
                            
                            # Face ka center point (Centroid) nikalenge tracking ke liye
                            cx, cy = x + w//2, y + h//2
                            new_targets.append({"name": name, "conf": conf, "box": (x,y,w,h), "center": (cx,cy)})
                            
                            # DB Logging Logic
                            curr_time = time.time()
                            if name not in last_seen or (curr_time - last_seen[name]) > COOLDOWN:
                                last_seen[name] = curr_time
                                face_crop = frame[y:y+h, x:x+w]
                                _, buffer = cv2.imencode('.jpg', face_crop)
                                img_b64 = base64.b64encode(buffer).decode('utf-8')
                                
                                conn = sqlite3.connect(DB_FILE)
                                conn.execute("INSERT INTO logs (name, time, conf, captured_img) VALUES (?, ?, ?, ?)", 
                                             (name, datetime.now().strftime("%I:%M:%S %p"), conf, img_b64))
                                conn.commit(); conn.close()
                
                # Naye recognized targets ko memory mein save karo
                if new_targets:
                    active_targets = new_targets

            except Exception: pass

        # 3. SMOOTH DRAG LOGIC (Centroid Tracking)
        # Naye fast bounding boxes ko purane identified naam ke sath jodein
        for (hx, hy, hw, hh) in faces:
            hcx, hcy = hx + hw//2, hy + hh//2 # Current face ka center
            
            matched_target = None
            min_dist = float('inf')

            # Sabse kareeb (closest) identified face dhoondho
            for target in active_targets:
                tcx, tcy = target['center']
                # Calculate Distance using Math
                dist = ((hcx - tcx)**2 + (hcy - tcy)**2)**0.5 
                
                if dist < 120: # Agar face pichle frame se zyada door nahi gaya hai
                    if dist < min_dist:
                        min_dist = dist
                        matched_target = target
            
            if matched_target:
                # Target ki memory update karo taaki box uske sath-sath chal sake
                matched_target['center'] = (hcx, hcy)
                
                # Box aur Naam Draw karo
                cv2.rectangle(frame, (hx, hy), (hx+hw, hy+hh), (0, 255, 204), 2)
                cv2.putText(frame, f"{matched_target['name']} ({matched_target['conf']})", 
                            (hx, hy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 204), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
    cap.release()

# --- ROUTES ---
@app.route('/')
def index(): return render_template('index.html')

@app.route('/video_feed')
def video_feed(): return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_logs')
def get_logs():
    try:
        conn = sqlite3.connect(DB_FILE)
        query = """
        SELECT name, time, conf, captured_img 
        FROM logs 
        WHERE id IN (SELECT MAX(id) FROM logs GROUP BY name) 
        ORDER BY id DESC
        """
        data = conn.execute(query).fetchall()
        conn.close()
        return jsonify([{"name": d[0], "time": d[1], "conf": d[2], "img": d[3]} for d in data])
    except: return jsonify([])

@app.route('/register_page')
def register_page(): return render_template('register.html')

@app.route('/register_face', methods=['POST'])
def register():
    file = request.files.get('photo'); name = request.form.get('name')
    if file and name:
        path = os.path.join(UPLOAD_FOLDER, f"{name.replace(' ','_')}.jpg")
        file.save(path)
        for f in os.listdir(UPLOAD_FOLDER):
            if f.endswith(".pkl"): os.remove(os.path.join(UPLOAD_FOLDER, f))
        return jsonify({"status": "success", "message": f"{name} Synced!"})
    return jsonify({"status": "error"})

# COOLDOWN MEMORY
last_seen = {}
COOLDOWN = 30

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)