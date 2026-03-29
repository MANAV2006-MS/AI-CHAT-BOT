from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neno-gym-beast-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neno_gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- DATABASE MODEL ---------------- #
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_msg = db.Column(db.Text, nullable=False)
    bot_reply = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(36), index=True)


# ---------------- AI COACH ---------------- #
class NenoGymCoach:
    def __init__(self):
        self.sessions = {}

        # 📚 KNOWLEDGE BASE
        self.knowledge = {

            "beginner_plan": """🏋️ BEGINNER PLAN:
• Full Body – 3x/week

Day Plan:
1. Squat – 3x10
2. Bench Press – 3x10
3. Lat Pulldown – 3x12
4. Shoulder Press – 3x10
5. Plank – 3x30 sec

Progress weekly ↑ weight""",

            "push_day": """🔥 PUSH DAY (Chest + Shoulders + Triceps):
1. Bench Press – 4x8
2. Incline Dumbbell Press – 3x10
3. Shoulder Press – 3x10
4. Lateral Raise – 3x15
5. Tricep Pushdown – 3x12""",

            "pull_day": """💪 PULL DAY (Back + Biceps):
1. Pull-ups / Lat Pulldown – 4x8-12
2. Barbell Row – 3x10
3. Cable Row – 3x12
4. Face Pull – 3x15
5. Bicep Curl – 3x12""",

            "leg_day": """🦵 LEG DAY:
1. Squat – 4x6-8
2. Romanian Deadlift – 3x10
3. Leg Press – 3x12
4. Hamstring Curl – 3x12
5. Calf Raises – 5x20""",

            "nutrition": """🍗 NUTRITION BASICS:
• Protein: 1.6–2g per kg bodyweight
• Carbs: Rice, oats
• Fats: Nuts, eggs
• Water: 3–4L/day

Bulk → calorie surplus  
Cut → calorie deficit""",

            "fat_loss": """🔥 FAT LOSS:
• 500 calorie deficit
• HIIT 2–3x/week
• Steps: 8k–12k/day
• High protein diet""",

            "muscle_gain": """💪 MUSCLE GAIN:
• Calorie surplus +300–500
• Progressive overload
• 8–12 reps ideal
• Sleep = growth""",

            "recovery": """😴 RECOVERY:
• Sleep: 7–9 hours
• Rest days: 1–2/week
• Stretch + mobility
• Avoid overtraining""",

            "mistakes": """❌ COMMON MISTAKES:
• Ego lifting
• Skipping legs
• No progressive overload
• Bad diet
• Inconsistency""",

            "warmup": """🔥 WARMUP:
• 5–10 min cardio
• Dynamic stretching
• Light sets before heavy lifts"""
        }

    def get_reply(self, message, session_id="guest"):
        session_id = str(session_id)
        lower_msg = message.lower()

        if session_id not in self.sessions:
            self.sessions[session_id] = {"count": 0}

        self.sessions[session_id]["count"] += 1

        # 🧠 SMART RESPONSE LOGIC
        if any(x in lower_msg for x in ["beginner", "start", "new"]):
            return self.knowledge["beginner_plan"]

        elif "push" in lower_msg:
            return self.knowledge["push_day"]

        elif "pull" in lower_msg:
            return self.knowledge["pull_day"]

        elif "leg" in lower_msg:
            return self.knowledge["leg_day"]

        elif any(x in lower_msg for x in ["diet", "nutrition", "food"]):
            return self.knowledge["nutrition"]

        elif any(x in lower_msg for x in ["fat", "cut", "lose"]):
            return self.knowledge["fat_loss"]

        elif any(x in lower_msg for x in ["muscle", "bulk", "size"]):
            return self.knowledge["muscle_gain"]

        elif any(x in lower_msg for x in ["rest", "sleep", "recovery"]):
            return self.knowledge["recovery"]

        elif any(x in lower_msg for x in ["mistake", "wrong"]):
            return self.knowledge["mistakes"]

        elif "warmup" in lower_msg:
            return self.knowledge["warmup"]

        elif any(x in lower_msg for x in ["hi", "hello", "hey"]):
            return "💪 NENO COACH: Ready to build a beast physique?"

        else:
            return """💪 NENO COACH:
Ask me anything:
• workout plan
• push/pull/legs
• fat loss
• muscle gain
• diet"""


# ---------------- INIT BOT ---------------- #
neno = NenoGymCoach()


# ---------------- ROUTES ---------------- #
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    session_id = session['session_id']

    if request.method == 'POST':
        user_msg = request.form.get('message', '').strip()

        if user_msg and len(user_msg) <= 500:
            reply = neno.get_reply(user_msg, session_id)

            chat = Chat(
                user_msg=user_msg,
                bot_reply=reply,
                session_id=session_id
            )

            db.session.add(chat)
            db.session.commit()

        return redirect(url_for('index'))

    chats = Chat.query.filter_by(session_id=session_id)\
        .order_by(Chat.timestamp.desc()).limit(30).all()[::-1]

    return render_template('index.html', chats=chats)


@app.route('/clear')
def clear_chat():
    session_id = session.get('session_id')

    if session_id:
        Chat.query.filter_by(session_id=session_id).delete()
        db.session.commit()

    return redirect(url_for('index'))


# ---------------- RUN ---------------- #
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("💪 NENO GYM COACH - FULLY LOADED!")
    print("🌐 http://localhost:5000")
    app.run(debug=True, port=5000)