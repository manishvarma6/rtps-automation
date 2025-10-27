# # xyz.py
# import google.generativeai as genai
# import os

# os.environ["GRPC_VERBOSITY"] = "ERROR"
# os.environ["GLOG_minloglevel"] = "2"

# # ✅ Initialize Gemini API
# API_KEY = "AIzaSyDkcOkzFf4a-h8oKkhAGwp-lb1nhYIIsBc"
# genai.configure(api_key=API_KEY)

# def gemini_file_analyze(file_path, prompt="Summarize this file in English."):
#     try:
#         # ✅ Upload the file to Gemini
#         uploaded_file = genai.upload_file(file_path)
#         print(f"📂 Uploaded file: {uploaded_file.uri}")

#         # ✅ Load Gemini model
#         model = genai.GenerativeModel("gemini-1.5-flash")

#         # ✅ Pass uploaded file + prompt
#         response = model.generate_content([uploaded_file, prompt])

#         return response.text.strip()

#     except Exception as e:
#         return f"⚠️ Error analyzing file with Gemini: {e}"








# import google.generativeai as genai
# import os

# # Set log levels (optional)
# os.environ["GRPC_VERBOSITY"] = "ERROR"
# os.environ["GLOG_minloglevel"] = "2"

# # ✅ Initialize Gemini API
# API_KEY = "AIzaSyDkcOkzFf4a-h8oKkhAGwp-lb1nhYIIsBc"
# genai.configure(api_key=API_KEY)

# def gemini_file_analyze(file_path, prompt="Summarize this file in English."):
#     try:
#         # ✅ Upload file
#         uploaded_file = genai.upload_file(file_path)
#         print(f"📂 Uploaded file: {uploaded_file.uri}")

#         # ✅ Load Gemini model properly
#         model = genai.GenerativeModel(model_name="gemini-1.5-flash")

#         # ✅ Generate content with file + prompt
#         response = model.generate_content([uploaded_file, prompt])

#         return response.text.strip()

#     except Exception as e:
#         return f"⚠️ Error analyzing file with Gemini: {e}"



# import google.generativeai as genai
# import os

# # ✅ Reduce logging noise (optional)
# os.environ["GRPC_VERBOSITY"] = "ERROR"
# os.environ["GLOG_minloglevel"] = "2"

# # ✅ Initialize Gemini API
# API_KEY = "AIzaSyDkcOkzFf4a-h8oKkhAGwp-lb1nhYIIsBc"   # apna API key daalo
# genai.configure(api_key=API_KEY)

# def gemini_file_analyze(file_path, prompt="give me the only number written on the image . nothing else."):
#     try:
#         # ✅ Create a temporary RAG store
#         rag_store = genai.create_rag_store(display_name="temp_rag_store")

#         # ✅ Upload file into the store
#         uploaded_file = genai.upload_file(
#             file_path,
#             display_name=os.path.basename(file_path),
#             rag_store_name=rag_store.name
#         )
#         print(f"📂 Uploaded file: {uploaded_file.uri}")

#         # ✅ Use Gemini model
#         model = genai.GenerativeModel(model_name="gemini-1.5-flash")

#         # ✅ Generate response
#         response = model.generate_content([uploaded_file, prompt])

#         # ✅ Optional: clean up to save quota
#         genai.delete_file(uploaded_file.name)
#         genai.delete_rag_store(rag_store.name)

#         return response.text.strip()

#     except Exception as e:
#         return f"⚠️ Error analyzing file with Gemini: {e}"





# working was this 

import google.generativeai as genai
import os

# ✅ Reduce logging noise (optional)
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# ✅ Initialize Gemini API
API_KEY = "AIzaSyDkcOkzFf4a-h8oKkhAGwp-lb1nhYIIsBc"  
genai.configure(api_key=API_KEY)

def gemini_file_analyze(file_path, prompt="give me the only number written on the image . nothing else."):
    try:
        # ✅ Upload the file to Gemini
        uploaded_file = genai.upload_file(file_path)
        print(f"📂 Uploaded file: {uploaded_file.uri}")

        # ✅ Load Gemini model (use available one)
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

        # ✅ Pass uploaded file + prompt
        response = model.generate_content([uploaded_file, prompt])

        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error analyzing file with Gemini: {e}"

# img_file = "captcha.png"

# if __name__ == "__main__":
#     result_img = gemini_file_analyze(img_file, prompt="give me the only number written on the image . nothing else.")
#     captcha_text = result_img.strip()
#     print("🖼️ Image Result:\n", result_img)




# import google.generativeai as genai
# import os
# import base64

# os.environ["GRPC_VERBOSITY"] = "ERROR"
# os.environ["GLOG_minloglevel"] = "2"

# API_KEY = "AIzaSyDkcOkzFf4a-h8oKkhAGwp-lb1nhYIIsBc"   # apna API key daalo
# genai.configure(api_key=API_KEY)




# def gemini_file_analyze(file_path, prompt="give me the only number written on the image. nothing else."):
#     try:
#         # ✅ Detect file type automatically
#         ext = os.path.splitext(file_path)[1].lower()
#         mime_type = "image/png" if ext == ".png" else "image/jpeg"

#         # ✅ Read the image as base64
#         with open(file_path, "rb") as f:
#             image_bytes = f.read()
#         image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#         # ✅ Load older image-compatible model
#         model = genai.GenerativeModel(model_name="models/gemini-pro-vision")

#         # ✅ Generate content with image + prompt
#         response = model.generate_content([
#             {
#                 "mime_type": mime_type,
#                 "data": image_base64
#             },
#             prompt
#         ])

#         return response.text.strip()

#     except Exception as e:
#         return f"⚠️ Error analyzing file with Gemini: {e}"

# if __name__ == "__main__":
#     img_file = "captcha.png"  # update your file name
#     result = gemini_file_analyze(img_file)
#     print("🖼️ Image Result:\n", result)