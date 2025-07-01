from flask import Flask, render_template, request, redirect, url_for
from gerador_receita import preencher_com_reportlab_receita
from gerador_atestado import preencher_com_reportlab_atestado_unico
from gerador_atestado_duplo import preencher_com_reportlab_atestado_duplo
from datetime import date

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
        cid_map = {
            "1": "A09",
            "2": "R05",
            "3": "M79.1",
            "4": "R50",
            "5": "J45",
            "6": "M54",
            "7": "R05"
        }
        cid = cid_map.get(cid, cid)

    motivos_receitas = [
        [...],  # mantenha seu array de receitas aqui
    ]
    
    if receita:
        receita = motivos_receitas[int(receita) - 1]
        if observacao:
            receita.append(observacao.lower())

    if not nome or not receita:
        return "Nome e motivo são obrigatórios!", 400

    # Aqui você pode salvar PDFs no disco ou enviá-los como response (adaptar!)
    # Só evite abrir navegador (webbrowser)

    return redirect(url_for('index'))

# app: objeto que o gunicorn vai usar
