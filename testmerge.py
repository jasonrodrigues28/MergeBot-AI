import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz  # PyMuPDF for PDF handling
from reportlab.pdfgen import canvas
from transformers import pipeline
import os

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text, max_length=200):
    chunks = chunk_text(text)
    summaries = [summarizer(chunk, max_length=max_length, min_length=50, do_sample=False)[0]["summary_text"] for chunk in chunks]
    return " ".join(summaries)

def create_summary_pdf(summary, filename):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "Auto-Generated Summary:")
    y = 780
    for line in summary.split(". "):
        c.drawString(100, y, line + ".")
        y -= 20
    c.save()

def merge_pdfs():
    pdf_files = pdf_list.get(0, tk.END)
    if not pdf_files:
        messagebox.showerror("Error", "No PDFs selected!")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not save_path:
        return
    
    try:
        # Extract and summarize text
        full_text = " ".join([extract_text_from_pdf(pdf) for pdf in pdf_files])
        summary = summarize_text(full_text)
        
        # Create summary PDF
        summary_pdf_path = "summary.pdf"
        create_summary_pdf(summary, summary_pdf_path)
        
        # Merge summary and selected PDFs
        merged_pdf = fitz.open()
        merged_pdf.insert_pdf(fitz.open(summary_pdf_path))
        for pdf in pdf_files:
            merged_pdf.insert_pdf(fitz.open(pdf))
        merged_pdf.save(save_path)
        
        messagebox.showinfo("Success", f"Merged PDF saved at:\n{save_path}")
        os.remove(summary_pdf_path)  # Remove temporary summary PDF
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")

def select_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for file in files:
        if file not in pdf_list.get(0, tk.END):
            pdf_list.insert(tk.END, file)

def remove_selected():
    selected_indices = pdf_list.curselection()
    for i in reversed(selected_indices):
        pdf_list.delete(i)

def on_drop(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith(".pdf") and file not in pdf_list.get(0, tk.END):
            pdf_list.insert(tk.END, file)

# GUI Setup
root = TkinterDnD.Tk()
root.title("MergeBot AI - PDF Summarizer & Merger")
root.geometry("500x450")
root.configure(bg="#2C2F33")

# Buttons
tk.Button(root, text="➕ Select PDFs", command=select_pdfs, bg="#7289DA", fg="white").pack(pady=10)
tk.Button(root, text="❌ Remove Selected", command=remove_selected, bg="#D83C3C", fg="white").pack(pady=5)

# Listbox to display PDFs
pdf_list = tk.Listbox(root, width=60, height=10, bg="#23272A", fg="white", font=("Arial", 10))
pdf_list.pack(pady=10)

# Merge Button
tk.Button(root, text="📄 Merge & Summarize PDFs", command=merge_pdfs, bg="#43B581", fg="white").pack(pady=10)

# Enable Drag & Drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
