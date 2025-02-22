import fitz

firstPDF = fitz.open("testDoc.pdf")
pdf_list = ["testDoc2.pdf", "merged.pdf"]


for pdf in pdf_list:
    i = fitz.open(pdf)
    firstPDF.insert_pdf(i)

firstPDF.save("loop.pdf")
