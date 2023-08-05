# -*- coding: utf-8 -*-
'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
import pymysql
import cx_Oracle
import sqlite3
from pymongo import MongoClient
"""Importando bibliotecas internas"""
from Pyautomators.Error import Banco_erro
"""Criando variaveis dos bancos"""
ORACLE,SQLITE,MYSQL,MONGO='Oracle','SQLite','MySQL',"Mongo"
###- annotation:
###    mainTitle: Pyautomators - Classe Relacional
###    text_description1:
###        - "Esta classe tem o intuito de prover conexão e funções de CRUD em Banco de Dados Relacionais.\n"
###        - "Devemos antes de tudo fazer o import da classe para utilização de seus métodos.\n"
###    ex1:
###        - python: "from Pyautomators.banco_de_dados import Relacional"
###    text_description2:
###        - "Feito o import da classe então devemos instacia-la passando os parametros necessarios para utilização de seus metodos.\n"
###    title: "Parametros"
###    text_description3:
###        - "**servidor:str** (Obrigatorio)- Tipo de Servidor de banco de dados que vai trabalhar.\n EXP.: 'Oracle', 'SQLite' e 'MySQL'.\n "
###        - "**user:str -** Usuario de conexão com o servidor\n"
###        - "**senha:str -** Senha de conexão com o servidor\n"
###        - "**banco:str -** O banco de dados na qual iremos nos conectar no servidor\n"
###        - "**endereco:str -** É o endereço na qual vamos usar para nos conectar ao servidor.\nEXP.: URL OU localhost OU 127.0.0.1...\n"
###        - "**porta:int -** É a porta de conexão para o endereço. \nEXP.: 8080, 3601 ...\n"
###    ex2:
###        - python: "BD=Relacional('servidor','user','senha','banco','endereco','porta')"
###        - python: "BD=Relacional('MySQL','root',senha='TestesAutomatizados',banco='World',endereco='10.70.78.15',porta=3306)"
###    exception: "Banco_erro"




class Relacional():
    
    def __init__(self,servidor,user=None,senha=None,banco=None,endereco=None,porta=None):
        """Verifica se o Servidor for valido ele escolher um dos servidores do banco"""
        if (servidor=="MySQL"):
            """Verifica se os parametros foram preenchidos para o Mysql"""
            if(servidor is not None and user is not None and senha is not None and banco is not None and endereco is not None\
               and  porta is not None):
                self.__bank=pymysql.connect(user=user,passwd=senha,db=banco,host=endereco,port=porta,autocommit=True)
                
            else:
                Erro="""Não é um servidor valor valido para MySQL!
                        Valores obrigatorios são:
                        user=usuario que vai ser usado no banco,
                        senha=senha do usuario,
                        banco=banco de dados que sera usado,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        """
                raise Banco_erro(Erro)
        elif (servidor=="Oracle"):
            """Verifica se os parametros foram preenchidos para o Oracle"""
            if(servidor is not None and user is not None and senha is not None and endereco is not None\
               and  porta is not None):
                self.__bank=cx_Oracle.connect('{}/{}@{}{}'.format(user,senha,endereco,porta))
            else:
                Erro="""Não é um servidor valor valido para Oracle!
                        Valores obrigatorios são:
                        user=usuario que vai ser usado no banco,
                        senha=senha do usuario,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        """
                raise Banco_erro(Erro)
            
            
        elif(servidor=="SQLite"):
            """Verifica se os parametros foram preenchidos para o SQLite"""

            if(banco is not None):
                self.__bank=sqlite3.connect(banco)
            else:
                Erro="""Não é um servidor valor valido para SQLite!
                        Valores obrigatorios são:
                        banco=Url ou Arquivo ou :memory:
                        """
                raise Banco_erro(Erro)
        else:
            Erro="\n\nNão é um servidor valido!\nOs servidores validos são: 'Oracle','MySQL' ou 'SQLite'\nInsira um valor correto!"
            raise Banco_erro(Erro)
            
        self.cursor=self.__bank.cursor()
        
    def buscar_tudo(self,query:str):
        Erro='Esta Query é invalida!'
        """verifica a query e retorna todos os dados na query"""
        if(str(query).upper().find('SELECT')!= -1):
            try:
                self.cursor.execute(query)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        return self.cursor.fetchall()
		
