# Top level for program
import re
import subprocess
import sys
from docx import Document
from docx.shared import Inches
"""
    Manaforged makes it easier than ever to automatically
    inflate your income and not leave a paper trail..., ok
    Paul?
    It converts PDFs to WordDocs, or vice versa, and increases
    any numbers found in the document.
"""
# converts pdf to text
def pdf_to_text(pdf_name):
    pdf_content = subprocess.check_output(["./pdf2txt.py", pdf_name])
    return pdf_content

# Need to manaforgize the numbers in here
def text_to_word_doc(text):
    document = Document()
    lines = text.split('\n')
    # print(lines)

    # cleaning up the text
    for line in text.split('\n'):
        ascii_pdf_content = line.decode("utf-8", "replace")
        control_char_map = dict.fromkeys(range(32))
        clean_pdf_content = ascii_pdf_content.translate(control_char_map)
        #look_for_money(clean_pdf_content)
        document.add_paragraph(clean_pdf_content)
    return document

# Text to PDF 
def increase_money(item, multiplier=2):
    item = item.replace("$", "").replace(",", "")
    as_float = float(item)
    as_float *= multiplier 
    as_dollars = '${:,.2f}'.format(as_float)
    return as_dollars

def inflate(pdf_content, multiplier=2):
    money_pattern = "\$+\d*[.,]\d*[..]\d*"
    inflated = [
        increase_money(item, multiplier) 
        if re.search(money_pattern, item) is not None 
        else item for item in pdf_content.split(" ") 
        ] 
    return " ".join(inflated)

if __name__ == "__main__":
    pdf_text =  pdf_to_text(sys.argv[1])
    print(inflate(pdf_text))
    inflated = inflate(pdf_text)
    document = text_to_word_doc(inflated)
    document.save('demo.docx')
