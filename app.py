from flask import Flask, request, render_template, send_file
import google.generativeai as genai

# Masukkan API key Anda di sini
api_key = "AIzaSyC2NW89CA2s9KGuXInjB107-xzOllcJz18"
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "models/gemini-1.5-flash",
    system_instruction="You are a professional AI translator proficient in all world languages. Your task is to translate any text into Indonesian with high accuracy, preserving the original meaning, and adapting the language style to fit Indonesian context and culture."
)

app = Flask(__name__)

# Fungsi untuk menerjemahkan isi file
def translate_text(input_text):
    response = model.generate_content(input_text)
    return response.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    input_text = file.read().decode('utf-8')
    translated_text = translate_text(input_text)

    # Menyimpan hasil terjemahan ke file output
    output_file_path = 'output.txt'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(translated_text)

    return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)