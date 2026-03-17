import streamlit as st
import pandas as pd
import joblib
import os

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Comic Predictor", layout="centered")

# 2. โหลดโมเดล (ปรับปรุงให้รองรับ Path บน Cloud)
@st.cache_resource
def load_my_model():
    # หาที่อยู่ของไฟล์ app.py แล้วไปดึงไฟล์โมเดลที่อยู่ในที่เดียวกัน
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "best_comic_model.pkl")
    return joblib.load(model_path)

# พยายามโหลดโมเดล ถ้า Error จะโชว์แจ้งเตือนที่เข้าใจง่าย
try:
    model = load_my_model()
except Exception as e:
    st.error(f"ไม่สามารถโหลดโมเดลได้: {e}")
    st.stop()

# 3. ส่วน UI
st.title("📚 ระบบพยากรณ์คะแนนการ์ตูน")
st.write("กรอกข้อมูลการ์ตูนเพื่อทำนายเรตติ้งที่น่าจะได้ (0-10)")

with st.form("comic_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.number_input("ปีที่วางจำหน่าย", 1900, 2026, 2024)
        pages = st.number_input("จำนวนหน้า", 1, 2000, 150)
        vols = st.number_input("จำนวนเล่ม", 1, 500, 1)
        genre = st.selectbox("แนวการ์ตูน", ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Sci-Fi'])
        
    with col2:
        fmt = st.selectbox("รูปแบบ", ['Hardcover', 'Paperback', 'Digital'])
        theme = st.selectbox("สไตล์สี", ['Full Color', 'Black and White'])
        lang = st.selectbox("ภาษา", ['English', 'Thai', 'Japanese'])
        age = st.selectbox("เรตอายุ", ['Everyone', 'Teen', 'Adults Only 18+'])
    
    country = "USA"
    status = "Ongoing"
    submit = st.form_submit_button("เริ่มทำนายผล")

if submit:
    input_data = pd.DataFrame({
        'Release Year': [year], 'Page Count': [pages], 'Volume Count': [vols],
        'Format': [fmt], 'Theme (Color Style)': [theme], 'Genre': [genre],
        'Country of Origin': [country], 'Status': [status], 'Language': [lang], 'Age Rating': [age]
    })
    
    prediction = model.predict(input_data)[0]
    
    st.success(f"### ผลการทำนาย: {prediction:.2f} คะแนน")
    st.progress(min(max(prediction / 10, 0.0), 1.0)) # กัน Error ถ้าคะแนนเกิน 10
    st.info("💡 หมายเหตุ: ผลการทำนายนี้คำนวณจากสถิติในอดีตเท่านั้น")