###- annotation:
###    title: Métodos
###    text_description1:
###        - "**buscar_tudo(query:str)**:"
###    parameters:
###        - query: ":str" 
###    text_description2:
###        - "Este metodo busca todos os valores de uma tabela, baseado em uma Query."
###    ex1:
###        - python: "buscar_tudo(\"SELECT * FROM 'nome_tabela'\")"
###    return:
###        - List: "retorna uma lista com tuplas de linhas que foram buscadas na tabela"
###    exception: "Banco_erro"

    def buscar_um(self,query:str):
        Erro='Esta Query é invalida!'
        """Verifica a query e retorna somente o primeiro valor"""
        if(str(query).upper().find('SELECT')!= -1):
            try:
                self.cursor.execute(query)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        return self.cursor.fetchone()
		
###- annotation:
###    text_description:
###        - "**buscar_um(query:str)**: "
###    parameters:
###        - query: ":str" 
###    text_description2:
###        - "Este metodo busca um unico valor de uma tabela, baseado em uma Query."
###    ex1:
###        - python: "buscar_um(\"SELECT * FROM 'nome_tabela'\")"
###    return: 
###        -    Tuple: "retorna uma tupla com o primeiro parametro a ser achado na busca"
###    exception: "Banco_erro"

    def inserir_lista(self,sql:str,valores:list):
