import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ (UX/UI หมวด 4)
st.set_page_config(page_title="Comic Rating Predictor", page_icon="📚", layout="wide")

# 2. เตรียม Session State สำหรับเก็บตารางประวัติ (คะแนนโบนัส)
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. โหลดโมเดล
@st.cache_resource
def load_my_model():
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "best_comic_model.pkl")
    return joblib.load(model_path)

try:
    model = load_my_model()
except Exception as e:
    st.error(f"⚠️ ไม่สามารถโหลดโมเดลได้: {e}")
    st.stop()

# --- ส่วนแสดงผลหลัก ---
st.title("📚 ระบบพยากรณ์คะแนนการ์ตูน (Comic Predictor)")
st.markdown("กรอกข้อมูลเพื่อทำนายเรตติ้งที่น่าจะได้ โดยใช้โมเดล **Gradient Boosting**")

# แบ่งหน้าจอเป็น 2 ฝั่ง: ซ้ายสำหรับกรอก / ขวาสำหรับโชว์ผลและประวัติ
col_input, col_display = st.columns([1, 1.5], gap="large")

with col_input:
    with st.form("comic_form"):
        st.subheader("📝 กรอกข้อมูลการ์ตูน")
        
        year = st.number_input("📅 ปีที่วางจำหน่าย", 1900, 2026, 2024)
        pages = st.number_input("📄 จำนวนหน้า", 1, 2000, 150)
        vols = st.number_input("📦 จำนวนเล่ม", 1, 500, 1)
        genre = st.selectbox("🎭 แนวการ์ตูน", ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Sci-Fi'])
        fmt = st.selectbox("📦 รูปแบบ", ['Hardcover', 'Paperback', 'Digital'])
        theme = st.selectbox("🎨 สไตล์สี", ['Full Color', 'Black and White'])
        lang = st.selectbox("🗣️ ภาษา", ['English', 'Thai', 'Japanese'])
        age = st.selectbox("🔞 เรตอายุ", ['Everyone', 'Teen', 'Adults Only 18+'])
        
        # ข้อมูลคงที่
        country = "USA"
        status = "Ongoing"
        
        submit = st.form_submit_button("🚀 เริ่มทำนายผล")

with col_display:
    if submit:
        # เตรียมข้อมูล
        input_data = pd.DataFrame({
            'Release Year': [year], 'Page Count': [pages], 'Volume Count': [vols],
            'Format': [fmt], 'Theme (Color Style)': [theme], 'Genre': [genre],
            'Country of Origin': [country], 'Status': [status], 'Language': [lang], 'Age Rating': [age]
        })
        
        # ทำนายผล
        prediction = model.predict(input_data)[0]
        final_score = max(0, min(10, round(float(prediction), 2)))
        
        # แสดงผลลัพธ์ปัจจุบัน
        st.subheader("🎯 ผลการทำนาย")
        st.metric(label="Predicted Rating", value=f"{final_score} / 10")
        st.progress(final_score / 10)
        
        if final_score >= 7:
            st.success("🌟 มีแนวโน้มได้รับความนิยมสูง!")
        else:
            st.info("👍 อยู่ในเกณฑ์มาตรฐาน")

        # --- บันทึกประวัติลงตาราง (คะแนนโบนัส) ---
        new_record = {
            "เวลา": datetime.now().strftime("%H:%M:%S"),
            "แนวเรื่อง": genre,
            "หน้า": pages,
            "เล่ม": vols,
            "เรตติ้งที่ทาย": final_score
        }
        st.session_state.history.append(new_record)

    # 4. แสดงตารางประวัติ (Prediction History Table)
    st.divider()
    st.subheader("📜 ตารางเปรียบเทียบประวัติการทำนาย")
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.table(history_df) # หรือ st.dataframe(history_df)
        
        if st.button("🗑️ ล้างข้อมูลในตาราง"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("ยังไม่มีข้อมูลประวัติการทำนาย")

# --- Footer (Disclaimer) ---
st.divider()
st.caption("💡 Disclaimer: ข้อมูลนี้เป็นเพียงการวิเคราะห์ทางสถิติเพื่อการศึกษาเท่านั้น | พัฒนาโดย AAI Student")