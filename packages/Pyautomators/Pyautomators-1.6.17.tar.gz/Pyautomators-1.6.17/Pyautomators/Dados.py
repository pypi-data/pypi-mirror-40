# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
"""Importando bibliotecas externas"""
import yaml
import json
import pytesseract as ocr
from PIL import Image
import pyautogui
import pandas
import os
"""Importando bibliotecas internas"""
from Pyautomators.Error import Dado_erro

###- annotation:
###    mainTitle: Pyautomators - Módulo Dados
###    text_description:
###        - "Este modulo tem o intuito de trabalhar com dados de entrada para teste, trabalhando com a entrada dos dados para o teste.\n"
###        - "Devemos antes de tudo fazer o import da classe para utilização de seus métodos.\n"
###    ex:
###        - python: "from Pyautomators import Dados"

def tela_texto(xi:int, yi:int, xf:int, yf:int,renderizacao=False,x=-1,y=-1,limpar=True,language="eng")->str:
###- annotation:
###    title: Funções
###    text_description1:
###        - "**tela_texto**(xi:int, yi:int, xf:int, yf:int,renderizacao=False,x=-1,y=-1,limpar=True,language='eng')->str:"
###    parameters:
###        - xi-yi-xf-yf: ":int(obrigatorio)= pontos para retangular o local que será retirado a informação."
###        - renderizacao: ":bool= Se o valor for True, então irá renderizar a imagem para um tamanho de leitura melhor do Tesseract."
###        - x-y-: ":int= Tamanho da foto Renderizada."
###        - limpar: ":bool= Exclui a imagem após utilização."
###        - language: ":str= Linguagem para tradução."
###    text_description2:
###        - "Esta função retira de um ponto expecifico da tela um valor apartir dos pontos inicias xi:yi, traçado um contorno ate xf:yf"
###        - "em uma tela, a mesma retira um print podendo renderizar o tamanho da informação para melhorar a captura do dado.\n"
###    ex:
###        - python: "tela_texto(1,100,50,200,True,200,300,False)"
    """
    formando a função lambda de subtração
    gerano a subtração dos pontos, para achar a largura e altura
    verifica se os pontos são inteiros e se não são negativos
    cria o arquivo temporario para retirar o valor da imagem
    retirando o print da tela e guardando no arquivo temporario
    caso renderização seja true ele começa o prSocesso de ajuste da imagem
    verifica se os valores de x e y são menores que 0
    abre a imagem e renderiza e salva novamente
    Abre a imagem 
    Retira a string da imagem
    Caso o parametro limpar sejá True, a imagem e descartada
    """
    result=lambda a,b:b-a 
    xd=result(xi,xf)
    yd=result(yi,yf)
    if((type(xd) is float) or (type(yd) is float) or xd<=0 or yd<=0):
        Erro="""
                Os Valores de xi:yi e xf:yf estão errados
                tente seguir este padrão e contruir com valores inteiros:
                xf>xi
                Yf>yi"""
        raise Dado_erro(Erro)
    nome="teste.png"
    pyautogui.screenshot(nome,region=(xi,yi,xd,yd))
    if(renderizacao==True ):
        #
        if(y<=0 or x<=0):
            Erro="""
                    Os Valores de x:y estão errados
                    tente seguir e contruir com valores positivos
                    """
            raise Dado_erro(Erro)
        else:
            #
            im = Image.open(nome)
            ims=im.resize((x, y),Image.ANTIALIAS)
            ims.save(nome,'png')
    im=Image.open(nome)    
    valor=ocr.image_to_string(im,lang=language)
    if(limpar):
        #remove a imagem
        os.remove(nome)
    return valor
    
def pegarConteudoJson(NomeArquivo):
###- annotation:
###    text_description:
###        - "**pegarConteudoJson(NomeArquivo:str)**:"
###    parameters:
###        - NomeArquivo: "str: =:Nome do arquivo Json."
###    text_description1:
###        - "Esta função retira o conteúdo de um json e retorna a um Dicionario"
###    ex:
###        - python: "pegarConteudoJson('valor.json')"
    """
    Vai Abrir o conteudo e vai retornar o json como dicionario
    Carregando conteudo para dicionarios"""
    arquivo = open(NomeArquivo.replace("\\","/"), 'r')
    lista = arquivo.read()
    arquivo.close()    
    jso=json.loads(lista)  
    return dict(jso)


def pegarConteudoCSV(NomeArquivo:str):
###- annotation:
###    text_description:
###        - "**pegarConteudoCSV(NomeArquivo:str)**:"
###    parameters:
###        - NomeArquivo: ":str= Nome do arquivo CSV."
###    text_description1:
###        - "Esta função retira o conteudo de um CSV e retorna um DataFrame."
###    ex:
###        - python: "pegarConteudoCSV('valor.csv')"
    """Vai abrir o conteudo e vai retornar um dataframe"""
    valor=pandas.read_csv(NomeArquivo)
    valor=pandas.DataFrame(valor)
    return valor
    
def pegarConteudoXLS(NomeArquivo:str,Planilha:str):
###- annotation:
###    text_description:
###        - "**pegarConteudoXLS(NomeArquivo:str,Planilha:str)**:"
###    parameters:
###        - NomeArquivo: ":str=Nome do arquivo XLS."
###        - Planilha: ":str= Qual planilha dese ser retirado o conteudo"
###    text_description1:
###        - "Esta função retira o conteudo de um Excel e retorna a um DataFrame."
###    ex:
###        - python: "pegarConteudoXLS('valor.xls','Planilha1')"
    """Vai abrir o conteudo e vai retornar um dataframe"""
    valor=pandas.read_excel(NomeArquivo,sheet_name=Planilha)
    valor=pandas.DataFrame(valor)
    return valor

def pegarConteudoYAML(NomeArquivo):
###- annotation:
###    text_description:
###        - "**pegarConteudoYAML(NomeArquivo:str)**:"
###    parameters:
###        - NomeArquivo: ":str= Nome do arquivo YAML."
###    text_description1:
###        - "Esta funcao retira o conteudo de um yaml e retorna um dict."
###    ex:
###        - python: "pegarConteudoYAML('teste.yaml')"
    """Vai Abrir o conteudo e vai retornar o json como dicionario"""
    arquivo=open(NomeArquivo,"r")
    return yaml.load(arquivo)