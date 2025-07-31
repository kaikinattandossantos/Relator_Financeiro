from flask import Blueprint, redirect, render_template, request, url_for
from . import db   
from .models import Entidade

import pandas as pd
from io import StringIO

auth = Blueprint('auth', __name__)


@auth.route('/salvar-entidade-custo', methods=['GET', 'POST'])
def salvar_custo():
    if request.method == 'POST':
        tipo = request.form.get('tipo_custo')
        nome = request.form.get('nome_custo')
        numero = request.form.get('numero_custo')
        observacao = request.form.get('observacao')

        nova_entidade = Entidade(tipo=tipo, nome=nome, numero=numero, observacao=observacao)
        db.session.add(nova_entidade)
        db.session.commit()

    return render_template('custos.html')



@auth.route('/visualizar')
def cadastro_form():
    todos_os_custos = Entidade.query.all()
    

    return render_template('visualizar_custos.html', custos=todos_os_custos)


@auth.route('/deletar_custo/<int:id>')
def deletar_custo(id):
    custo_para_deletar = Entidade.query.get_or_404(id)

    db.session.delete(custo_para_deletar)
    db.session.commit()

    return redirect(url_for('auth.cadastro_form'))



@auth.route('/modificar_custo/<int:id>', methods=['GET', 'POST'])
def modificar_custos(id):
    custo = Entidade.query.get_or_404(id)
    if request.method == 'POST':
        custo.tipo = request.form.get('tipo_custo')
        custo.nome = request.form.get('nome_custo')
        custo.numero = request.form.get('numero_custo')
        custo.observacao = request.form.get('observacao')

        db.session.commit()
    
    return render_template('modificar_custo.html', custo=custo)



