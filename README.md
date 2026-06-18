# 👁️ AI-Based Missing Person Detection System 

![System Status](https://img.shields.io/badge/System-Active-00ffcc.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Flask-Web_Framework-black)
![AI](https://img.shields.io/badge/DeepFace-ArcFace-orange)
![CV](https://img.shields.io/badge/OpenCV-Tracking-green)

**Transforming passive surveillance into proactive public safety.**

Thousands go missing annually, and authorities cannot manually monitor every single camera feed. The **Surveillance Core v5.0** is an intelligent, automated AI intervention designed to replace hours of manual tape review with instant, millisecond frame matching. It is specifically built for high-traffic, controlled environments like airports, railway stations, and secure venues.

---

## 🚀 Key Features

* **Real-Time Live Tracking (Zero-Lag):** Utilizes a hybrid detection approach. It uses ultra-fast Haar Cascades for frame-by-frame object tracking and triggers heavy AI recognition (DeepFace) at specific intervals to ensure a smooth **30 FPS** video feed.
* **"1-Person-1-Slot" Smart Dashboard:** A professional Cyber-Security UI that prevents log spamming. If a target is identified, it captures their *real-time* face crop and updates their unique slot in the sidebar.
* **High-Accuracy Distance Calculation:** Uses 128-Dimensional vector encoding via the **ArcFace** model with a strict confidence threshold to eliminate false positives.
* **Centroid Drag & Track Algorithm:** The system pins the identification tag to the moving target's face, ensuring the bounding box and name tag magnetically stick to the person as they move across the frame.
* **Database & Memory Management:** Built-in SQLite database with overwrite logic and cooldown memory to prevent database bloating while securing identification logs.

---

## 🧠 System Architecture

The MVP System Architecture is built on a streamlined, zero-friction pipeline:

1.  **Frontend UI:** HTML5, CSS3, Vanilla JS (Cyberpunk Command Center theme designed for high-stress security environments).
2.  **Backend API:** Python (Flask) for data processing and video feed routing.
3.  **AI Engine:** OpenCV (Spatial mapping) + DeepFace (Dense numerical data encoding & Recognition).
4.  **Database:** SQLite3 for secure storage of profiles and alert logs.

---

## ⚙️ Installation & Setup

Follow these steps to run the Surveillance Core on your local machine.

### 1. Prerequisites
Ensure you have Python 3.8+ installed. 

### 2. Clone the Repository
```bash
git clone [https://github.com/YourUsername/ai-surveillance-system.git](https://github.com/YourUsername/ai-surveillance-system.git)
cd ai-surveillance-system
3. Create a Virtual Environment (Recommended)
Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
4. Install Dependencies
Bash
pip install -r requirements.txt
5. Run the System
Bash
python app.py
The system will automatically create the reference_images folder and surveillance.db file upon the first run.

💻 Usage Instructions
Access the Dashboard: Open your browser and go to http://127.0.0.1:5000.

Register a Target: Click on + SYNC NEW TARGET in the header. Upload a clear, front-facing image of the missing person and enter their name.

Monitor Live Feed: Return to the main dashboard. As soon as the registered person steps into the camera frame, the system will instantly identify them, draw a tracking box, and log their real-time snapshot in the sidebar with a confidence score.

🛡️ Ethics & Limitations
Privacy: System is designed to be restricted to controlled environments and authorized law enforcement personnel only.

Data Security: Relies on mathematical encodings (vectors) rather than raw images for its core querying key.

Human-in-the-Loop: System serves as an alert tool requiring human verification for final action due to potential accuracy drops in extreme occlusions.

Academic Project by: Team at LNCT, Bhopal.


***

### README ko GitHub par Push Kaise Karein?

1. Apne VS Code mein ek nayi file banayein: `README.md`
2. Upar wala pura text usme paste karke save karein. *(Dhyan rahe, 'YourUsername' ki jagah apna GitHub username daal dijiyega Clone section mein)*.
3. VS Code terminal mein ye run karein:
   ```bash
   git add README.md
   git commit -m "Added Project README"
   git push
