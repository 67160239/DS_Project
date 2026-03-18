# 📚 Comic Rating Predictor System
**Project สำหรับวิชา Machine Learning Deployment**

แอปพลิเคชันสำหรับพยากรณ์คะแนนเรตติ้งของการ์ตูน (0-10) โดยวิเคราะห์จากปัจจัยพื้นฐาน เช่น แนวเรื่อง, จำนวนหน้า, และปีที่วางจำหน่าย เพื่อช่วยให้นักเขียนหรือสำนักพิมพ์ประเมินแนวโน้มความนิยมล่วงหน้า

---

## 🌐 เข้าใช้งานแอปพลิเคชัน
👉 **[คลิกที่นี่เพื่อเปิดหน้าเว็บ Streamlit](https://dsproject-ep2sgccopjin5flft7t9ud.streamlit.app/)**

---

## 🧐 1. การนิยามปัญหา (Problem Definition)
ในปัจจุบันอุตสาหกรรมการ์ตูนมีการแข่งขันสูงมาก ปัญหาคือเราจะรู้ได้อย่างไรว่าการ์ตูนที่สร้างขึ้นมีโอกาสประสบความสำเร็จแค่ไหน? 
- **เป้าหมาย:** สร้างโมเดลที่สามารถทำนายคะแนนเรตติ้ง (Regression) จากข้อมูล Metadata
- **ทำไมต้องใช้ ML?:** เนื่องจากปัจจัยที่มีผลต่อคะแนนมีความซับซ้อนและสัมพันธ์กันในหลายมิติ ML จึงสามารถช่วยหา Pattern จากสถิติในอดีตได้ดีกว่าการคาดเดาด้วยคน

## 📊 2. ข้อมูลที่ใช้ (Dataset & EDA)
- **แหล่งที่มา:** [https://www.kaggle.com/datasets/rudrakumargupta/comic-books-dataset-10000-entries]
- **Insights ที่พบ:**
  - แนวการ์ตูน (Genre) บางประเภท เช่น [Sci-Fi] มีแนวโน้มได้เรตติ้งสูงกว่าปกติ

## 🤖 3. การพัฒนาโมเดล (Model Development)
- **Algorithm:** [Random Forest Regressor, GradientBoosting Regressor]
- **Preprocessing:** ใช้ `Pipeline` ในการจัดการข้อมูล (Imputer, Scaler, OneHotEncoder)
- **Random Forest:** - $R^2$ Score: [-0.0187]
- **GradientBoosting:** - $R^2$ Score: [-0.0187]

## 🛠️ 4. การจัดการปัญหาทางเทคนิค (Technical Challenges)
ในการ Deployment ครั้งนี้ได้พบปัญหา **Version Mismatch** ระหว่าง Google Colab และ Streamlit Cloud:
- **Solution:** แก้ไขโดยการทำ Environment Pinning ผ่านไฟล์ `requirements.txt` และกำหนดเวอร์ชัน Python 3.11 ผ่านไฟล์ `.python-version` เพื่อให้โครงสร้างโมเดลทำงานได้อย่างถูกต้อง

## 📁 โครงสร้าง Repository
- `app.py`: โค้ดหลักของ Streamlit UI
- `best_comic_model.pkl`: โมเดลที่ผ่านการ Train และ Tuning แล้ว
- `requirements.txt`: รายการ Library ที่จำเป็น
- `.python-version`: ไฟล์กำหนดเวอร์ชัน Python สำหรับ Cloud
