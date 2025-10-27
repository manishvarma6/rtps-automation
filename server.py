import json
import os
import time
import threading
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from flask import Flask, request, jsonify, send_from_directory
# import requests
from geminisearch import gemini_file_analyze

# app = Flask(__name__)



# def choose_script(apply_for):
#     apply_for = apply_for.strip().lower()
#     if apply_for in ["residence", "residence certificate"]:
#         from residentauto import run_browser_automation
#     elif apply_for in ["income", "income certificate"]:
#         from incomeauto import run_browser_automation
#     elif apply_for in ["caste", "caste certificate"]:
#         from castauto import run_browser_automation
#     else:
#         raise ValueError(f"Unknown certificate type: {apply_for}")
#     return run_browser_automation



# @app.route("/")
# def home():
#     # serve the html form
#     return send_from_directory(os.getcwd(), "residence_certificate_form.html")


# @app.route("/submit", methods=["POST"])
# # def submit_form():
# #     data = request.json
# #     apply_for = data.get("applyFor", "").lower()

# #     # Save JSON (optional)
# #     with open("formdata.json", "w", encoding="utf-8") as f:
# #         json.dump(data, f, indent=2, ensure_ascii=False)

# #     # ✅ Choose automation file dynamically
# #     def choose_script(apply_for):
# #         if "residence" in apply_for:
# #             from residentauto import run_browser_automation
# #         elif "caste" in apply_for:
# #             from castauto import run_browser_automation
# #         elif "income" in apply_for:
# #             from incomeauto import run_browser_automation
# #         else:
# #             raise ValueError(f"Unknown certificate type: {apply_for}")
# #         return run_browser_automation

# #     run_browser_automation_func = choose_script(apply_for)

# #     # ✅ Run in background thread (so API responds instantly)
# #     threading.Thread(target=run_browser_automation_func, args=(data,)).start()

# #     return jsonify({"status": "ok", "message": f"Automation started for {apply_for.title()} certificate!"})



# def submit_form():
#     data = request.json
#     apply_for = data.get("applyFor", "").strip().lower()

#     # 🧠 Create unique JSON file for each request
#     timestamp = int(time.time())
#     json_filename = f"formdata_{apply_for}_{timestamp}.json"
#     json_path = os.path.join("saved_forms", json_filename)

#     # Ensure folder exists
#     os.makedirs("saved_forms", exist_ok=True)

#     # Save this request's data safely
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

#     # ✅ Choose correct script (no overlap)
#     def choose_script(apply_for):
#         if apply_for in ["residence", "residence certificate"]:
#             from residentauto import run_browser_automation
#         elif apply_for in ["income", "income certificate"]:
#             from incomeauto import run_browser_automation
#         elif apply_for in ["caste", "caste certificate"]:
#             from castauto import run_browser_automation
#         else:
#             raise ValueError(f"Unknown certificate type: {apply_for}")
#         return run_browser_automation

#     run_func = choose_script(apply_for)

#     # ✅ Background thread (no blocking)
#     threading.Thread(target=run_func, args=(data,)).start()

#     return jsonify({
#         "status": "ok",
#         "message": f"Automation started for {apply_for.title()} certificate!",
#         "dataFile": json_filename
#     })



# @app.route("/use_saved", methods=["POST"])
# def use_saved():
#     req = request.json
#     filename = req.get("filename")
#     update_choice = req.get("updateChoice")  # "update" or "use"

#     # Load saved file
#     path = os.path.join("saved_forms", filename)
#     if not os.path.exists(path):
#         return jsonify({"error": "Saved file not found"}), 404

#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     # If user chose to update, send data back to frontend for editing
#     if update_choice == "update":
#         return jsonify({"status": "ok", "data": data})

#     # Else directly trigger automation
#     apply_for = data.get("applyFor", "").strip().lower()
#     func = choose_script(apply_for)
#     threading.Thread(target=func, args=(data,)).start()

#     return jsonify({"status": "ok", "message": f"Started automation using saved data for {apply_for.title()}!"})



# if __name__ == "__main__":
#     app.run(debug=True)






















import json
import os
import threading
from flask import Flask, request, jsonify, send_from_directory

# Import your automation modules
from geminisearch import gemini_file_analyze  # keep as-is if used in your autos
# NOTE: residentauto.py, incomeauto.py, castauto.py must have run_browser_automation(data) function

app = Flask(__name__)

# -----------------------------------------------------------
# Serve frontend HTML form
# -----------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "residence_certificate_form.html")


# -----------------------------------------------------------
# Handle direct form submissions (new applications)
# -----------------------------------------------------------
@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json
    apply_for = data.get("applyFor", "").lower()

    # Save a copy for debugging (optional)
    with open("formdata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Choose automation dynamically
    def choose_script(apply_for):
        if "residence" in apply_for:
            from residentauto import run_browser_automation
        elif "caste" in apply_for:
            from castauto import run_browser_automation
        elif "income" in apply_for:
            from incomeauto import run_browser_automation
        else:
            raise ValueError(f"Unknown certificate type: {apply_for}")
        return run_browser_automation

    run_func = choose_script(apply_for)

    # Run automation in background thread
    threading.Thread(target=run_func, args=(data,)).start()

    return jsonify({"status": "ok", "message": f"Automation started for {apply_for.title()} certificate!"})


# -----------------------------------------------------------
# Handle saved applications (loaded from localStorage)
# -----------------------------------------------------------
@app.route("/use_saved", methods=["POST"])
def use_saved():
    req = request.json
    data = req.get("data")
    # certificate_choice = req.get("certificateChoice", "").lower()
    certificate_choice = req.get("certificateChoice", "").lower().strip().replace("]", "")


    if not data:
        return jsonify({"status": "error", "message": "No saved data received"}), 400

    # Choose automation dynamically
    def choose_script(cert):
        if "residence" in cert:
            from residentauto import run_browser_automation
        elif "caste" in cert:
            from castauto import run_browser_automation
        elif "income" in cert:
            from incomeauto import run_browser_automation
        else:
            raise ValueError(f"Unknown certificate type: {cert}")
        return run_browser_automation

    run_func = choose_script(certificate_choice)
    threading.Thread(target=run_func, args=(data,)).start()

    return jsonify({
        "status": "ok",
        "message": f"Automation started for saved {certificate_choice.title()} data!"
    })


if __name__ == "__main__":
    app.run(debug=True)
