# Gestão de Custos Pessoais

## Descrição

Este projeto é um aplicativo web simples para gerenciamento de custos pessoais. Ele permite cadastrar, visualizar, modificar e deletar custos, além de analisar um extrato bancário em formato CSV para identificar gastos correspondentes aos custos cadastrados. O aplicativo utiliza Flask como framework web, SQLAlchemy para interação com o banco de dados MySQL e templates HTML para a interface do usuário.

## Tecnologias

* **Python:** Linguagem de programação principal.
* **Flask:** Framework web Python.
* **Flask-SQLAlchemy:** Extensão Flask para ORM (Object-Relational Mapping) com SQLAlchemy.
* **SQLAlchemy:** Biblioteca Python para interação com bancos de dados.
* **MySQL:** Sistema de gerenciamento de banco de dados relacional.
* **HTML, CSS:** Para a interface do usuário.
* **Pandas:** Biblioteca Python para manipulação de dados (processamento do CSV).


## Como Executar

1. **Pré-requisitos:**
    * Ter o Python 3 instalado.
    * Instalar as dependências: `pip install -r requirements.txt`
    * Criar um banco de dados MySQL chamado "autonomo" (ou altere as variáveis de configuração em `website/__init__.py`).  Certifique-se de ter um usuário com permissão para criar tabelas neste banco de dados. As credenciais padrão estão configuradas no arquivo `website/__init__.py` como usuário "root" e senha "senha123" (**ALTERE ESSAS CREDENCIAIS PARA UM VALOR SEGURO ANTES DE RODAR A APLICAÇÃO**).
2. **Configurando o banco de dados:**  As credenciais do banco de dados MySQL estão definidas em `website/__init__.py`.  **Modifique-as para refletir suas próprias credenciais.**
3. **Executar o aplicativo:** `python main.py`
4. **Acessar:** Abra seu navegador web e acesse `http://127.0.0.1:5000/`.


## Requisitos

* Python 3.x
* MySQL Server
* Pacotes Python: `Flask`, `Flask-SQLAlchemy`, `SQLAlchemy`, `pandas` (instalados via `pip install -r requirements.txt`)


## Estrutura do Projeto

```
gestão_custos/
├── main.py
└── website/
    ├── __init__.py
    ├── auth.py
    ├── models.py
    └── templates/
        ├── analise.html
        ├── base.html
        ├── custos.html
        ├── modificar_custo.html
        ├── resultado.html
        └── visualizar_custos.html
```

## Funcionalidades

* **Cadastro de Custos:** Permite cadastrar novos custos com tipo, nome, número/código e observação.
* **Visualização de Custos:** Mostra uma lista de todos os custos cadastrados com opções para modificar ou deletar.
* **Edição de Custos:** Permite modificar informações de custos existentes.
* **Deleção de Custos:** Permite deletar custos.
* **Análise de Extrato:** Permite o upload de um arquivo CSV de extrato bancário para identificar e sumarizar gastos relacionados aos custos cadastrados.  O resultado é exibido em uma tabela.


**Observação:** O código para o processamento do arquivo CSV em `/processar_extrato_csv` está incompleto no arquivo `website/auth.py`.  Você precisará implementar a lógica para ler o arquivo, comparar com os dados do banco e gerar o relatório.  O template `resultado.html` já está preparado para exibir os resultados.  Considere usar a biblioteca `pandas` para facilitar o processamento do CSV.