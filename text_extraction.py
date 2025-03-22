import fitz  

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

print(chunks)