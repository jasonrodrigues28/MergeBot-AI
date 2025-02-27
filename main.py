import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF for PDF merging

def select_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for file in files:
        pdf_list.insert(tk.END, file)  # Add selected PDFs to the list box

def merge_pdfs():
    pdf_files = pdf_list.get(0, tk.END)  # Get all files in the list
    if not pdf_files:
        messagebox.showerror("Error", "No PDFs selected!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not save_path:
        return  # User cancelled save

    try:
        merged_pdf = fitz.open()  # Create a blank PDF
        for pdf in pdf_files:
            merged_pdf.insert_pdf(fitz.open(pdf))  # Merge each PDF
        merged_pdf.save(save_path)
        messagebox.showinfo("Success", f"Merged PDF saved at:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs: {e}")

# GUI Setup
root = tk.Tk()
root.title("MergeBot AI - PDF Merger")
root.geometry("400x350")

tk.Button(root, text="Select PDFs", command=select_pdfs).pack(pady=10)
pdf_list = tk.Listbox(root, width=50, height=8)
pdf_list.pack()

tk.Button(root, text="Merge PDFs", command=merge_pdfs).pack(pady=10)

root.mainloop()
