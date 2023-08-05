# -*- coding: utf-8 -*-
'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
import os
import time
from collections import deque
import shutil
"""Importando bibliotecas internas"""
from Pyautomators.Error import Ambiente_erro

###- annotation:
###    mainTitle: Pyautomators - Modulo Ambiente
###    text_description:
###        - "Este modulo tem o intuito de trabalhar em conjunto do sistema operacional,"
###        - "trabalhando com diretorios, arquivos(Nao seus conteudos) e partes do sistema.\n"
###        - "Devemos antes de tudo fazer o import do modulo para utilização de seus métodos.\n"
###    ex:
###        - python: "from Pyautomators import Ambiente\n"

def _tratar_path(diretorio):
    if(type(diretorio)==list):
        """verificando se o diretorio veio como lista de varias path"""
        for arquivo in diretorio:
            arquivo=arquivo.replace("\\", "/")
        dir=diretorio
    else:
        """caso seja uma string ele simplismente retorna as barras como padrão"""
        dir=diretorio.replace("\\", "/")
    return dir

def irDiretorio(diretorio):
    try:
        os.chdir(_tratar_path(diretorio))
    except:
        Erro='\nEste diretorio não existe!'
        raise Ambiente_erro(Erro)
		
###- annotation:
###    title: Funções
###    text_description1:
###        - "**irDiretorio(diretorio:str):**"
###    parameters:
###        - diretorio: ":str= caminho para um diretorio" 
###    text_description2:
###        - "Esta função muda seu diretorio na sua linha de comando para outro diretorio"
###        - "Não ha necessidade de passar o caminho, ou pode se criar outros diretorios dentro de diretorios"
###    ex:
###        - python: "irDiretorio('C:/User/cafe')"
###        - python: "irDiretorio(r'C:/User/cade')"
###    exception: "Ambiente_erro"

def criarPasta(nomePasta):
###- annotation:
###    text_description1:
###        - "**criarPasta(nomePasta:str):**"
###    parameters:
###        - nomePasta: ":str= nome da pasta" 
###    text_description2:
###        - "Esta função cria um diretorio"
###    ex:
###        - python: "criarPasta('C:/User/NovaPasta')"
###        - python: "criarPasta('NovaPasta')"
###    exception: "Ambiente_erro"

    try:
        os.mkdir('./'+nomePasta)
    except:
        Erro='\nEste diretorio já existe!'
        raise Ambiente_erro(Erro)




def abrirPrograma(programa):
###- annotation:
###    text_description1:
###        - "**abrirPrograma(programa:str):** "
###    parameters:
###        - programa: ":str= caminho do programa" 
###    text_description2:
###        - "Esta função executa um programa(que for executavel como permissao)."
###    ex:
###        - python: "abrirPrograma('C:\\Program Files (x86)\\Notepad++\\notepad++.exe')"
###    exception: "Ambiente_erro"

    try:
        os.startfile(_tratar_path(programa))
    except:
        Erro='\nNão foi possivel encontrar ou não existe este programa!'
        raise Ambiente_erro(Erro)   

def comandLine(command):
    os.system(command)
	
###- annotation:
###    text_description1:
###        - "**comandLine(command:str):** "
###    parameters:
###        - command: ":str= comando" 
###    text_description2:
###        - "Esta função executa uma instrução na linha de comando, dentro do seu diretorio atual."
###    ex:
###        - python: "comandLine('mkdir novaPasta')"



def dia_mes_ano():
    """
        retira data local do sistema
        adiciona em uma lista todos os dados
        Cria um objeto pilha
        faz a interação com a pilha
        adiciona os tres primeiros valores da lista (dia, mes , ano), e no final discarta as outras informações
        """
    line=time.localtime()
    line=list(line)
    lis=deque()
    for h in line:
        lis.appendleft(int(h))
        if(line.index(h) == 2):
            break
    return list(lis)
	
###- annotation:
###    text_description1:
###        - "**dia_mes_ano():** .\n"
###    text_description2:
###        - "Esta função retorna o dia, mes e ano da sua maquina.\n"
###    ex:
###        - python: "valor=dia_mes_ano() \nprint(valor) \n >>>[16,7,2018]"
###    return:
###        - List: "Data atual que esta no sistema operacional ques esta sendo executado, sendo uma lista com dia, mes e ano"

