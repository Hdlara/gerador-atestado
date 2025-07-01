from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime, timedelta
import os
import tempfile
import webbrowser
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, Label, Entry, Button, StringVar, Radiobutton, ttk, messagebox
from reportlab.pdfgen import canvas
from utils import caminho_recurso


def preencher_com_reportlab_atestado_unico(nome, motivo, cid, tipo):
    temp_dir = tempfile.mkdtemp()
    overlay_path = os.path.join(temp_dir, "overlay.pdf")
    final_path = os.path.join(temp_dir, f"Atestado_{nome}.pdf")

    # Cria o overlay com os dados
    c = canvas.Canvas(overlay_path, pagesize=A4)

    # Ajuste as coordenadas conforme seu PDF
    c.drawString(120, 660, nome)
    c.drawString(100, 612, datetime.now().strftime('%d/%m/%Y'))
    
    # hora atual menos 30 minutos
    hora_menos_30 = datetime.now() - timedelta(minutes=30)

    # formatar para string no formato HH:MM
    hora_formatada = hora_menos_30.strftime('%H:%M')

    # desenhar no PDF
    c.drawString(300, 613, hora_formatada)
    c.drawString(350, 592, datetime.now().strftime('%H:%M'))

    
    if tipo == 1:
        c.drawString(75.5, 524, 'X')
    elif tipo == 2:
        c.drawString(75.5, 500, 'X')
        c.drawString(232, 502, motivo)
    elif tipo == 3:
        c.drawString(75.5, 478, 'X')
    elif tipo == 4:
        c.drawString(75.5, 456, 'X')
    elif tipo == 5:
        c.drawString(75.5, 434, 'X')
    elif tipo == 6:
        c.drawString(75.5, 412, 'X')
    elif tipo == 7:
        c.drawString(75.5, 388, 'X')
        c.drawString(130, 389, motivo)

    if cid:
        c.drawString(100, 333, cid)

    c.save()

    pdf_modelo_path = caminho_recurso("ATESTADO_1.pdf")
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

'''
# O resto do código permanece igual...
motivos_cids = {
    "Diarreia": "A09",
    "Dor de cabeça": "R51",
    "Febre": "R50",
    "Gripe": "J11",
    "Dor nas costas": "M54",
    "Consulta Médica": ""
}

pdf_path = preencher_com_reportlab('henrique dias lara brito dias junior TERCEIRO', 'FILHO', 'R11', 'acompanhante', 'nome_acompanhante')
if pdf_path:
    webbrowser.open(pdf_path)



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
        pdf_path = preencher_com_reportlab(nome, motivo, cid, acompanhante, nome_acompanhante)
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
'''