from flask import Flask, render_template, request, redirect, url_for, flash
import shutil 
import os
import sys
import signal
from gerador_receita import preencher_com_reportlab_receita
from gerador_atestado import preencher_com_reportlab_atestado_unico
from gerador_atestado_duplo import preencher_com_reportlab_atestado_duplo
from datetime import date, datetime
import threading
import webbrowser

app = Flask(__name__)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    nome = request.form.get("nome", "").strip()
    receita = request.form.get("motivo", '').strip()
    observacao = request.form.get("observacao", "").strip()
    acompanhante = request.form.get("acompanhante", "").strip()
    nome_acompanhante = request.form.get("nome-acompanhante", "").strip()
    justificativa = request.form.get("justificativa", 0).strip()
    parentesco = request.form.get("parentesco", "").strip()
    parentesco_atestado = request.form.get("parentesco-atestado", "").strip()
    motivo_outros = request.form.get("motivo-outros-atestado", "").strip()

    imprimir_atestado = request.form.get("imprimir_atestado", "nao").strip()
    imprimir_receita = request.form.get("imprimir_receita", "nao").strip()

    cid = receita
    motivo = ""

    if justificativa == "2":
        motivo = parentesco_atestado
    elif justificativa == "7":
        motivo = motivo_outros

    if cid:
        if cid == "1":
            cid = "A09"
        elif cid == "2":
            cid = "R05"
        elif cid == "3":
            cid = "M79.1"
        elif cid == "4":
            cid = "R50"
        elif cid == "5":
            cid = "J45"
        elif cid == "6":
            cid = "M54"
        elif cid == "7":
            cid = "R05"

    if receita:
        motivos_receitas = [
            [
                '1. Soro de Reidratação oral dar   ml 01/01 hora 07 dias',
                '2. Dipirona ou Paracetamol dar   gotas 06/06 horas. se dor ou febre',
                '3. Simeticona dar   gotas de 8/8 horas, se cólica',
                '4.            Dar   8/8 horas, se vômitos (3 dias)',
                '5. Floratil dar 01 envelope, 12/12 horas, 03 dias',
            ],
            [
                '1. Dipirona ou parecetamol tomar      gts de 6/6hs se dor ou febre',
                '2. Acctilcistona (xarope) tomar      ml de 8/8hd caso tosse.',
                '3. Prodsin 3mg/ml tomar      ml ao dia por 5 dias',
                '4. NBZ+SF 0.9% 5ml + Clonila (     ) Inalar de 12/12hs x 5 dias',
                '5. Lavagem Nasal com salsep Lavar narina de 03/03hs se necessário',
            ],
            [
                '1. Dipirona ou parecetamol dar      gts de 6/6hs se dor ou febre',
                '2. Profenid 20mh/ml dar     gts de 12/12hs x 5 dias.',
                '3. Lavagem Nasal com Salsep 03/03 horas se necessário'
            ],
            [
                'CLavulin 400+57mg/5ml tomar   ml de 8/8hrs. Por   dias '
            ],
            [
                '1. Prednisolona 3ml/ml Tomar   ml 1 vez ao dia 5 dias USO INALATORIO',
                '1. Aerolin NAS CRISES DE TOSSE',
                '2. Clenil HFA   mcg = CONTINUO aplicar   pufs com máscara e espaçador 12/12 horas.'
            ],
            [
                'AZITORMICINA 200mg/ml Tomar   ml ao dia por 5 dias.'
            ],
            [
                '1. NB2+SF 0,9% 3ml + CLENIL 12/12 horas por 5 dias',
                '2. Dipirona    gotas de 6/6horas se febre',
                '3. Desloratadina   ml do dia por 5 dias',
                '4. Lavagem nasal se necessário'
            ]   
        ]
    
        receita = motivos_receitas[int(receita) - 1]

        if observacao:
            receita.append(observacao.lower())

    if not nome or not receita:
        return "Nome e motivo são obrigatórios!", 400
        
    arquivos_para_abrir = []
    pasta_pdf = os.path.join("static", "pdfs")
    os.makedirs(pasta_pdf, exist_ok=True)

    if imprimir_receita == 'sim':
        receita_pdf = preencher_com_reportlab_receita(nome, None, receita)
        # mover ou salvar na pasta_pdf
        novo_caminho = os.path.join(pasta_pdf, f"receita_{datetime.now().timestamp()}.pdf")
        shutil.move(receita_pdf, novo_caminho)
        arquivos_para_abrir.append(f"/static/pdfs/{os.path.basename(novo_caminho)}")

    if imprimir_atestado == 'sim' and acompanhante == "sim":
        atestado_pdf = preencher_com_reportlab_atestado_duplo(nome, motivo, cid, int(justificativa), nome_acompanhante, nome)
        novo_caminho = os.path.join(pasta_pdf, f"atestado_duplo_{datetime.now().timestamp()}.pdf")
        shutil.move(atestado_pdf, novo_caminho)
        arquivos_para_abrir.append(f"/static/pdfs/{os.path.basename(novo_caminho)}")
    elif acompanhante == "sim":
        atestado_pdf = preencher_com_reportlab_atestado_unico(nome_acompanhante, nome, cid, 2)
        novo_caminho = os.path.join(pasta_pdf, f"atestado_acomp_{datetime.now().timestamp()}.pdf")
        shutil.move(atestado_pdf, novo_caminho)
        arquivos_para_abrir.append(f"/static/pdfs/{os.path.basename(novo_caminho)}")
    else:
        atestado_pdf = preencher_com_reportlab_atestado_unico(nome, motivo, cid, int(justificativa))
        novo_caminho = os.path.join(pasta_pdf, f"atestado_{datetime.now().timestamp()}.pdf")
        shutil.move(atestado_pdf, novo_caminho)
        arquivos_para_abrir.append(f"/static/pdfs/{os.path.basename(novo_caminho)}")

    # Renderiza página com script que abre as abas dos PDFs
    return render_template("abrir_pdfs.html", arquivos=arquivos_para_abrir)
