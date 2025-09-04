# 🖥️ BSPI Computer Club Website

Official digital platform of **Bangladesh Sweden Polytechnic Institute (BSPI) Computer Club**.  
This website unites all club activities such as announcements, events, learning resources, help section, quizzes, and dashboards for leaders & members.

---

## 🚀 Features

### 🔑 User Features
- Registration with **Email Verification (OTP)**
- Login with **Brute-force protection** (Django-axes)
- **Leader approval** before login access
- Help Section with posts & threaded comments (AJAX)
- Event listing with details & multi-image gallery
- Announcements with optional Q&A
- **Quiz System** (score, results, PDF export)
- Wing-based learning resources (videos, docs, comments)

### 🧑‍💼 Leader Features
- Dashboard with pending & approved members
- Approve/Reject members with email notifications
- Manage events & learning resources

### 🔐 Admin Features
- Full access via **Django Admin (Jazzmin customized)**
- Manage users, events & monitor security

---

## ⚙️ Technical Details

- **Backend**: Django 5.1, SQLite/MySQL (configurable)  
- **Frontend**: HTML, CSS, JavaScript (GSAP animations, Locomotive scroll, Typewriter effect)  
- **Security**:
  - Email verification & Leader approval
  - CSRF protection
  - Input sanitization with Bleach
  - Account lockout with Django-axes  

---

## 🗄️ Database Models
- `CustomUser` – Extended user model with roles (leader/member)  
- `HelpPost` & `Comment` – Help section with threaded comments  
- `Announcement` – Notices with optional Q&A  
- `Event` & `EventMomentImage` – Events & galleries  
- `Person` – Advisors, Executives, Members  
- `LeaderboardMember` – Featured members/projects  
- `LearningMaterial` – Wing-based resources with videos/docs  
- `QuizQuestion` & `QuizAttempt` – Quiz system with scoring & results  
- `LessonComment` – Comments on lessons  

---

## 📄 Templates (Pages)

- `home.html` → Homepage with intro, events & contact form  
- `about.html` → Advisors, Executives, Members  
- `announcement.html` & `announcement_detail.html` → News/Notices  
- `event.html` & `event_detail.html` → Events + Photo Gallery  
- `help_section.html` → Help posts & comments  
- `leader_dashboard.html` → Manage pending/approved members  
- `user_dashboard.html` → Wing-based learning dashboard  
- `learning.html` → Learning resources page  
- `quiz.html` & `quiz_result.html` → Quiz system  
- `lession_vd.html` → Lesson video page with comments  
- Auth pages: `register.html`, `login.html`, `verify.html`  
- Security pages: `blocked.html`, `pending_approval.html`  

---

## 🎨 JavaScript Features
- 3D hover effects on cards  
- Smooth scrolling (Locomotive + GSAP)  
- Typing animation on homepage  
- FAQ accordion with localStorage persistence  
- AJAX-powered secure contact form  
- Responsive sidebar navigation  
- Quiz radio button highlight  
- GSAP animated page loader  

---

## 🔮 Future Improvements
- Live chat / Chatbot integration  
- Online event registration & attendance system  
- Competitive programming contests & hackathon module  
- Mobile app API integration  
- Automated certificate generation  

---

## ⚡ Setup Instructions

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/bspi_computerclub_site.git
   cd bspi_computerclub_site
2. **Create Virtual Environment**
   ```python -m venv venv
      source venv/bin/activate 
3. **Install Dependencies**
   ```
   pip install -r requirements.txt
4. **Run Database Migrations**
   ```
   python manage.py migrate
5. **Start Development Server**
   ```
   python manage.py runserver

**Live link**
<a  target="_blank" href="https://bspi-1.onrender.com"> View Now </a>
   
**📌 Project Evolution**
**🟢 Initial Version (Before Hackathon)**

Registration & Login with Email Verification + Leader Approval

Announcements & Events (with photo gallery)

Help Section with posts & comments

Wing-based learning resources (basic version)

Leader dashboard for member approval

Admin panel with Jazzmin customization

**🔵 Hackathon Updates (Sept 1–7, 2025)**

✅ Quiz System (questions, scoring, results, PDF export)

✅ Lesson Video Page with comment system

✅ Enhanced Security: input sanitization (Bleach), stronger brute-force protection (Django-axes)

✅ User Dashboard updated with new learning modules

✅ New Templates: quiz.html, quiz_result.html, lession_vd.html

✅ Extra UI Improvements: GSAP animations, better sidebar navigation, quiz highlighting

**👨‍💻 Developed & Designed by:**
Pritom Dey


