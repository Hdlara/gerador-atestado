from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from datetime import datetime, timedelta
import os
import sys
import tempfile
import webbrowser
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, Label, Entry, Button, StringVar, Radiobutton, ttk, messagebox
from reportlab.pdfgen import canvas
from utils import caminho_recurso

def preencher_com_reportlab_receita(nome, endereco, receita):
    temp_dir = tempfile.mkdtemp()
    overlay_path = os.path.join(temp_dir, "overlay.pdf")
    final_path = os.path.join(temp_dir, f"RECEITUARIO_{nome}.pdf")

    # Cria o overlay com os dados
    c = canvas.Canvas(overlay_path, pagesize=A4)

    # Ajuste as coordenadas conforme seu PDF
    c.drawString(85, 355, nome)
    c.drawString(70, 138, datetime.now().strftime('%d/%m/%Y'))

    c.setFont("Times-Roman", 10)

    if endereco:
        c.drawString(85, 333, endereco)

    linha = 310 - 14.5
    max_chars = 87
    espaco_entre_linhas = 14.5

    for frase in receita:
        if len(frase) <= max_chars:
            c.drawString(35, linha, frase)
            linha -= espaco_entre_linhas
        else:
            split_index = frase.rfind(" ", 0, max_chars)
            if split_index == -1:
                split_index = max_chars

            parte1 = frase[:split_index].strip()
            parte2 = frase[split_index:].strip()

            c.drawString(35, linha, parte1)
            linha -= espaco_entre_linhas
            c.drawString(35, linha, parte2)
            linha -= espaco_entre_linhas

    c.save()

    pdf_modelo_path = caminho_recurso("RECEITUARIO_DIVIDIDO_VERTICAL.pdf")
    original_pdf = PdfReader(open(pdf_modelo_path, "rb"))
    overlay_pdf = PdfReader(open(overlay_path, "rb"))
    writer = PdfWriter()

    original_page = original_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    original_page.merge_page(overlay_page)

    writer.add_page(original_page)
    with open(final_path, "wb") as f_out:
        writer.write(f_out)

    return final_path

    '''# Mescla com o PDF original
    original_pdf = PdfReader(open("RECEITUARIO_DIVIDIDO_VERTICAL.pdf", "rb"))
    overlay_pdf = PdfReader(open(overlay_path, "rb"))
    writer = PdfWriter()

    original_page = original_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    original_page.merge_page(overlay_page)

    writer.add_page(original_page)
    with open(final_path, "wb") as f_out:
        writer.write(f_out)

    return final_path '''

'''lista_frases = [
    '1. Dipirona ou parecetamol tomar      gts de 6/6hs se dor ou febre',
    '2. Acctilcistona (xarope) tomar      ml de 8/8hd caso tosse.', 
    '3. Prodsin 3mg/ml tomar      ml ao dia por 5 dias', 
    '4. NBZ+SF 0.9% 5ml + Clonila (     ) Inalar de 12/12hs x 5 dias',
    '5. Lavagem Nasal com salsep Lavar narina de 03/03hs se necessário',
    'Observação alergico a lactose e ovo'
]

pdf_path = preencher_com_reportlab_receita('Henrique Dias Lara Brito dias junior TERCEIRO', 'Rua jorge bem jor 535', lista_frases)
if pdf_path:
    webbrowser.open(pdf_path)
'''