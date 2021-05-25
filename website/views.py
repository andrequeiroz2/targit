import numpy as np
import pandas as pd
from .controller import cep_search
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, request, flash, redirect, url_for


views = Blueprint('views', __name__)

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    df = pd.read_csv('data/clientes.csv', dtype=object, sep=';')
    df = df.replace(np.nan, '', regex=True)
    return render_template('clientes.html', df=df, titles=df.columns.values)


## -- CADASTRO --
@views.route('/cadastro', methods=['GET','POST'])
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    ## TODO pegar informações do forms
    if request.method == 'POST':
        
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        cep = request.form["cep"]

        # Validate.
        if not nome:
            flash('Imput your Name.', 'error')
            return render_template('cadastro.html')

        if not sobrenome:
            flash('Imput your Last Name.', 'error')
            return render_template('cadastro.html')
        
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash('Imput your Valid Email.', 'error')
            return render_template('cadastro.html')

        if not cep:
            flash('Imput your Valid CEP.', 'error')
            return render_template('cadastro.html')
        
        if len(cep)>8:
            flash('Invalid CEP.', 'error')
            return render_template('cadastro.html')

        ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
        result = cep_search(cep)

        if "erro" in result:
            flash('Invalid CEP.', 'error')
            return render_template('cadastro.html')
        
        ## TODO criar nova linha no arquivo csv
        #nome;sobrenome;email;cep;logradouro;complemento;bairro;localidade;uf;ibge;gia;ddd;siafi
        cep=result["cep"]
        logradouro=result["logradouro"]
        complemento=result["complemento"]
        bairro=result["bairro"]
        localidade=result["localidade"]
        uf=result["uf"]
        ibge=result["ibge"]
        gia=result["gia"]
        ddd=result["ddd"]
        siafi=result["siafi"]
        
        inf = pd.DataFrame(data=[
                            [
                                nome,
                                sobrenome,
                                email,
                                cep,
                                logradouro,
                                complemento,
                                bairro,
                                localidade,
                                uf,
                                ibge, 
                                gia, 
                                ddd,
                                siafi
                            ]
                                ],
                        columns=[
                            "nome",
                            "sobrenome",
                            "email",
                            "cep",
                            "logradouro",
                            "complemento",
                            "bairro",
                            "localidade",
                            "uf",
                            "ibge",
                            "gia",
                            "ddd",
                            "siafi"])
        
        inf.to_csv('data/clientes.csv',
                    index=False,
                    header=False,
                    mode='a',
                    sep=';')
        return redirect(url_for('views.clientes'))
    return render_template('cadastro.html')


## -- CONSULTA CEP --
@views.route('/consulta-cep', methods=['GET','POST'])
def consulta_cep():
    ## TODO pegar CEP do forms
    if request.method == 'POST':

        #validate
        input = request.form["cep"]

        if not input:
            flash('Imput your valid CEP.', 'error')
            return render_template('consulta_cep.html')
        
        if len(input)>8:
            flash('Invalid CEP.', 'error')
            return render_template('consulta_cep.html')
        
        ## TODO buscar informações de endereço da API do ViaCEP (https://viacep.com.br/)
        result = cep_search(input)

        if "erro" in result:
            flash('Invalid CEP.', 'error')
            return render_template('consulta_cep.html')
        
        return render_template('consulta_cep.html', 
                                cep=result["cep"],
                                logradouro=result["logradouro"],
                                complemento=result["complemento"],
                                bairro=result["bairro"],
                                localidade=result["localidade"],
                                uf=result["uf"],
                                ibge=result["ibge"],
                                gia=result["gia"],
                                ddd=result["ddd"],
                                siafi=result["siafi"]
                            )

    return render_template('consulta_cep.html')