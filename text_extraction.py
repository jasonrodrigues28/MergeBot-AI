import fitz  
from transformers import pipeline
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    
    text = "" #empty string to store the text
    
    for page in doc:  
        text += page.get_text("text")
    return text

pdf_text = extract_text_from_pdf("t.pdf")
#print(pdf_text)

#making senetces into chunks
chunks = []
current_chunk = ""

sentences = pdf_text.split(". ")
for i in sentences:
    if len(current_chunk) + len(i) > 1000:
        chunks.append(current_chunk)
        current_chunk = ""
    current_chunk += i + ". "

if current_chunk:
    chunks.append(current_chunk)

#summerizing
hello = ""
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

for chunk in tqdm(chunks, desc="Summarizing: "):
    summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
    hello = summary

print(hello)