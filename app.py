from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route('/shutdown', methods=['POST'])
def shutdown():
    threading.Thread(target=fechar_app).start()
    return redirect("https://www.google.com")

def fechar_app():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    else:
        os.kill(os.getpid(), signal.SIGTERM)
    sys.exit()

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
           
    if imprimir_receita == 'sim':
        receita_pdf = preencher_com_reportlab_receita(nome, None, receita)
        webbrowser.open(receita_pdf)
    
    if imprimir_atestado == 'sim' and acompanhante == "sim":
        atestado_pdf = preencher_com_reportlab_atestado_duplo(nome, motivo, cid, int(justificativa), nome_acompanhante, parentesco)
        webbrowser.open(atestado_pdf)
    elif acompanhante == "sim":
        atestado_pdf = preencher_com_reportlab_atestado_unico(nome_acompanhante, parentesco, cid, 2)
        webbrowser.open(atestado_pdf)
    else:
        atestado_pdf = preencher_com_reportlab_atestado_unico(nome, motivo, cid, int(justificativa))
        webbrowser.open(atestado_pdf)



    #flash("Receita e atestado gerados com sucesso!")
    return redirect(url_for('index'))

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

def encerrar_servidor():
    print("Encerrando servidor após 1 minuto...")
    os._exit(0)  

if __name__ == "__main__":

    data_limite = date(2025, 7, 1)
    hoje = date.today()
    if hoje > data_limite:
        sys.exit()

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1, abrir_navegador).start()
        threading.Timer(54000, encerrar_servidor).start()

    app.run(debug=True)  

