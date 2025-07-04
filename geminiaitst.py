import google.generativeai as genai

genai.configure(api_key="AIzaSyDi1bkSkJ9YDXRycdvpXemeI2RwernKNhI")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain Bitcoin")
print(response.text)