def path_atual(Com_seu_diretorio=True):
    diretorio=None
    """se o parametro: Com_seu_diretorio for True, Ele pega sua path atual, caso seja false o valor será de somente o caminho ate o diretorio """
    if(Com_seu_diretorio):
        diretorio=_tratar_path(str(os.getcwd()))
    elif(not Com_seu_diretorio):
        diretorio=_tratar_path(str(os.path.dirname(os.getcwd())))
        
    return diretorio+"/"
	
###- annotation:
###    text_description1:
###        - "**path_atual(Com_seu_diretorio:str=True):**"
###    parameters:
###        - Com_seu_diretorio: ":str= comando" 
###    text_description2:
###        - "Esta função retorna o caminho ate o seu diretorio, com False a sua pasta atual da path, retornando somente o caminho.\ncom False a sua pasta atual da path, retornando somente o caminho.\n"
###    ex:
###        - python: "path=path_atual()\nprint(path)\n>>>C:/User/administrador/[pastaAtual]/ \nOU \npath=path_atual(False) \nprint(path) \n>>>C:/User/administrador/"
###    return:
###        - String: "o diretorio que esta ou o caminho ate ele."
def copiar_aquivos_diretorio(path_arquivo1:str,path_arquivo2:str):
    Erro=r'''
        Para copiar um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do arquivo alvo
        Exemplo:
        copiar_aquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/Cenario.txt")'''
    path_arquivo1=_tratar_path(path_arquivo1)
    path_arquivo2=_tratar_path(path_arquivo2)
    if(type(path_arquivo1) == str and type(path_arquivo2) == str):
        try:
            shutil.copyfile(path_arquivo1, path_arquivo2)
        except:
            raise Ambiente_erro(Erro)
    else:
        
        raise Ambiente_erro(Erro)

###- annotation:
###    text_description1:
###        - "**copiar_aquivos_diretorio(path_arquivo1:str,path_arquivo2:str)**:"
###    parameters:
###        - path_arquivo1: ":str= arquivo que sera retirado o conteudo" 
###        - path_arquivo12: ":str= arquivo que sera enviado o conteudo" 
###    text_description2:
###        - "Esta função copia o conteudo de um arquivo para outro arquivo, \npassando o caminho conseguimos colocar em outro.\nPara copiar um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do arquivo alvo."
###        - "Para copiar um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do arquivo alvo."
###    ex:
###        - python: "copiar_aquivos_diretorio(r\"C:\\Users\\administrador\\Desktop \\Cenarios.txt\", \"Features/Cenario.txt\")"
###    exception: "Ambiente_erro"
    
def mover_arquivos_diretorio(path_arquivo1:str,path_2:str):
    r'''Esta função move o conteudo de um arquico para outro diretorio
    Exemplo::
    mover_arquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/")'''
    Erro=r'''
        Para mover um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do diretorio alvo
        Exemplo:
        mover_arquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/")'''
    path_arquivo1=_tratar_path(path_arquivo1)
    path_arquivo2=_tratar_path(path_2)
    if(type(path_arquivo1) == str and type(path_2) == str):
        try:
            shutil.move(path_arquivo1, path_arquivo2)
        except:
            raise Ambiente_erro(Erro)
    else:
        
        raise Ambiente_erro(Erro)
		
###- annotation:
###    text_description1:
###        - "**mover_arquivos_diretorio(path_arquivo1:str,path_2:str)**:"
###    parameters:
###        - path_arquivo1: ":str= arquivo que sera retirado o conteudo" 
###        - path_2: ":str= path do diretorio que sera enviado" 
###    text_description2:
###        - "Esta função move o conteudo de um arquivo para outro diretorio.\n"
###    ex:
###        - python: "mover_arquivos_diretorio(r\"C:\\Users\\administrador\\Desktop\\Cenarios.txt\", \"Features/\")"
###    exception: "Ambiente_erro"
        
def remover_arquivo(NomeArquivo:str):
    NomeArquivo=_tratar_path(NomeArquivo)
    try:
        os.remove(NomeArquivo)
    except:
        Erro='''Este arquivo ou diretorio não existe!!'''
        raise Ambiente_erro(Erro)
		
###- annotation:
###    text_description1:
###        - "**remover_arquivo(NomeArquivo:str)**:"
###    parameters:
###        - NomeArquivo: ":str= arquivo que sera excluido" 
###    text_description2:
###        - "Esta função exclui um arquivo."
###    ex:
###        - python: "remover_arquivo('arquivo.txt')\n OU\n remover_arquivo('base/arquivo.txt')"
###    exception: "Ambiente_erro"
		
