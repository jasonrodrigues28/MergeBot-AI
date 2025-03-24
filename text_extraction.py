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
full_summary = "" # store the entire summary
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

for chunk in tqdm(chunks, desc="Summarizing: "):
    summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
    full_summary += summary[0]['summary_text'] + " "

# Function to add wrapped text to the PDF
def add_wrapped_text(page, text, x, y, max_width, line_spacing=15):
    tw = fitz.TextWriter(page.rect)  # Create a TextWriter for the page
    words = text.split(" ")
    line = ""
    y_position = y  

    for word in words:
        test_line = line + word + " "

        # Check if adding the word exceeds max_width
        if fitz.get_text_length(test_line, fontsize=12) < max_width:
            line = test_line
        else:
            tw.append((x, y_position), line, fontsize=12)
            y_position += line_spacing  # Move to the next line
            line = word + " "

    if line:
        tw.append((x, y_position), line, fontsize=12)

    # Apply the text writer to the page
    tw.write_text(page)

# creating summary PDF
doc = fitz.Document()   # Create a new PDF document
page = doc.new_page()   # Add a blank page

# Define text and page width constraints
x, y = 50, 50  # Start position
max_width = 400  # Adjust as needed
add_wrapped_text(page, full_summary, x, y, max_width)

doc.save("summarized-text.pdf")
doc.close()

print("Summarization and PDF creation completed successfully.")