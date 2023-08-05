# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
"""Importando bibliotecas externas"""
import os 
from selenium import webdriver 
import subprocess
"""Importando bibliotecas internas"""
from Pyautomators.mouse_teclado import Teclado
from Pyautomators.mouse_teclado import Mouse
from Pyautomators.Verifica import Valida
from Pyautomators.Error import Elemento_erro

###- annotation:
###    mainTitle: Pyautomators - Classe Desk
###    text_description:
###        - "Esta classe tem metodos de selenium para Desktop em conjunto de metodos que simulam mouse e teclado, para visão de usuario, na qual passamos um elemento chave e seu tipo e ele executa a ação descrita.\n"
###        - "Devemos antes de tudo fazer o import da classe para utilização de seus métodos.\n"
###    ex:
###        - python: "from Pyautomators.desk import Desk"
###    text_description1:
###        - "Depois instancie a classe e passe os parametros necessarios.\n"
###        - "**Parametros:**\n"
###        - "**aplicacao:str**(Obrigatorio): Qual aplicação será testada.\n"
###        - "**Driver_Winium:str:**Local Aonde esta o Driver do Winium.\n"
###    text_description2:
###        - "**Exteções:**"
###    unorderedList1:
###        - Teclado
###        - Mouse
###        - Valida
###    ex1:
###        - python: "context.app = desk('aplicacao',Driver_Winium='Winium.Desktop.Driver.exe')"


class Desk(Teclado,Mouse,Valida):
    def __init__(self,aplicacao:str,Driver_Winium="Winium.Desktop.Driver.exe"):
        """Ira abrir um subprocesso, em background para o driver"""
        self.sub=subprocess.Popen(Driver_Winium)
        """Ira abrir o webdriver desktop, com o nome da aplicação"""
        self.driver= webdriver.Remote(command_executor="http://localhost:9999",desired_capabilities={"app": aplicacao})
        
    @staticmethod
    def Open_comandLine(Comand):
###- annotation:
###    title: Metodos
###    text_description:
###        - "**open_comandLine(Comand):**"
###    parameters:
###        - Comand: ":str(obrigatorio)= Comando."
###    text_description1:
###        - "Este metodo abre a aplicação apartir de uma linha de comando."
###    ex:
###        - python: "Open_comandLine('java -jar aplicação.jar')"
        """Ira executar um comando por linha de comano para abrir um programa, este metodo não consegue construir um objeto que tenha os comandos webdriver"""
        os.system(Comand)
        
    def fechar_programa(self):
###- annotation:
###    text_description:
###        - "**fechar_programa()**:"
###        - "Este metodo fecha a conexão com o driver."
###    ex:
###        - python: "fechar_programa()"	

        """Ira fechar o driver e o subprocesso do Winium"""
        self.driver.close()
        self.sub.terminate()
        
    
        
    def elemento(self,elemento,tipo,implicit=None):
###- annotation:
###    text_description:
###        - "**elemento(elemento:str, tipo:str, implicit:int)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo procura um elemento e retorna o objeto do elemento."
###        - "**lista de elementos:**"
###    unorderedList:
###        - id
###        - name
###        - class
###        - xpath
###    ex:
###        - python: "elemento('id.user','id',10)"
###        - python: "elemento('class_user_login','class',1)"
###        - python: "elemento('login','name')"
###    return:
###        - Element: "retorna um WebElement"
###    exception: "Elemento_erro"

        """Verifica se precisa executar alguma espera."""
        
        if(implicit!=None):
            self.driver.implicitly_wait(implicit)
            
        """Verifica se é de algum tipo para proccurar, caso contrario leva uma exceçao"""
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk
                name:    Desk
                class:    Desk
                xpath:    Desk
                               
                """
            raise Elemento_erro(Erro)
        """Retorna o elemento encontrado"""
        return element
      
    def elemento_list(self,elemento,tipo,indice_lista,implicit=None):
###- annotation:
###    text_description:
###        - "**elemento_list(elemento,tipo,indice_lista,implicit)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo procura um conjunto de elementos que tem o mesmo padrão de webelemento, coloca em uma lista e retorna pelo indice."
###        - "**lista de elementos:**id; name; class; xpath;"
###    ex:
###        - python: "elemento_list('id.user','id',0)"
###        - python: "elemento_list('class_user_login','class',3)"
###        - python: "elemento_list('login','name',2)"
###    return:
###        - Object: "retorna um WebElement"

        """Vefificando todos os elementos com esse padrão"""
        elements=self.elementos_list(elemento, tipo,implicit)
        """Retirando da lista um elemento especifico, baseado no indice"""
        element=elements[indice_lista]
        """Retorna o elemento especifico"""
        return element
    
    def elementos_list(self,elemento,tipo,implicit=None):
###- annotation:
###    text_description:
###        - "**elementos_list(elemento,tipo,implicit):** "
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Esta procura todos os elementos de elementos com o mesmo parametro."
###        - "**lista de elementos:**"
###    unorderedList:
###        - id
###        - name
###        - class
###        - xpath
###    ex:
###        - python: "elementos_list('login','name')"
###    return:
###        - List: "retorna uma lista de WebElements"
###    exception: "Elemento_erro"
        """Vefificando todos os elementos com esse padrão"""
        if(implicit!=None):
            self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):           
            elements=self.driver.find_elements_by_id(elemento)  
        elif(tipo == 'name'):
            elements=self.driver.find_elements_by_name(elemento)
        elif(tipo == 'class'):            
            elements=self.driver.find_elements_by_class_name(elemento)
        elif(tipo == 'xpath'):            
            elements=self.driver.find_elements_by_xpath(elemento)
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Desk
                name:    Desk
                class:    Desk
                xpath:    Desk
               
                
                """
        
            raise Elemento_erro(Erro)
        """Retorna todos os elemento buscados"""
        return elements
    
    def escreve(self,elemento,conteudo,tipo,implicit=None):
