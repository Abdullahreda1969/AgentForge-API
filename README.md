# 🤖 AgentForge API

**الوصف**: محرك ذكي لتوليد تطبيقات ويب كاملة (Streamlit) من وصف نصي بسيط. أنشئ تطبيق "مدير مهام" أو "دفتر عناوين" في ثوانٍ.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Deployed on](https://img.shields.io/badge/Deployed%20on-Diploi-3B82F6)](https://diploi.com)

هذا المشروع هو واجهة برمجة تطبيقات (API) قوية تبسط عملية تطوير البرمجيات. بدلاً من كتابة آلاف الأسطر من الكود، ما عليك سوى إرسال وصف دقيق لتطبيقك، وسيقوم AgentForge بإنشاء مشروع Streamlit متكامل وقابل للتشغيل الفوري.

**🚀 جربه الآن على RapidAPI Hub:**  
[![RapidAPI](https://img.shields.io/badge/RapidAPI-View%20API-0066FF?logo=rapidapi)](https://rapidapi.com/abdullahreda1969/api/agentforge-ai-engine)

## ✨ الميزات الرئيسية

- **⚡ توليد فوري**: حوّل وصفك النصي إلى تطبيق Streamlit عملي في ثوانٍ.
- **🧠 مدعوم بالذكاء الاصطناعي**: يستخدم نموذج `gemma3` (محلي أو سحابي) لفهم متطلباتك.
- **🔧 جاهز للتشغيل**: الملف المُنزل (ZIP) يحتوي على كل شيء: `main.py`, `helpers.py`, `database.py` و `requirements.txt`.
- **🌐 RESTful API**: سهل الاستخدام مع أي لغة برمجة (Python، JavaScript، cURL...).
- **🎛️ خطط تسعير مرنة**: +4 خطط (مجانية ومدفوعة) تناسب جميع الاحتياجات عبر RapidAPI.

## 🏗️ كيف يعمل؟

1. **المطور** يرسل طلب `POST` إلى `/v1/generate` مع وصف لمشروعه (مثل "تطبيق مدير مهام").
2. الـ API يستقبل الطلب، يحلله، ويستخدم AI لتوليد هيكل المشروع والكود المطلوب.
3. يتم تعبئة المشروع الناتج في ملف `.zip` وإرجاع رابط للتحميل.
4. المطور يقوم بفك الضغط وتشغيل التطبيق فوراً باستخدام `streamlit run main.py`.

![AgentForge API Flow (رابط صورة توضيحية)](https://your-image-link.com/flow.png)

## 🛠️ متطلبات التشغيل (للمطور المحلي)

- Python 3.11 أو أحدث.
- `pip` (مدير حزم بايثون).

## 🚀 بداية سريعة (للاستخدام المحلي)

اتبع هذه الخطوات لتشغيل الـ API على جهازك الخاص:

1. **استنساخ المستودع**:

    ```bash
    git clone https://github.com/abdullahreda1969/AgentForge-API.git
    cd AgentForge-API
    ```

2. **إنشاء بيئة افتراضية وتثبيت المتطلبات**:

    ```bash

bash
python -m venv venv
source venv/bin/activate # على Windows: venv\Scripts\activate
pip install -r requirements.txt
تشغيل الخادوم:

bash
python run_api.py
الوصول إلى التوثيق التفاعلي:
افتح متصفحك على: <http://localhost:8000/docs> (Swagger UI) أو <http://localhost:8000/redoc> (ReDoc).

📚 الاستخدام (كعميل API)
بعد نشر API (على Diploi أو غيره)، يمكنك استخدام أي أداة أو لغة برمجة لإرسال الطلبات.

1. الحصول على مفتاح API (مجاني)
   bash
   curl -X POST <https://my-dev--agentforge-8hgo.diploi.me/v1/api-key> \
    -H "Content-Type: application/json" \
    -d '{"email": "<your-email@example.com>", "plan": "free"}'
   الرد المتوقع:

json
{
"api_key": "YOUR_GENERATED_API_KEY",
"plan": "free",
"monthly_limit": 100
} 2. توليد تطبيق
bash
curl -X POST <https://my-dev--agentforge-8hgo.diploi.me/v1/generate> \
 -H "Content-Type: application/json" \
 -H "X-API-Key: YOUR_GENERATED_API_KEY" \
 -d '{
"description": "Simple task manager app with add and delete features",
"project_name": "MyTaskManager"
}'
الرد المتوقع:

json
{
"success": true,
"project_id": "MyTaskManager",
"download_url": "/download/MyTaskManager.zip",
"message": "Project 'MyTaskManager' generated successfully"
} 3. تنزيل المشروع
انسخ قيمة download_url من الرد السابق والصقها في متصفحك لتبدأ عملية التحميل (أو استخدم wget/curl).

💳 خطط التسعير
الاشتراكات متاحة حصرياً عبر RapidAPI Hub:

الخطة السعر (شهرياً) طلبات API
BASIC (Free) $0.00 100 طلب/شهر
PRO $49.00 5,000 طلب/شهر
ULTRA $99.00 50,000 طلب/شهر
MEGA $499.00 غير محدود
اطلع على صفحة API على RapidAPI

📁 هيكل المشروع
text
AgentForge_API/
├── api/ # واجهة برمجة التطبيقات (FastAPI)
│ ├── main.py # نقطة الدخول وتهيئة الـ API
│ ├── auth.py # إدارة مفاتيح API
│ └── models.py # نماذج البيانات (Pydantic)
├── core/ # المنطق الأساسي للنظام
│ ├── orchestrator.py # تنسيق عملية التوليد
│ └── templates.py # قوالب المشاريع الجاهزة
├── local/ # مشغل النموذج المحلي (للاختبار)
│ └── orchestrator.py
├── projects/ # الأماكن التي تُحفظ فيها المشاريع المُنشأة
├── requirements.txt # تبعيات المشروع (Python packages)
├── run_api.py # سكريبت تشغيل خادوم الـ API
└── README.md # هذا الملف

🤝 المساهمة
المساهمات مرحَّب بها! يمكنك فتح Issue أو إرسال Pull Request على GitHub.

📞 الدعم
الدعم الفني (للمشتركين المدفوعين): [abdallahreda1969@gmail.com]

قناة المجتمع (مجانية): [رابط دعوة Discord/Telegram]

📜 الترخيص
هذا المشروع مرخص تحت رخصة MIT.

✨ صُنع بواسطة Abdullah Reda

---