###- annotation:
###    text_description:
###        - "**inserir_lista(sql:str,valores:list)**:"
###    parameters:
###        - sql: ":str(Obrigátorio)= SQL para inserir valor."
###        - valores: ":list(Obrigatorio)= Lista com tuplas de valores para serem inseridos."
###    text_description2:
###        - "Este metodo inserir diversos valores em uma tabela, baseado em uma script sql."
###    ex:
###        - python: "inserir_lista(\"INSERT INTO {} VALUES ({}, '{}');\",[(\"a\",\"b\",\"c\"),(\"a\",\"b\",\"c\")...])"
###        - python: "inserir_lista('SELECT * FROM city')"
###    exception: "Banco_erro"

        Erro='Esta Query é invalida!'
        """Verifica a query Se é um Insert"""
        if(str(sql).upper().find('INSERT')!= -1):
            try:
                self.cursor.executemany(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit() 
        
        
    def inserir(self,sql:str,valores:tuple):
###- annotation:
###    text_description:
###        - "**inserir(sql:str,valores:tuple)**:"
###    parameters:
###        - sql: ":str(obrigatorio)= SQL para inserir valor."
###        - valores: ":tuple(obrigatorio)= uma tupla de valores para serem inseridos."
###    text_description2:
###        - "Este metodo inseri diversos valores em uma tabela, baseado em uma script , na qual temos os parametros."
###    ex:
###        - python: "inserir(\"INSERT INTO {} VALUES ({}, '{}');\",(\"a\",\"b\",\"c\"))"
###    exception: "Banco_erro"

        Erro='Esta Query é invalida!'
        """Verifica a query Se é um Insert"""
        if(str(sql).upper().find('INSERT')!= -1):
            try:
                self.cursor.execute(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit()
    
    def deletar(self,sql:str,valores:tuple):
###- annotation:
###    text_description:
###        - "**deletar(sql:str,valores:tuple)**:"	
###    parameters:
###        - sql: ":str(obrigatorio)= SQL para deletar valores da tabela."
###        - valores: ":tuple(obrigatorio)= uma tupla de valores para serem deletados."
###    text_description2:
###        - "Este metodo deleta valores em uma tabela, baseado em uma script, na qual temos os parametros."	
###    ex:
###        - python: "deletar(\"DELETE FROM {} WHERE id = {}\",(\"TABELA\",\"3\"))"
###    exception: "Banco_erro"

        Erro='Esta Query é invalida!'
        """Verifica a query Se é um DELETE"""
        if(str(sql).upper().find('DELETE')!= -1):
            try:
                self.cursor.execute(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit()
    
    def atualizar(self,sql:str,valores:tuple):
###- annotation:
###    text_description:
###        - "**atualizar(sql:str,valores:tuple)**:"
###    parameters:
###        - sql: ":str(obrigatorio)= SQL para atualizar valores da tabela."
###        - valores: ":tuple(obrigatorio)= uma tupla de valores para serem atualizados."
###    text_description2:
###        - "Este metodo atualiza valores em uma tabela, baseado em uma script, na qual temos os parametros."
###    ex:
###        - python: "atualizar(\"UPDATE {} SET title = {} WHERE id = {}\",(\"TABELA\",\"x\",\"3\"))"
###    exception: "Banco_erro"

        Erro='Esta Query é invalida!'
        """Verifica a query Se é um UPDATE"""
        result=None
        if(str(sql).upper().find('UPDATE')!= -1):
            try:
                self.cursor.execute(sql.format(*valores))
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        self.__bank.commit()

    def fechar_conexao(self):
###- annotation:
###    text_description:
###        - "**fechar_conexao()**: \nEste metodo fecha conexão com o driver.\n"
###    ex:
###        - python: "fechar_conexao()"
###    text_description2:
###        - "\n\n\n"
        self.cursor.close()
        self.__bank.close()
class Nao_Relacional():
    def __init__(self,Servidor,banco=None,endereco=None,porta=None):       
###- annotation:
###    mainTitle: Pyautomators - Classe Nao_Relacional
###    text_description:
###        - "Esta classe tem o intuito prover conexão e funções de CRUD em banco Não Relacional.\n"
###        - "Devemos antes de tudo fazer o import da classe para utilização de seus métodos.\n"
###    ex1:
###        - python: "from Pyautomators.banco_de_dados import Nao_Relacional"
###    text_description2:
###        - "Feito o import da classe então devemos instacia-la passando os parametros necessarios para utilização de seus metodos.\n"
###    title: "Parametros"
###    text_description3:
###        - "**Servidor:str**(obrigatorio): Tipo de Servidor de banco de dados que vai trabalhar.\nEXP.: 'Mongo'.\n"
###        - "**banco:str:** O banco de dados na qual iremos no conectar no servidor.\n"
###        - "**endereco:str:** É o endereço na qual vamos usar para nos conectar ao servidor.\nEXP.: URL OU localhost OU 127.0.0.1...\n"
###        - "**porta:int:** É a porta de conexão para o endereço. \nEXP.: 8080, 3601 ...\n"
###    ex2:
###        - python: "context.BD=Nao_Relacional('servidor','banco','endereco','porta')"
###        - python: "context.BD=Nao_Relacional('Mongo', 'banco_testes','10.0.0.1' ,8080)"
###    exception: "Banco_erro"
        
        if(Servidor=='Mongo'):
            if(Servidor is not None and banco is not None and endereco is not None and porta is not None):
                self.__con=MongoClient(endereco,porta)
                self.__bank=self.__con[banco]
            else:
                
                Erro="""Não é um servidor valor valido para MongoDB!
                        Valores obrigatorios são:
                        banco=banco de dados que sera usado,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        """
                raise Banco_erro(Erro)
        else:
            Erro="\n\nNão é um servidor valido!\nOs servidores validos são: 'Mongo'\nInsira um valor correto!"
            raise Banco_erro(Erro)  
        
    def buscar(self,dicionario:dict,colecao:str):
###- annotation:	
###    title: Métodos
###    text_description:
###        - "**buscar(dicionario:dict,colecao:str)**:"
###    parameters:
###        - dicionario: ":str=dicionario com chave e valor que queremos procurar."
###        - colecao: ":str=é como uma tabela de banco de dados que queremos procurar."
###    text_description2:
###        - "Este metodo busca o primeiro valor de chaves no banco:"
###        - "O retorno é um dicionario com a chave que foi procurada, na qual temos os parametros."
###    ex:
###        - python: "buscar({\"nome\": \"Radioactive\"},\"testes\")"
###    return:
###        - Dict: "retorna um dicionario com os itens que foram buscados"
###    exception: "Banco_erro"

        Erro='\nColecao ou dicionario invalido!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        result=None
        if(dicionario is not None and colecao is not None):
            try:
                """colecao e em qual base deve ser procurada e dicionario e o json/dicionario que vai procurar"""
                result=self.__bank[colecao].find(dicionario)
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        return result
    
    def buscar_tudo(self,colecao:str):
###- annotation:	
###    text_description:
###        - "**buscar_tudo(colecao:str)**:"
###    parameters:
###        - colecao: ":str=é como uma tabela de banco de dados que queremos procurar."
###    text_description2:
###        - "Este metodo busca todos os valores de chaves no banco:"
###        - "O retorno é um dicionario com a chave que foi procurada, na qual temos os parametros."
###    ex:
###        - python: "buscar_tudo(\"testes\")"
###    return:
###        - List: "retorna uma lisca com dicionarios de itens que foram buscados"
###    exception: "Banco_erro"

        Erro='\nColecao ou dicionario invalido!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        result=None
        if( colecao is not None):
            try:
                """colecao e em qual base deve ser procurada e dicionario e o json/dicionario que vai procurar"""
                result=self.__bank[colecao].find()
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        return result
        
    
    def atualizar(self,colecao,anterior,atual):
###- annotation:	
###    text_description:
###        - "**atualizar(colecao:str,anterior:dict,atual:dict)**:"
###    parameters:
###        - colecao: ":str= colecao da base de dados mongo"
###        - anterior: ":dict= dicionario com chave e valor que queremos procurar para atualizar.\n"
###        - atual: ":dict= e o valor que queremos atualizar.\n"
###    text_description2:
###        - "Este metodo atualiza o todos os  valores de chaves no banco:\n"	
###    ex:
###        - python: "atualizar(\"testes\",{\"_id\": 2},{\"$set\",{\"novo\":\"Novooooo\"}})"
###    exception: "Banco_erro"

        Erro='\nAtualização com sintaxe incorreta!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        if(type(anterior) is dict and type(atual) is dict):
            
            try:
                type(atual['$set'])==dict
                """Set é uma sintaxe do MongoDB, para atualizar um valor os parametros são dicionarios"""
                self.__bank[colecao].update_one(anterior,atual)
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        
        
        
        
    def inserir(self,dicionario,colecao,ids=True):
###- annotation:	
###    text_description:
###        - "**inserir(dicionario:dict,colecao:str,ids:bool=True)**:"
###    parameters:
###        - dicionario: ":dict= dicionario com chave e valor que queremos inserir."
###        - colecao: "colecao da base de dados mongo."
###        - ids: ":bool= True, se vamos inserir um id e False, se o Id vir no dicionario."
###    text_description2:
###        - "Este metodo inseri o todos os  valores de chaves no banco"
###    ex:
###        - python: "inserir({\\"
###        - python: "'nome': 'Nothing left to say',\\ \n'banda': 'Imagine Dragons',\\ \n'categorias':['indie', 'rock'],\\ \n'lancamento': datetime.datetime.now()\\ \n},\"testes\")"
###    exception: "Banco_erro"

        Erro='\nInserção com sintaxe incorreta!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        if(ids==True and type(dicionario)==dict):
            try:
                """Inserindo um dicionario"""
                self.__bank[colecao].insert_one(dicionario).inserted_id
            except:
                raise Banco_erro(Erro)
        elif(ids==False and type(dicionario)==dict):
            try:
                """Inserindo um dicionario"""
                self.__bank[colecao].insert_one(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
    def inserir_lista(self,colecao,lista,ids=True):
###- annotation:	
###    text_description1:
###        - "**inserir_lista(colecao:str,lista:list,ids=True)**:"
###    parameters:
###        - lista: ":list= lista de dicionarios com chave e valor que queremos inserir."
###        - colecao: ":str=colecao da base de dados mongo."
###        - ids: ":bool= True, se vamos inserir um id e False, se o Id vir no dicionario."
###    text_description2:
###        - "Este metodo inseri diversos valores chave no banco."
###    ex:
###        - python: "inserir(\"testes\",{\\"
###        - python: "'nome': 'Nothing left to say',\\ \n'banda': 'Imagine Dragons',\\ \n'categorias':['indie', 'rock'],\\ \n'lancamento': datetime.datetime.now()\\ \n})"
###    exception: "Banco_erro"

        Erro='\nInserção com sintaxe incorreta!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        if(ids==True and type(lista)==dict):
            try:
                """Inserindo um dicionario"""
                self.__bank[colecao].insert_many(lista).inserted_id
            except:
                raise Banco_erro(Erro)
        elif(ids==False and type(lista)==dict):
            try:
                """Inserindo um dicionario"""
                self.__bank[colecao].insert_many(lista)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
        
    def deletar(self,dicionario:dict):
###- annotation:
###    text_description:
###        - "**deletar(dicionario:dict)**:"
###    parameters:
###        - dicionario: ":dict= dicionario de valor que queremos deletar."
###    ex:
###        - python: "deletar({'_id': 1})"
###    exception: "Banco_erro"

        Erro='\nDelete com sintaxe incorreta!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        if(type(dicionario)==dict):
            try:
                """Inserindo um dicionario"""
                self.__bank.delet_one(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
        
    def deletar_tudo(self,dicionario:dict):
###- annotation:
###    text_description:
###        - "**deletar_tudo(dicionario:dict)**:"
###    parameters:
###        - dicionario: ":dict= dicionario de valor que queremos deletar."
###    text_description1:
###        - "Este metodo deletar diversos valores chave no banco."
###    ex:
###        - python: "deletar_tudo({'banda': 'Imagine Dragons'})"	
###    exception: "Banco_erro"

        Erro='\nDelete com sintaxe incorreta!!'
        """Verifica se os valores de entrada são nulos caso seja nulos"""
        if(type(dicionario)==dict):
            try:
                """Removendo todos os dicionarios"""
                self.__bank.delete_many(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)