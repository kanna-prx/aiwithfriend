from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# คลังข้อสอบจำลอง (ดึงมาจากข้อสอบคณิตศาสตร์ประยุกต์ 1 มี.ค. 68)
exam_bank = {
    "q1": {
        "subject": "Math",
        "topic": "Set Theory",
        "text": "ให้เซต A = {∅, √2} แล้วเซต P(P(A)) ∪ P(A) มีสมาชิกกี่ตัว?",
        "choices": ["10", "16", "18", "19", "20"],
        "answer": 2 # Index 2 คือ "18"
    }
}

@app.route('/')
def index():
    # ส่งหน้า HTML ไปแสดงผล
    return render_template('index.html')

@app.route('/api/get_question', methods=['GET'])
def get_question():
    # ดึงข้อสอบไปแสดงผลที่หน้าเว็บ
    q = exam_bank["q1"]
    return jsonify({"id": "q1", "text": q["text"], "choices": q["choices"]})

@app.route('/api/submit', methods=['POST'])
def submit_answer():
    data = request.json
    user_answer = data.get("answer")
    
    # ตรวจคำตอบ
    is_correct = (user_answer == exam_bank["q1"]["answer"])
    
    # AI จำลองการอธิบายและคำนวณโอกาสติดมหาลัย
    ai_explanation = ""
    if is_correct:
        ai_explanation = "สุดยอด! คุณเข้าใจคอนเซปต์ของเพาเวอร์เซต A มีสมาชิก 2 ตัว P(A) มี 4 ตัว และ P(P(A)) มี 16 ตัว เมื่อนำมา Union กัน สมาชิกที่ซ้ำกันมี 2 ตัว จึงได้ 16 + 4 - 2 = 18 ตัว"
    else:
        ai_explanation = "เกือบไปแล้ว! ก่อนดูเฉลย ลองทบทวนสูตรจำนวนสมาชิก n(A U B) = n(A) + n(B) - n(A ∩ B) ดูก่อนนะ สมาชิกที่หน้าตาซ้ำกันนับเป็น 1 ตัว"

    # สมมติระบบวิเคราะห์คะแนนและโอกาสแอดมิชชั่น
    stats = {
        "score": 100 if is_correct else 0,
        "radar_data": [85, 90, 40, 60, 75], # สมมติคะแนนแต่ละบทเรียน
        "admission_chance": "85% (คณะวิศวกรรมศาสตร์ ม.เป้าหมาย)" if is_correct else "45% (ต้องเน้นเรื่องเซตเพิ่มเติม)"
    }
    
    return jsonify({
        "correct": is_correct,
        "explanation": ai_explanation,
        "stats": stats
    })

if __name__ == '__main__':
    app.run(debug=True)