import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD  # Drag & Drop support
import fitz  # PyMuPDF for PDF merging
import os

def select_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for file in files:
        if file not in pdf_list.get(0, tk.END):
            pdf_list.insert(tk.END, file)

def remove_selected():
    selected_indices = pdf_list.curselection()
    for i in reversed(selected_indices):  
        pdf_list.delete(i)

def merge_pdfs():
    pdf_files = pdf_list.get(0, tk.END)
    if not pdf_files:
        messagebox.showerror("Error", "No PDFs selected!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not save_path:
        return

    try:
        merged_pdf = fitz.open()
        for pdf in pdf_files:
            merged_pdf.insert_pdf(fitz.open(pdf))
        merged_pdf.save(save_path)
        messagebox.showinfo("Success", f"Merged PDF saved at:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")

def on_drop(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith(".pdf") and file not in pdf_list.get(0, tk.END):
            pdf_list.insert(tk.END, file)

# GUI Setup
root = TkinterDnD.Tk()  # Enables drag & drop support
root.title("MergeBot AI - PDF Merger")
root.geometry("450x400")
root.configure(bg="#2C2F33")

# Buttons
tk.Button(root, text="➕ Select PDFs", command=select_pdfs, bg="#7289DA", fg="white").pack(pady=10)
tk.Button(root, text="❌ Remove Selected", command=remove_selected, bg="#D83C3C", fg="white").pack(pady=5)

# Listbox to display PDFs
pdf_list = tk.Listbox(root, width=60, height=10, bg="#23272A", fg="white", font=("Arial", 10))
pdf_list.pack(pady=10)

# Merge Button
tk.Button(root, text="📄 Merge PDFs", command=merge_pdfs, bg="#43B581", fg="white").pack(pady=10)

# Enable Drag & Drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
