# 🤖 AgentForge AI Engine - المحرك الذكي لتوليد التطبيقات

## ولّد تطبيقات كاملة من وصف نصي باستخدام الذكاء الاصطناعي

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Deployed on](https://img.shields.io/badge/Deployed%20on-Diploi-3B82F6)](https://diploi.com)

---

## 🚀 ما هو AgentForge؟

**AgentForge** هو خدمة API-as-a-Service تولد تطبيقات Streamlit كاملة وجاهزة للتشغيل من مجرد وصف نصي بسيط. وفر وقتك وتجنب كتابة الأكواد المكررة. فقط صف ما تريده، وAgentForge سيبنيها لك.

**جربه مباشرة:** [AgentForge على RapidAPI](https://rapidapi.com/abdullahreda1969/api/agentforge-ai-engine)

---

## ✨ الميزات

| الميزة                     | الوصف                                                  |
| -------------------------- | ------------------------------------------------------ |
| **🚀 قوالب ذكية**          | أسرع خيار، قوالب جاهزة للتطبيقات الشائعة               |
| **🦙 Ollama AI**           | توليد محلي بالذكاء الاصطناعي (بدون إنترنت، مجاني، خاص) |
| **☁️ Gemini AI**           | توليد سحابي بالذكاء الاصطناعي (قوي، سريع)              |
| **📦 تحميل فوري**          | احصل على ملف ZIP يحتوي على المشروع الكامل              |
| **🔧 قاعدة بيانات SQLite** | تخزين دائم لتطبيقاتك                                   |

---

## 🎯 أنواع التطبيقات المدعومة

| النوع            | الدوال                                                | مثال                         |
| ---------------- | ----------------------------------------------------- | ---------------------------- |
| **مدير مهام**    | `get_tasks()`, `add_task()`, `delete_task()`          | "تطبيق إدارة مهام"           |
| **دفتر عناوين**  | `get_contacts()`, `add_contact()`, `delete_contact()` | "دفتر عناوين بأرقام الهواتف" |
| **إدارة منتجات** | `get_products()`, `add_product()`, `delete_product()` | "نظام إدارة مخزون"           |
| **مدير مكتبة**   | `get_books()`, `add_book()`, `delete_book()`          | "نظام إدارة مكتبة"           |
| **آلة حاسبة**    | يولد ديناميكياً                                       | "تطبيق آلة حاسبة بسيط"       |

---

## 🏗️ كيف يعمل؟

المستخدم يرسل وصفاً
↓
AgentForge API (FastAPI)
↓
اختيار المحرك (قوالب / Ollama / Gemini)
↓
توليد الملفات (main.py, helpers.py, database.py, config.py)
↓
إرجاع رابط تحميل ZIP
↓
المستخدم يشغل: streamlit run main.py

text

---

## 📊 مقارنة المحركات الثلاثة

| المحرك             | السرعة            | الجودة     | إنترنت | التكلفة | الأفضل لـ            |
| ------------------ | ----------------- | ---------- | ------ | ------- | -------------------- |
| **القوالب الذكية** | ⚡ سريع جداً      | ⭐⭐⭐⭐   | ❌ لا  | مجاني   | الإنتاج              |
| **Ollama AI**      | 🐢 بطيء (30-90 ث) | ⭐⭐⭐⭐   | ❌ لا  | مجاني   | الاستخدام دون إنترنت |
| **Gemini AI**      | ⚡ سريع (5-15 ث)  | ⭐⭐⭐⭐⭐ | ✅ نعم | مجاني   | الإنتاج              |

---

## 🚀 البدء السريع (للاستخدام المحلي)

### المتطلبات الأساسية

- Python 3.11+
- Ollama (للمحرك المحلي)

### التثبيت

```bash
# نسخ المستودع
git clone https://github.com/abdullahreda1969/AgentForge-API.git
cd AgentForge-API

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الـ API
python run_api.py

# تشغيل الواجهة (اختياري)
streamlit run app.py
استخدام Ollama (المحرك المحلي)
bash
# تثبيت Ollama من https://ollama.com
ollama pull gemma3

# تشغيل خادم Ollama (اترك هذه النافذة مفتوحة)
ollama serve

# ثم اختر "Ollama AI" في الواجهة
متغيرات البيئة
أنشئ ملف .env:

env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
🔗 نقاط نهاية API
| الطريقة | المسار | الوصف |
| --- | --- | --- |
| GET | /health | فحص صحة الخدمة |
| POST | /v1/api-key | الحصول على مفتاح API |
| POST | /v1/generate | توليد تطبيق |
| GET | /v1/stats | إحصائيات الاستخدام |
| GET | /docs | توثيق Swagger |
مثال طلب
bash
# 1. الحصول على مفتاح API
curl -X POST https://my-dev--agentforge-f0bc.diploi.me/v1/api-key \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@example.com","plan":"free"}'

# 2. توليد تطبيق
curl -X POST https://my-dev--agentforge-f0bc.diploi.me/v1/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"description":"آلة حاسبة بسيطة","project_name":"MyApp"}'

# 3. تحميل ملف ZIP
# استخدم رابط download_url من الرد
💰 خطط التسعير (عبر RapidAPI)

| الخطة | السعر | الطلبات/شهر |
| --- | --- | --- |
| مجانية | $0 | 100 |
| Pro | $49 | 5,000 |
| Business | $99 | 50,000 |
| Enterprise | $499 | غير محدود |
🌍 الروابط
المصدر    الرابط
الـ API المباشر    https://my-dev--agentforge-f0bc.diploi.me
RapidAPI    AgentForge على RapidAPI
التوثيق    Swagger UI
GitHub    github.com/abdullahreda1969/AgentForge-API
الموقع الشخصي    abdullahreda1969.github.io/Portfolio
📝 مقالات
كيف بنيت API يولّد تطبيقات كاملة من وصف نصي (بالإنجليزية)

API-as-a-Service: كيف حولت الكود إلى مصدر دخل متكرر (بالإنجليزية)

📧 تواصل
البريد الإلكتروني: abdallahreda1969@gmail.com

LinkedIn: Abdullah Reda

📜 الترخيص
رخصة MIT - انظر ملف LICENSE للتفاصيل.

بُني بحب بواسطة Abdullah Reda

text

---
```
