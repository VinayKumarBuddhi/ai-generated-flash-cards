from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import PyPDF2
import docx
import requests

# Function to extract text from PDF files
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from Word files
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

# Function to extract text from TXT files
def extract_text_from_txt(file):
    return file.read().decode('utf-8')

# Function to generate flashcards using OpenAI API
def generate_flashcards(text, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": [
                {"role": "system", "content": "You are an AI that generates educational flashcards."},
                {"role": "user", "content": f"Generate concise flashcards from the following text:\n\n{text}"}
            ],
        "max_tokens": 300
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)
    return response.json()['choices'][0]['message']['content']


# View to handle file uploads
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file = document.file
            # Extract text based on file type
            if file.name.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            elif file.name.endswith('.docx'):
                text = extract_text_from_docx(file)
            elif file.name.endswith('.txt'):
                text = extract_text_from_txt(file)
            else:
                return render(request, 'extractor/upload.html', {'form': form, 'error': 'Unsupported file format'})

            # Generate flashcards using OpenAI API
            api_key = "api_key"  # Replace with your OpenAI API key
            flashcards_text = generate_flashcards(text, api_key)
            flashcards_list = [fc.strip() for fc in flashcards_text.split("\n") if fc.strip()]
            return render(request, 'extractor/upload.html', {'form': form, 'flashcards': flashcards_list})
    else:
        form = DocumentForm()
    return render(request, 'extractor/upload.html', {'form': form})