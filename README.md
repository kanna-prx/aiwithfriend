# The Pro Duck: Your AI-Powered Exam Companion
**"Don't just wing it, be a Pro Duck!"** The Pro Duck is an intelligent web application designed to transform static PDF exams into interactive learning experiences. Powered by **Google Gemini 2.5 Flash**, this tool acts as a personal tutor that helps you master your studies through smart hints and strategic analytics.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aiwithfriend-6icuhll2uhv8uf68twe2pc.streamlit.app/)

---

## 🌟 Why "The Pro Duck"?

In the world of programming, "Rubber Duck Debugging" is a famous technique. **The Pro Duck** takes it to the next level by talking back! It helps students navigate through tough exam questions by providing guidance rather than just answers.

## ✨ Key Features

* **📄 Pro-Parsing:** Automatically extracts questions and choices from PDF exam papers.
* **💡 Quack-Hints:** Get 1-2 sentence clues to nudge you in the right direction when you're stuck.
* **🚀 Duck-Tricks:** Exclusive exam-taking strategies and "shortcuts" provided by AI for each topic.
* **📊 Radar Analytics:** A "Pro Duck" view of your performance via Spider Charts to see exactly where you need to improve.
* **🌑 Sleek Dashboard:** Minimalist and fast UI built with Streamlit.

---

## 🛠️ Tech Stack

* **AI Engine:** Google Gemini API (2.5 Flash)
* **Web Framework:** Streamlit
* **PDF Engine:** PyMuPDF (fitz)
* **Data Viz:** Plotly & Pandas

---

## 🚀 Getting Started

1. **Clone the Repo**
   ```bash
   git clone [https://github.com/kanna-prx/aiwithfriend/blob/main/main.py]

2. **Install dependencies**

   Run this command to install all required libraries:
   ```bash
   pip install -r requirements.txt

3. **Configure Secrets**

   To keep the API Key secure, this project uses Streamlit's secrets management.

   #### 🌍 For Deployment (Streamlit Cloud):
   1. Go to your **App Dashboard** on Streamlit Cloud.
   2. Click on **Manage App** > **Settings** > **Secrets**.
   3. Paste the following line (replace with your actual key):
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"

4. **Run the application**

   To start **The Pro Duck** on your local machine, execute the following command in your terminal:
   ```bash
   streamlit run main.py
