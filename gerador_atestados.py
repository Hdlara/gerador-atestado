import os
import tempfile
import webbrowser
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar, Radiobutton, ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from PyPDF2 import PdfReader, PdfWriter
from utils import caminho_recurso

def gerar_atestado(nome, motivo, cid, acompanhante, nome_acompanhante):
    # Criar um PDF temporário com as informações
    temp_dir = tempfile.mkdtemp()
    temp_pdf_path = os.path.join(temp_dir, "temp.pdf")
    
    # Criar um canvas para adicionar as informações
    c = canvas.Canvas(temp_pdf_path)
    
    # Configurações de fonte
    c.setFont("Helvetica", 10)
    
    # Posições dos campos (você precisará ajustar conforme seu template)
    campos_posicoes = {
        'Paciente': (150, 650, nome),
        'Data': (150, 630, datetime.now().strftime('%d/%m/%Y')),
        'Hora de chegada': (300, 630, datetime.now().strftime('%H:%M')),
        'Hora De saída': (400, 630, datetime.now().strftime('%H:%M')),
        'CID': (150, 610, cid),
        'Paciente_2': (150, 590, nome),
        'Acompanhante': (150, 570, nome_acompanhante if acompanhante == "sim" else ""),
        'Motivo': (150, 550, motivo)
    }
    
    # Desenhar os textos nas posições corretas
    for campo, (x, y, valor) in campos_posicoes.items():
        if valor:  # Só desenha se houver valor
            c.drawString(x, y, str(valor))
    
    # Marcar os checkboxes conforme o motivo
    if motivo == "Consulta Médica":
        c.drawString(100, 530, "X")  # Posição do checkbox "Consulta Médica"
    else:
        c.drawString(100, 510, "X")  # Posição do checkbox "Não estava em condições"
    
    if acompanhante == "sim":
        c.drawString(100, 490, "X")  # Posição do checkbox "Acompanhante"


    c.save()
    
    pdf_modelo_path = caminho_recurso("ATESTADO.pdf")
    template = PdfReader(open(pdf_modelo_path, "rb"))
    overlay = PdfReader(open(temp_pdf_path, "rb"))
    writer = PdfWriter()

    original_page = template.pages[0]
    overlay_page = overlay.pages[0]
    original_page.merge_page(overlay_page)

    writer.add_page(original_page)
    with open(temp_pdf_path, "wb") as f_out:
        writer.write(f_out)

    return temp_pdf_path

# O resto do código permanece igual...
motivos_cids = {
    "Diarreia": "A09",
    "Dor de cabeça": "R51",
    "Febre": "R50",
    "Gripe": "J11",
    "Dor nas costas": "M54",
    "Consulta Médica": ""
}

def gerar():
    nome = nome_var.get().strip()
    motivo = motivo_var.get()
    acompanhante = acomp_var.get()
    nome_acompanhante = acomp_nome_var.get().strip()

    if not nome:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do paciente!")
        return
    
    if acompanhante == "sim" and not nome_acompanhante:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do acompanhante!")
        return
    
    cid = motivos_cids.get(motivo, "")
    
    try:
        pdf_path = gerar_atestado(nome, motivo, cid, acompanhante, nome_acompanhante)
        if pdf_path:
            webbrowser.open(pdf_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar atestado: {str(e)}")

# GUI (mantida igual)
root = Tk()
root.title("Gerador de Atestado Médico")
root.geometry("500x250")

nome_var = StringVar()
motivo_var = StringVar()
acomp_var = StringVar(value="não")
acomp_nome_var = StringVar()

Label(root, text="Nome do Paciente:").grid(row=0, column=0, sticky="w")
Entry(root, textvariable=nome_var).grid(row=0, column=1, columnspan=2)

Label(root, text="Motivo:").grid(row=1, column=0, sticky="w")
combo = ttk.Combobox(root, textvariable=motivo_var, values=list(motivos_cids.keys()), state="readonly")
combo.grid(row=1, column=1, columnspan=2)
combo.current(0)

Label(root, text="Atestado para acompanhante?").grid(row=2, column=0, sticky="w")
Radiobutton(root, text="Sim", variable=acomp_var, value="sim", command=lambda: toggle_acomp_field()).grid(row=2, column=1, sticky="w")
Radiobutton(root, text="Não", variable=acomp_var, value="não", command=lambda: toggle_acomp_field()).grid(row=2, column=2, sticky="w")

acomp_nome_label = Label(root, text="Nome do Acompanhante:")
acomp_nome_entry = Entry(root, textvariable=acomp_nome_var)

def toggle_acomp_field():
    if acomp_var.get() == "sim":
        acomp_nome_label.grid(row=3, column=0, sticky="w")
        acomp_nome_entry.grid(row=3, column=1, columnspan=2)
    else:
        acomp_nome_label.grid_remove()
        acomp_nome_entry.grid_remove()

# Botões
Button(root, text="Gerar Atestado", command=gerar).grid(row=4, column=1)
Button(root, text="Sair", command=root.destroy).grid(row=4, column=2)

toggle_acomp_field()  # Inicializa visibilidade
root.mainloop()