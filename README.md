# Reddit Weekly Analytics 📊

> **Automated Reddit analytics platform**: Fetch posts, analyze engagement metrics, and export analytics to Google Sheets weekly

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF)](https://github.com/features/actions)
[![PRAW](https://img.shields.io/badge/Reddit-PRAW-FF4500)](https://praw.readthedocs.io/)
[![Google Sheets](https://img.shields.io/badge/Google-Sheets-34A853)](https://www.google.com/sheets/)

## 🚀 المميزات (Features)

✅ **جلب البيانات التلقائية**: يجمع أحدث 1000 منشور من أي subreddit  
✅ **تحليل إحصائي ذكي**: Top posts, engagement rate, karma growth  
✅ **تصدير مباشر**: تحديث Google Sheets تلقائي كل أسبوع  
✅ **أتمتة كاملة**: GitHub Actions scheduled task كل اثنين  
✅ **سهل الاستخدام**: إعداد بسيط بـ environment variables  

## 📋 المتطلبات (Requirements)

- Python 3.11+
- حساب Reddit API
- حساب Google Cloud (Service Account)
- GitHub repository (مع GitHub Actions)

## 🔧 الإعداد (Setup)

### 1️⃣ استنساخ المستودع (Clone Repository)

```bash
git clone https://github.com/yourusername/reddit-weekly-analytics.git
cd reddit-weekly-analytics
```

### 2️⃣ تثبيت المتطلبات (Install Dependencies)

```bash
pip install -r requirements.txt
```

### 3️⃣ إعداد Reddit API 🤖

1. انتقل إلى [Reddit Apps](https://www.reddit.com/prefs/apps)
2. اضغط "Create an app" أو "Create another app"
3. اختر نوع التطبيق: **script**
4. انقر "Create app"
5. ستحصل على:
   - **Client ID**: تحت اسم التطبيق
   - **Client Secret**: الزر "secret"

### 4️⃣ إعداد Google Sheets API 📊

#### أ. إنشاء Google Cloud Project:
1. انتقل إلى [Google Cloud Console](https://console.cloud.google.com/)
2. اضغط "Create a new project"
3. اسم المشروع: `reddit-analytics`
4. انتظر التفعيل

#### ب. تفعيل Google Sheets API:
1. اذهب إلى APIs & Services → Library
2. ابحث عن "Google Sheets API"
3. اضغط "Enable"

#### ج. إنشاء Service Account:
1. اذهب إلى APIs & Services → Credentials
2. اضغط "Create Credentials" → "Service Account"
3. ملء البيانات:
   - Service account name: `reddit-analytics`
4. اضغط "Create and continue"
5. اضغط "Create key" → JSON
6. ستحمل ملف JSON
7. احفظ محتوى JSON الكامل

### 5️⃣ إضافة GitHub Secrets 🔐

انتقل إلى: **Repository** → **Settings** → **Secrets and variables** → **Actions**

أضف هذه الـ Secrets:

| اسم Secret | القيمة |
|-----------|--------|
| `REDDIT_CLIENT_ID` | Client ID من Reddit |
| `REDDIT_CLIENT_SECRET` | Client Secret من Reddit |
| `SUBREDDIT_NAME` | اسم الـ Subreddit (مثل: `python`, `programming`) |
| `GOOGLE_SHEET_NAME` | اسم Google Sheet (مثل: `Reddit Weekly Analytics`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | محتوى ملف JSON الكامل من Google Cloud |

#### مثال لإضافة Secret:

```bash
# في GitHub UI:
1. اضغط "New repository secret"
2. في Name: ادخل اسم السيكريت
3. في Secret: الصق القيمة
4. اضغط "Add secret"
```

## 🏃 التشغيل (Running)

### 🔄 التشغيل التلقائي (Automatic)

يعمل تلقائياً **كل اثنين الساعة 8:00 صباحاً UTC**

للتحقق من الحالة:
1. اذهب إلى **Actions** tab في repo
2. اختر **Reddit Weekly Analytics** workflow
3. شاهد آخر تشغيل

### ▶️ التشغيل اليدوي (Manual)

#### في GitHub UI:

```
Actions → Reddit Weekly Analytics → Run workflow
```

#### أو من Terminal (إذا كان لديك GitHub CLI):

```bash
gh workflow run weekly_analytics.yml
```

### 💻 التشغيل المحلي (Local)

```bash
# ضع environment variables:
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
export SUBREDDIT_NAME="python"
export GOOGLE_SHEET_NAME="Reddit Weekly Analytics"
export GOOGLE_APPLICATION_CREDENTIALS="{json_content}"

# ثم شغل:
python reddit_stats.py
```

## 📊 مخرجات البيانات (Output)

تُحدَّث Google Sheet تلقائياً مع:

| معلومة | الوصف |
|------|-------|
| **Week ID** | رقم الأسبوع (YYYY-W##) |
| **Total Posts** | عدد المنشورات |
| **Total Score** | مجموع الـ Upvotes |
| **Total Comments** | عدد التعليقات |
| **Avg Score** | متوسط الـ Score |
| **Avg Comments** | متوسط التعليقات |
| **Engagement Rate** | معدل التفاعل |
| **Top 10 Posts** | أفضل 10 منشورات |
| **All Posts Data** | جميع البيانات المفصلة |

## 🏗️ هيكل المشروع (Project Structure)

```
reddit-weekly-analytics/
├── .github/
│   └── workflows/
│       └── weekly_analytics.yml    # GitHub Actions workflow
├── reddit_stats.py                 # السكريبت الرئيسي
├── requirements.txt                 # المتطلبات
├── .gitignore                      # ملفات المسح
└── README.md                        # هذا الملف
```

## 📝 ملف السكريبت (reddit_stats.py)

```python
# الدوال الرئيسية:

fetch_reddit_posts()       # جلب المنشورات من Reddit
analyze_engagement()       # تحليل معايير التفاعل
export_to_google_sheets()  # تصدير إلى Google Sheets
main()                     # البرنامج الرئيسي
```

## 🐛 استكشاف الأخطاء (Troubleshooting)

### ❌ خطأ: "Reddit credentials not configured"

```
✅ الحل: تأكد من إضافة REDDIT_CLIENT_ID و REDDIT_CLIENT_SECRET في GitHub Secrets
```

### ❌ خطأ: "Google credentials not found"

```
✅ الحل: تأكد من نسخ محتوى JSON الكامل إلى GOOGLE_APPLICATION_CREDENTIALS
```

### ❌ Workflow لم يعمل

```
✅ الحل:
1. تحقق من Actions tab → اضغط على الـ workflow
2. شاهد الأخطاء في Logs
3. تأكد من الـ Secrets صحيحة
4. الـ Subreddit موجود
```

## 📚 المراجع (References)

- [PRAW Documentation](https://praw.readthedocs.io/)
- [gspread Documentation](https://docs.gspread.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 📄 الترخيص (License)

MIT License - استخدم حراً ✨

## 🤝 المساهمة (Contributing)

المساهمات مرحب بها! يمكنك:

1. Fork المشروع
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add AmazingFeature'`)
4. Push للـ branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ ملاحظات مهمة

- تأكد من عدم مشاركة Reddit/Google credentials علناً
- Reddit API يسمح بـ 60 requests في الدقيقة
- Google Sheets API له حد أقصى (عادة كافٍ للاستخدام العام)
- Workflow يعمل 24/7 لكن مجاني فقط لـ 2000 دقيقة/شهر

## 📞 الدعم (Support)

إذا واجهت مشكلة:

1. ✅ تحقق من [قسم استكشاف الأخطاء](#-استكشاف-الأخطاء)
2. 📖 راجع التوثيق الرسمية
3. 🐛 افتح Issue جديد في GitHub

---

**Made with ❤️ by [Your Name]**

**آخر تحديث**: November 2025
