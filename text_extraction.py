import fitz  

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    
    text = "" #empty string to store the text
    
    for page in doc:  
        text += page.get_text("text")
    return text

pdf_text = extract_text_from_pdf("t.pdf")
print(pdf_text)
