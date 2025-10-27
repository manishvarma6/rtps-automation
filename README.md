
RTPS Bihar Certificate Automation

Overview

This project automates the online application process for **Resident**, **Caste**, and **Income Certificates** through the **RTPS Bihar** portal using **Python (Flask + Selenium)** and a smart front-end built with **HTML, CSS, and JavaScript**.

The goal is to reduce manual work by automatically filling forms, uploading documents, and submitting applications — all from a simple web dashboard.

---

 Features

✅ **Three Certificate Modules**

* 🏠 Resident Certificate
* 🧬 Caste Certificate
* 💰 Income Certificate

✅ **Web Dashboard**

* Built with HTML/CSS/JS for user input
* Allows saving & loading of application data (localStorage support)
* File uploads (photo, Aadhaar, documents)

✅ **Automation Engine (Python + Selenium)**

* Auto-fills RTPS form fields
* Handles dropdowns, text inputs, file uploads, and captchas
* Uses Gemini AI (Google Generative AI) to read captcha numbers from images

✅ **Flask Backend**

* REST API endpoints for `/submit` and `/use_saved`
* Background threading for smooth automation execution
* JSON-based communication with frontend

✅ **Error Handling**

* Handles missing data, invalid types, and CORS issues gracefully
* Logs all requests and automation steps

---

### 🧠 Tech Stack

| Layer          | Technology                    |
| -------------- | ----------------------------- |
| Frontend       | HTML, CSS, JavaScript         |
| Backend        | Flask (Python)                |
| Automation     | Selenium WebDriver            |
| AI Integration | Google Generative AI (Gemini) |
| File Parsing   | JSON                          |
| Browser        | Chrome / Edge                 |

---

 Project Structure

```
 RTPS-Automation

│
├── server.py                   # Flask backend
├── residentauto.py             # Resident certificate automation
├── castauto.py                 # Caste certificate automation
├── incomeauto.py               # Income certificate automation
├── geminisearch.py             # Captcha reader (Gemini AI)
├── formdata.json               # Temporary saved data
└── README.md                   # Project description
```

---

 How to Run Locally

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/rtps-automation.git
   cd rtps-automation
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key**

   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run Flask server**

   ```bash
   python server.py
   ```

5. **Open Frontend**

   * Open `index.html` or certificate form (`resident_certificate_form.html`, etc.)
   * Start automation via UI buttons.

---

### 🧩 Requirements

* Python 3.10+
* Google Chrome + ChromeDriver
* Stable Internet Connection
* Gemini API key (for captcha recognition)

---

### ⚠️ Disclaimer

This project is built **for educational and automation learning purposes only**.
Do not use it for illegal or unauthorized form submissions.
RTPS Bihar is a government service; misuse may violate their terms of service.

---


---

### ⭐ Support

If you like this project, consider giving it a **⭐ on GitHub** — it helps others discover it too!

---

Would you like me to tailor this README specifically with your **project folder names and your cyber café name (PV Digital Solution)**?
I can make it more personalized and professional before you upload.
