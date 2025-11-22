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

# ======================================================
# FLASK SERVER TO RECEIVE FORM DATA
# ======================================================
# app = Flask(__name__)


def run_browser_automation(data):
    """Runs the Selenium automation using the received JSON data."""
    print("✅ Starting browser automation...")

    # Save JSON so existing code can still use it if needed
    with open("formdata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # ====== Start Browser ======

        
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Bihar form URL (replace if different)
    driver.get("https://serviceonline.bihar.gov.in/")  

    wait = WebDriverWait(driver, 5)

    # 1. Click "सामान्य प्रशासन विभाग"
    samanya = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[normalize-space(text())='सामान्य प्रशासन विभाग']")
    ))
    samanya.click()

    # 2. Click "आवासीय प्रमाण-पत्र का निर्गमन"
    awasiy = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a/p[contains(normalize-space(.),'आवासीय प्रमाण-पत्र का निर्गमन')]")
    ))
    awasiy.click()

    time.sleep(1)  # allow collapse animation to finish

    anchal = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//p[@class='pLev2expand']/a[contains(text(),'अंचल स्तर पर')]")
    ))

    anchal.click()

    time.sleep(5)

    # 4. Switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    print("✅ Opened:", driver.current_url)


    # ====== Fill the Form ======
    time.sleep(3)


    def fill_name_with_spaces(driver, field_id: str, name: str):

        element = driver.find_element(By.ID, field_id)
        element.clear()
        
        words = name.strip().split()
        for i, word in enumerate(words):
            element.send_keys(word)
            if i < len(words) - 1:
                element.send_keys(Keys.SPACE)



    # Gender
    if data["gender"] == "Male":
        driver.find_element(By.ID, "17290_1").click()
    elif data["gender"] == "Female":
        driver.find_element(By.ID, "17290_2").click()
    else:
        driver.find_element(By.ID, "17290_3").click()

    fill_name_with_spaces(driver, "78250", data["applicantName"])
    time.sleep(0.5)



    #applicant hindi name
    element = driver.find_element(By.ID, "17287")
    element.clear()  
    element.send_keys(data["applicantNameHindi"])  
    time.sleep(0.5)



    # Father name
    # driver.find_element(By.ID, "78251").send_keys(data["fatherName"])
    driver.execute_script("arguments[0].value = arguments[1];", 
                        driver.find_element(By.ID, "78251"), 
                        data["fatherName"])
    time.sleep(0.5)


    #father hindi name
    element = driver.find_element(By.ID, "17288")
    element.clear()  
    element.send_keys(data["fatherNameHindi"])  
    time.sleep(0.5)

    #mother name
    # driver.find_element(By.ID, "41565").send_keys(data["motherName"])
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.ID, "41565"),
        data["motherName"].rstrip()
    )
    time.sleep(0.5)



    #mother hindi name
    element = driver.find_element(By.ID, "41567")
    element.clear()  
    element.send_keys(data["motherNameHindi"])  
    time.sleep(0.5)




    #husband name
    # driver.find_element(By.ID, "64876").send_keys(data["husbandName"])
    driver.execute_script("arguments[0].value = arguments[1];", 
                        driver.find_element(By.ID, "64876"), 
                        data["husbandName"])
    time.sleep(0.5)

    #husband hindi name
    element = driver.find_element(By.ID, "64877")
    element.clear()  
    element.send_keys(data["husbandNameHindi"])  

    time.sleep(1)
    # Mobile & Email
    driver.find_element(By.ID, "17293").send_keys(data["mobile"])
    driver.find_element(By.ID, "17294").send_keys(data["email"])

    # Wait for popup to show up
    popup = WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.ID, "digilockerPopUp"))
    )

    # Wait for OTP modal to appear
    otp_box = WebDriverWait(driver,2).until(
        EC.presence_of_element_located((By.ID, "otp"))
    )





    # Browser में modal input create करना
    driver.execute_script("""
    if (!document.getElementById('otp_modal')) {
        let div = document.createElement('div');
        div.id = 'otp_modal';
        div.style.position = 'fixed';
        div.style.top = '40%';
        div.style.left = '40%';
        div.style.padding = '20px';
        div.style.background = '#fff';
        div.style.border = '2px solid black';
        div.style.zIndex = 9999;
        div.innerHTML = '<label>Enter OTP:</label><input id="otp_input" /><button onclick="document.getElementById(\\'otp_modal\\').dataset.value = document.getElementById(\\'otp_input\\').value; document.getElementById(\\'otp_modal\\').dataset.done=1;">OK</button>';
        div.dataset.done = 0;
        document.body.appendChild(div);
    }
    """)

    # Wait until user enters OTP and clicks OK
    while True:
        done = driver.execute_script("return document.getElementById('otp_modal').dataset.done;")
        if done == '1':
            break
        time.sleep(0.2)

    # Fetch OTP from modal
    otp_value = driver.execute_script("return document.getElementById('otp_modal').dataset.value;")
    print("Entered OTP:", otp_value)

    # Enter OTP
    otp_box.send_keys(otp_value)


    driver.execute_script("""
    var modal = document.getElementById('otp_modal');
    if(modal){ modal.remove(); }
    """)


    # Click on Validate button
    validate_btn = driver.find_element(By.ID, "validateOTP")
    validate_btn.click()

    # Wait for alert
    WebDriverWait(driver, 5).until(EC.alert_is_present())

    # Switch to alert
    alert = driver.switch_to.alert

    # Accept the alert (click OK)
    alert.accept()



    #to select the address dropdown
    def select_dropdown_case_insensitive(select_element, text_to_match):
        select = Select(select_element)
        for option in select.options:
            if option.text.strip().lower() == text_to_match.strip().lower():
                select.select_by_visible_text(option.text.strip())
                return
        raise Exception(f"Option '{text_to_match}' not found in dropdown")



    # --- State ---
    state_el = wait.until(EC.presence_of_element_located((By.ID, "17391")))
    select_dropdown_case_insensitive(state_el, data["state"])

    # --- District ---
    wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//select[@id='17297']/option[normalize-space()]")
    ))
    district_el = driver.find_element(By.ID, "17297")
    select_dropdown_case_insensitive(district_el, data["district"])

    # --- Sub division ---
    wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//select[@id='17296']/option[normalize-space()]")
    ))
    district_el = driver.find_element(By.ID, "17296")
    select_dropdown_case_insensitive(district_el, data["subdivision"])

    # --- Block ---
    wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//select[@id='17298']/option[normalize-space()]")
    ))
    block_el = driver.find_element(By.ID, "17298")
    select_dropdown_case_insensitive(block_el, data["block"])

    time.sleep(2)


    #to select the radio button based on local body 
    # def select_radio_by_label(text_to_match):
    #     # wait until atleast one radio option is present
    #     radios = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@name='75290']")))

    #     for radio in radios:
    #         # label text निकालो (label[@for=id])
    #         label = driver.find_element(By.XPATH, f"//label[@for='{radio.get_attribute('id')}']").text.strip()
    #         if text_to_match.strip().lower() in label.lower():
    #             driver.execute_script("arguments[0].click();", radio)  # safe click
    #             print(f"✅ Selected option: {label}")
    #             return
        
    #     raise Exception(f"Option '{text_to_match}' not found in Local Body Type")

    def select_radio_by_label(value):
        xpath = f"//input[@name='75290' and @value='{value}']"
        radio = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", radio)


    select_radio_by_label(data["localBodyType"])




    # Ward, Village, Post Office, Police Station
    driver.find_element(By.ID, "56887").send_keys(data["wardNo"])
    driver.find_element(By.ID, "17299").send_keys(data["village"])
    driver.find_element(By.ID, "17300").send_keys(data["postOffice"])

    # --- police station ---
    state_el = wait.until(EC.presence_of_element_located((By.ID, "65015")))
    select_dropdown_case_insensitive(state_el, data["policeStation"])


    # Pin Code, Aadhaar
    driver.find_element(By.ID, "90772").send_keys(data["pincode"])


    # Desired base folder
    base_folder = r"C:\Users\DELL\Downloads"
    # Get only file name from whatever user gave
    filename = os.path.basename(data["photoPath"])
    # Combine new base path + filename
    photo_path = os.path.join(base_folder, filename)
    driver.find_element(By.ID, "90837").send_keys(photo_path)



    # Residence Type
    if data["residenceType"] == "Permanent":
        driver.find_element(By.ID, "41566_1").click() 
    else:
        driver.find_element(By.ID, "41566_2").click()

    driver.find_element(By.ID, "41566_1").click()
    # # Purpose
    # driver.find_element(By.ID, "90775").send_keys(data["purpose"])




    # पहले captcha दिखाई देने तक wait करो
    captcha_element = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "captchaImage"))   # अपने सही selector से बदलें
    )

    # Save screenshot of captcha
    captcha_file = "captcha.png"   # relative path
    captcha_element.screenshot(captcha_file)

    # Convert to absolute path
    captcha_path = os.path.abspath(captcha_file)
    print("✅ Captcha saved at:", captcha_path)



    # 🔹 Example 2: Image + Prompt
    img_file = captcha_path
    result_img = gemini_file_analyze(img_file, prompt="give me the only number written on the image . nothing else.")
    captcha_text = result_img.strip()
    print("🖼️ Image Result:\n", result_img)

    driver.find_element(By.ID, "captchaAnswer").send_keys(captcha_text)

    driver.find_element(By.ID, "submit_btn").click()


    WebDriverWait(driver, 5).until(EC.alert_is_present())

    # Switch to alert
    alert = driver.switch_to.alert

    # Accept the alert (click OK)
    alert.accept()
    time.sleep(10)

    driver.find_element(By.ID, "submit_btn").click()
    time.sleep(5)

    driver.find_element(By.ID, "submit_btn").click()


    time.sleep(5)
    # Step 1: Wait for dropdown and select "आधार कार्ड"
    dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "4867_enclDoc_cb"))
    )

    select = Select(dropdown)
    select.select_by_visible_text("आधार कार्ड")   # or select_by_value("4867-4394")

    # Step 2: Wait for file input to be enabled
    file_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "4867_attach"))
    )



    # Desired base folder
    # base_folder = r"C:\Users\DELL\Downloads"
    # Get only file name from whatever user gave
    aadharfile = os.path.basename(data["aadharPath"])
    # Combine new base path + filename
    aadharpath = os.path.join(base_folder, aadharfile)
    file_input.send_keys(aadharpath)
    time.sleep(10)


    driver.find_element(By.ID, "submit_btn").click()
    time.sleep(5)
    driver.find_element(By.ID, "submit_btn").click()
    time.sleep(5)

    driver.find_element(By.ID, "pdf_btn").click()


    time.sleep(5)



# @app.route("/")
# def home():
#     # serve the html form
#     return send_from_directory(os.getcwd(), "residence_certificate_form.html")

# @app.route("/submit", methods=["POST"])
# def submit_form():
#     data = request.json

#     # Save form data locally (optional)
#     with open("formdata.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

#     # ✅ Start Selenium automation in a separate thread
#     import threading
#     threading.Thread(target=run_browser_automation, args=(data,)).start()

#     return jsonify({"status": "ok", "message": "Automation started!"})

# if __name__ == "__main__":
#     app.run(debug=True)
