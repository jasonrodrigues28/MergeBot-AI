import fitz  
from transformers import pipeline
from tqdm import tqdm
import os
 
# Open the first PDF file and merge all the PDF files in the list into a new PDF file called "loop.pdf"
pdf_list = ["a.pdf", "b.pdf"]   #   PUT ALL THE PDF FILES HERE
temp_merge_output = fitz.open()
 
for pdf in pdf_list:
    i = fitz.open(pdf)
    temp_merge_output.insert_pdf(i)
    i.close()

temp_merge_output.save("Merged_pdf_temp.pdf")
temp_merge_output.close()
 
# Function to extract text from a PDF file and return it as a string
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    
    text = "" #empty string to store the text
    
    for page in doc:  
        text += page.get_text("text")
    return text

pdf_text = extract_text_from_pdf("Merged_pdf_temp.pdf")

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
sum_doc = fitz.open()
page = sum_doc.new_page()   # Add a blank page

# Define text and page width constraints
x, y = 50, 50  # Start position
max_width = 400  # Adjust as needed
add_wrapped_text(page, full_summary, x, y, max_width)

sum_doc.save("Summerized.pdf")
sum_doc.close()
print("Summarization successfully.")

# merging the summary document with the merged pdfs
output_file_list = ["Summerized.pdf", "Merged_pdf_temp.pdf"]   #   PUT ALL THE PDF FILES HERE
output_file = fitz.open()
 
for pdf in output_file_list:
    i = fitz.open(pdf)
    output_file.insert_pdf(i)
    i.close()

output_file.save("Output.pdf")  # GIVE YOUR OUTPUT PDF A NAME
output_file.close()

# Delete temporary PDF file
os.remove("Merged_pdf_temp.pdf")  # Remove temporary PDF file
os.remove("Summerized.pdf") # Remove temporary PDF file

print("Process completed")