###- annotation:
###    text_description:
###        - "**escreve(elemento,conteudo,tipo,implicit)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - conteudo: ":str= conteudo a ser escrito"
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo escreve em um elemento, na qual temos cinco parametros:"
###    ex:
###        - python: "escreve('gsfi','QUALQUER TEXTO','class',10)"

        """Encontrado o elemento"""
        element=self.elemento(elemento,tipo,implicit) 
        """Escrevendo neste elemento, caso haja conteudo, pode ser apagado antes da escrita"""
        element.send_keys(conteudo)
        """Retorna o elemento"""
        return element
    
           
    def clica(self,elemento,tipo,implicit=None):
###- annotation:
###    text_description:
###        - "**clica(elemento,tipo,implicit)**: "
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo clica em um elemento"
###    ex:
###        - python: "clica('gsfi','class',10)"
        
        """Encontrado o elemento"""
        element=self.elemento(elemento,tipo,implicit) 
        """Ação de clicar neste elemento"""
        element.click()
        """Retorna o elemento"""
        return element
             
    
    
                
    def escrever_elemento_lista(self,elemento,conteudo,tipo,indice_lista:int,implicit=None):
###- annotation:
###    text_description:
###        - "**escrever_elemento_lista(elemento,conteudo,tipo,indice_lista:int,implicit)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - conteudo: ":str= conteudo a ser escrito"
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo escreve em um elemento de uma lista de elementos com o mesmo tipo e elemento, na qual temos seis parametros"
###    ex:
###        - python: "escrever_elemento_lista('input','QUALQUER TEXTO','tag',2)"	

        """Encontrado o elemento, em uma lista de elementos"""
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        """Escrevendo neste elemento"""
        element.send_keys(conteudo)
        """Retornando o elemento"""
        return  element     
            
    def clica_elemento_lista(self,elemento,tipo,indice_lista:int,implicit=None):
###- annotation:
###    text_description:
###        - "**clica_elemento_lista(elemento,tipo,indice_lista,implicit)**:"	
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento. na qual temos quatro parametros."	
###    ex:
###        - python: "clica_elemento_lista('input','tag',1,10)"
	
        """Encontrado o elemento, em uma lista de elementos"""
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        """Clica no elemento"""
        element.click()
        """Retorna o elemento"""
        return element
        
    def get_element_location(self,element,tipo,implicit=None):
###- annotation:
###    text_description:
###        - "**get_element_location(element,tipo,implicit)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento."
###    ex:
###        - python: "get_element_location('input','tag',10)"
###    return:
###        - Tuple: "retorna as coordenadas de um elemento."
        """Encontra o elemento"""
        elemento=self.elemento(element,tipo,implicit)
        """Retira as medidas, e retorna uma string"""
        valor=elemento.get_attribute('BoundingRectangle')
        """Cria uma lista com os valores, pontos,x,y e a altura e largura"""
        localizacao=str(valor).split(',')
        """Retorna uma tupla, com os valores x,y inicial e os pontos x,y final"""
        return (int(localizacao[0]),int(localizacao[1]),int(localizacao[0])+int(localizacao[2]),int(localizacao[1])+int(localizacao[3]))