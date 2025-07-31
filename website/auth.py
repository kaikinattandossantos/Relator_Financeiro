# Em website/auth.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Entidade
import pandas as pd
from io import StringIO

auth = Blueprint('auth', __name__)

# --- ROTAS DE EXIBIÇÃO DE PÁGINA (GET) ---

@auth.route('/')
def base():
    # Rota para a página inicial, que pode herdar de base.html
    return render_template('base.html')

@auth.route('/cadastro')
def exibir_formulario_custo():
    """Mostra a página com o formulário de cadastro."""
    return render_template('custos.html')

@auth.route('/visualizar')
def visualizar_dados():
    """Busca todos os custos no banco e os exibe em uma tabela."""
    todos_os_custos = Entidade.query.all()
    return render_template('visualizar_custos.html', custos=todos_os_custos)

@auth.route('/analise')
def pagina_analise():
    """Mostra a página para o usuário fazer o upload do extrato."""
    return render_template('analise.html')

# --- ROTAS DE AÇÃO (POST, DELETE, UPDATE) ---

@auth.route('/cadastrar_entidade_custo', methods=['POST', 'GET'])
def cadastrar_custo():
    """Recebe os dados do formulário e salva um novo custo."""
    if request.method == 'POST':
        tipo = request.form.get('tipo_custo')
        nome = request.form.get('nome_custo')
        numero = request.form.get('numero_custo')
        observacao = request.form.get('observacao')

        nova_entidade = Entidade(tipo=tipo, nome=nome, numero=numero, observacao=observacao)
        db.session.add(nova_entidade)
        db.session.commit()
        flash('Custo cadastrado com sucesso!', 'success')

    # Correção: Redireciona para a lista para ver o novo item
    return render_template('custos.html')

@auth.route('/deletar-custo/<int:id>')
def deletar_custo(id):
    """Deleta um custo específico pelo seu ID."""
    custo_para_deletar = Entidade.query.get_or_404(id)
    db.session.delete(custo_para_deletar)
    db.session.commit()
    flash('Custo deletado com sucesso!', 'success')
    
    return redirect(url_for('auth.visualizar_dados'))

@auth.route('/modificar-custo/<int:id>', methods=['GET', 'POST'])
def modificar_custo(id): # Correção: Nome da função no singular
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    custo = Entidade.query.get_or_404(id)
    if request.method == 'POST':
        custo.tipo = request.form.get('tipo_custo')
        custo.nome = request.form.get('nome_custo')
        custo.numero = request.form.get('numero_custo')
        custo.observacao = request.form.get('observacao')
        db.session.commit()
        flash('Custo atualizado com sucesso!', 'success')
        
        # Correção: Redireciona após o POST
        return redirect(url_for('auth.visualizar_custos'))
        
    return render_template('modificar_custo.html', custo=custo)

@auth.route('/processar_extrato_csv', methods=['POST'])
def processar_extrato_csv():
    """Recebe e processa o arquivo CSV do extrato."""
    file = request.files.get('extrato_csv')
    if not file or file.filename == '':
        flash('Nenhum arquivo selecionado!', 'error')
        return redirect(url_for('auth.pagina_analise'))

    if file.filename.endswith('.csv'):
        try:
            entidades_cadastradas = Entidade.query.all()
            string_do_csv = StringIO(file.stream.read().decode("UTF-8"))
            df_extrato = pd.read_csv(string_do_csv)
            
            resultados = {}
            total_geral_identificado = 0

            for entidade in entidades_cadastradas:
                # CORREÇÃO PRINCIPAL: Usando os nomes de coluna corretos do seu CSV
                transacoes_encontradas = df_extrato[df_extrato['Descrição'].str.contains(entidade.nome, case=False, na=False)]
                
                if not transacoes_encontradas.empty:
                    # CORREÇÃO PRINCIPAL: Usando os nomes de coluna corretos do seu CSV
                    total_gasto = transacoes_encontradas[transacoes_encontradas['Valor'] < 0]['Valor'].sum()
                    
                    if total_gasto != 0:
                        resultados[entidade.nome] = abs(total_gasto)
                        total_geral_identificado += abs(total_gasto)

            return render_template('resultado.html', resultados=resultados, total_geral=total_geral_identificado)

        except Exception as e:
            flash(f'Ocorreu um erro ao processar o arquivo: Verifique os nomes das colunas. Erro: {e}', 'error')
            return redirect(url_for('auth.pagina_analise'))

    flash('Formato de arquivo inválido. Por favor, envie um arquivo .csv', 'error')
    return redirect(url_for('auth.pagina_analise'))