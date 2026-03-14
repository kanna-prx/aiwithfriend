import streamlit as st
import fitz
import json
import google.generativeai as genai
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --- 1. ตั้งค่าหน้าแอป ---
st.set_page_config(page_title="AI Exam Tutor", layout="wide")

# --- 2. ตั้งค่า API ---
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. ฟังก์ชันการคำนวณและประมวลผล ---
def process_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc[:5]: 
        text += page.get_text()
    
    prompt = f"""
    จากข้อสอบคณิตศาสตร์นี้: {text}
    จงสกัดข้อสอบแบบปรนัย 3 ข้อ ออกมาเป็น JSON format:
    [{{
        "question": "โจทย์...",
        "choices": ["ตัวเลือก 1", "2", "3", "4"],
        "correct": 0,
        "topic": "ชื่อบทเรียน",
        "explanation": "เฉลยละเอียด"
    }}]
    ตอบเฉพาะ JSON เท่านั้น
    """
    
    response = model.generate_content(prompt)
    try:
        res_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(res_text)
    except:
        return None

def plot_strength_chart(scores_dict):
    if not scores_dict: return
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='คะแนนรายบท'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    st.plotly_chart(fig)

# --- 4. ส่วนแสดงผล UI ---
st.title("🎓 AI คลังข้อสอบ & วิเคราะห์โอกาสสอบติด")

if 'questions' not in st.session_state:
    st.session_state['questions'] = []
if 'user_results' not in st.session_state:
    st.session_state['user_results'] = {}

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. คลังข้อสอบ")
    uploaded_file = st.file_uploader("อัปโหลดข้อสอบ PDF", type="pdf")
    if uploaded_file and st.button("วิเคราะห์ข้อสอบด้วย AI"):
        with st.spinner("AI กำลังอ่านไฟล์..."):
            questions = process_pdf(uploaded_file.read())
            st.session_state['questions'] = questions
            st.success(f"โหลดได้ {len(questions)} ข้อ!")

with col2:
    st.header("2. สนามสอบจำลอง")
    if st.session_state['questions']:
        score_count = 0
        for i, q in enumerate(st.session_state['questions']):
            st.subheader(f"ข้อที่ {i+1}")
            st.write(q['question'])
            user_choice = st.radio("เลือกคำตอบ:", q['choices'], key=f"radio_{i}")
            
            if st.button(f"ส่งคำตอบข้อ {i+1}", key=f"btn_{i}"):
                correct_idx = q['correct']
                if q['choices'].index(user_choice) == correct_idx:
                    st.success("ถูกต้อง!")
                    topic = q['topic']
                    st.session_state['user_results'][topic] = st.session_state['user_results'].get(topic, 0) + 100
                else:
                    st.error("ยังไม่ถูกลองดูใหม่นะ")
                    tutor_prompt = f"โจทย์: {q['question']} นักเรียนตอบผิดโดยเลือก {user_choice} ช่วยใบ้ให้เขากลับไปคิดใหม่"
                    hint = model.generate_content(tutor_prompt)
                    st.info(f"💡 คำใบ้จาก AI: {hint.text}")

# --- 5. สรุปผลและกราฟ ---
st.divider()
st.header("3. แดชบอร์ดวิเคราะห์ผล")
if st.session_state['user_results']:
    c1, c2 = st.columns(2)
    with c1:
        st.write("### จุดแข็ง-จุดอ่อนรายบท")
        plot_strength_chart(st.session_state['user_results'])
    
    with c2:
        st.write("### ประเมินโอกาสสอบติด")
        target_major = st.selectbox("เลือกคณะเป้าหมาย", ["วิศวะ จุฬาฯ (เกณฑ์ 75)", "วิทยาศาสตร์ มธ. (เกณฑ์ 55)"])
        avg_score = sum(st.session_state['user_results'].values()) / len(st.session_state['user_results'])
        
        threshold = 75 if "จุฬา" in target_major else 55
        chance = "สูง" if avg_score >= threshold else "ต้องพยายามอีก"
        
        st.metric("คะแนนเฉลี่ยของคุณ", f"{avg_score:.2f}%")
        st.write(f"โอกาสสอบติดคณะนี้: **{chance}**")
