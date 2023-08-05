# -*- coding: utf-8 -*-
'''
Created on 24 de ago de 2018

@author: koliveirab
'''
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from Pyautomators.Error import Elemento_erro

###- annotation:
###    mainTitle: Pyautomators - web_extensao

class Js_Script():
###- annotation:
###    title: Pyautomators - Classe Js_Script

    
    def __init__(self,drive):
        self.driver=drive
        
    def execute_script(self,script):
###- annotation:
###    title: Metodos
###- annotation: 
###    text_description:
###        - "**execute_script(script:str)**:"
###    parameters:
###        - script: ":str= comandos javascript"
###    text_description1:
###        - "Este metodo executa comandos javascript no navegador."
###    ex:
###        - python: "execute_script('window.scrollTo(0, document.body.scrollHeight);')"

	
        '''Este metodo executa comando javascript no console do navegador
        
            parametros:
            script(obrigatorio):o script a ser executado
           Exemplo:
        ("window.scrollTo(0, document.body.scrollHeight);")'''
        #executa javascript no driver
        self.driver.execute_script(script)   
        
    def rolagem_tela(self,valor):
###- annotation:
###    text_description:
###        - "**rolagem_tela(valor:int)**:"
###    parameters:
###        - valor: ":str= valor de rolagem"
###    text_description1:
###        - "Este metodo faz a rolagem da tela."
###    ex:
###        - python: "rolagem_tela(100)"
        #executa a rolagem da tela pelo javascript
        '''Este metodo faz a rolagem da pagina que esta sendo usada em javaScript
        Exemplo: rolagem_tela(100)'''
        self.execute_script("window.scrollTo({}, document.body.scrollHeight);".format(valor))
        
'''Este Modulo trabalha com as esperas feitas pelo WebDriverWait'''
class Espera():
    ''' Esta classe tem o intuito de prover conexao com o WevDriverWait'''
###- annotation:
###    title: Pyautomators - Classe Espera    
    
    
        
    def aguarde_condicao(self,condicao,tempo,intervalo=0.5,menssagem_exception=''):
###- annotation:
###    title: Metodos
###- annotation: 
###    text_description:
###        - "**aguarde_condicao(condicao:Condicoes_de_aguarde,tempo:int,intervalo:int,menssagem_exception:str)**:"
###    parameters:
###        - condicao: ":Condicao de espera= consicao de aguarde"
###        - tempo: ":int= valor de tentativas"
###        - intervalo: ":int= intervalo em cada tentativa"
###        - menssagem_exception: ":str= mensagem que sera gerada caso de erro"
###    text_description1:
###        - "Este metodo aguarda uma condição para passada por parametro durante o tempo determinado podendo controlar o tempo de verificação."
###    ex:
###        - python: "aguarde_condicao(condicao,100,1,'não foi possivel achar o elemento visivel')"
###    return:
###        - Element: "retorna um WebElement"
        
        #cria um objeto wait passando o tempo e o intervalo de cada para cada ciclo
        wait=WebDriverWait(self.driver,tempo,intervalo)
        #ira aguardar a condição passada ser valida, caso não seja dependendo valida no tempo determinado ira gerar um erro
        #caso nao sera gerado retorna o elemento
        return wait.until(condicao,menssagem_exception)


    def aguarde_condicao_negada(self,condicao,tempo,intervalo=0.5,menssagem_exception=''):
###- annotation:
###    text_description:
###        - "**aguarde_condicao_negada(condicao:Condicoes_de_aguarde,tempo:int,intervalo:int,menssagem_exception:str)**:"
###    parameters:
###        - condicao: ":Condicao de espera= consicao de aguarde"
###        - tempo: ":int= valor de tentativas"
###        - intervalo: ":int= intervalo em cada tentativa"
###        - menssagem_exception: ":str= mensagem que sera gerada caso de erro"
###    text_description1:
###        - "Este metodo trabalha com o aguarde trazendo uma condicao para o aguarde explicito, aonde ela nao deve aparecer,retorna o elemento."
###    ex:
###        - python: "aguarde_condicao_negada(condicao,100,1,'não foi possivel achar o elemento visivel')"
###    return:
###        - Element: "retorna um WebElement"
        
        #cria um objeto wait passando o tempo e o intervalo de cada para cada ciclo

        wait=WebDriverWait(self.driver,tempo,intervalo)
        return wait.until_not(condicao, menssagem_exception)
    
class Simula():
###- annotation:
###    title: Pyautomators - Classe Simula   
###    text_description:
    def mover_mouse(self,elemento,tipo,implicit=None):
###- annotation:
###    title: Metodos
###- annotation: 
###    text_description:
###        - "**mover_mouse(elemento:str,tipo:str,implicit:int)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "simula o movimento do mouse ate um elemento especificado."
###    ex:
###        - python: "ActionChains.mover_mouse('gsfi','class',10)"
        self.ActionChains.move_to_element(self.elemento(elemento,tipo,implicit)).perform()
        
    def duplo_clique(self,elemento,tipo,implicit=None):
###- annotation: 
###    text_description:
###        - "**duplo_clique(elemento:str,tipo:str,implicit:int)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Simula um clique duplo com o mouse."
###    ex:
###        - python: "ActionChains.duplo_clique('gsfi','class',10)"        
        self.ActionChains.double_click(self.elemento(elemento,tipo,implicit)).perform()
        
    def clique(self,elemento,tipo,implicit=None,Botao='left'):
###- annotation: 
###    text_description:
###        - "**clique(elemento:str,tipo:str,implicit:int)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###        - Botao: ":str= escolher entre as opções: left(padrao) ou right,"
###    text_description1:
###        - "Simula um clique com o mouse."
###    ex:
###        - python: "ActionChains.clique('gsfi','class',10)"   

        if(Botao=="left"):
            self.ActionChains.click(self.elemento(elemento,tipo,implicit)).perform()
        elif(Botao=='rigth'):
            self.ActionChains.context_click(self.elemento(elemento,tipo,implicit)).perform()
        else:
            Erro="""
                Escolha um valor Valido
                Os Valores são:
                left ou rigth
                
                """
            raise Elemento_erro(Erro)
        
    def clique_arraste(self,elemento1,tipo1,elemento2,tipo2,implicit1=None,implicit2=None):
###- annotation: 
###    text_description:
###        - "**clique_arraste(elemento1:str,tipo1:str,implicit1:int,elemento2:str,tipo2:str,implicit2:int)**:"
###    parameters:
###        - elemento1: ":str= elemento1 que deve ser procurado."
###        - tipo1: ":str= tipo do elemento1 que sera procurado."
###        - implicit1: ":int= tempo que devemos esperar o elemento1 aparecer, caso não apareça é gerado um erro."
###        - elemento2: ":str= elemento2 que deve ser procurado."
###        - tipo2: ":str= tipo do elemento2 que sera procurado."
###        - implicit2: ":int= tempo que devemos esperar o elemento2 aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "simula o arraste entre os elementos 1 e 2."
###    ex:
###        - python: "ActionChains.clique_arraste('gsfi','class','name','id')"   
        self.ActionChains.drag_and_drop(self.elemento(elemento1,tipo1,implicit1),self.elemento(elemento2,tipo2,implicit2)).perform()
        
    def digitos(self,elemento,tipo,lista_de_chaves,implicit=None):
###- annotation: 
###    text_description:
###        - "**digitos(elemento:str,tipo:str,implicit:int,lista_de_chaves:list)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "simula o a digitação em um elemento especificado."
###    ex:
###        - python: "from Pyautomators.web_extensao import Teclas_para_driver" 
###        - python: "ActionChains.digitos('gsfi','class',(Teclas_para_driver.TAB,Teclas_para_driver.ENTER))"  

         self.ActionChains.send_keys_to_element(self.app.elemento(elemento,tipo,implicit),*lista_de_chaves).perform()
        
class Alerta():
###- annotation:
###    title: Pyautomators - Classe Alerta    
    def __init__(self,driver):
        #trabalha com o alert do driver criando um objeto
        self.alert=Alert(driver)
        
    def aceitar(self):
###- annotation: 
###    title: Metodos
###    text_description:
###        - "**aceitar()**:"
###        - "aceitando o alerta apresentado."
###    ex:
###        - python: "alert.aceitar()" 
        self.alert.accept()
        
    def rejeitar(self):
###- annotation: 
###    text_description:
###        - "**rejeitar()**:"
###        - "reijeitando o alerta apresentado."
###    ex:
###        - python: "alert.rejeitar()" 
        self.alert.dismiss()
        
    def inserir_texto(self,texto):
###- annotation: 
###    text_description:
###        - "**inserir_texto(texto:str)**:"
###    parameters:
###        - texto: ":str= Texto para ser inserida."
###    text_description1:
###        - "escrevendo na entrada input do alerta."
###    ex:
###        - python: "alert.inserir_texto('Testes')" 
        self.alert.send_keys(texto)
        
    def get_texto(self):
###- annotation: 
###    text_description:
###        - "**inserir_texto(texto:str)**:"
###    parameters:
###        - texto: ":str= Texto para ser inserida."
###    text_description1:
###        - "retirando o texto do alerta."
###    ex:
###        - python: "alert.get_texto()" 
        return self.alert.text
    
class Select_model():
###- annotation:
###    title: Pyautomators - Classe select_model 
###    text_description:
###        - "Esta classe é usado como atributo da classe Web"
###        - "O construtor recebe um elemento select"
###    ex:
###        - python: "app.select(app.elemento('q','name'))" 
    
    def __init__(self,elemento):
        '''Este metodo trabalha com listas <Select> para preenchimento 
        parametros:
        elemento(obrigatorio): elemento do select
        
        Exemplo:
        
        select(app.elemento('user.select.list','id'))
        
        '''
        Erro="""
                            Não é um tipo de seleção valido
                            Digite um tipo valido:
                            
                            index
                            valor
                            texto    
                                
                                """

        self.select=Select(elemento)
            
    def select_index(self,*args):
###- annotation: 
###    title: Metodos
###    text_description:
###        - "**select_index(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser selecionado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).select_index('1')" 
        for valor in args:
            self.select.select_by_index(valor)
                        
    def select_valor(self,*args):
###- annotation: 
###    text_description:
###        - "**select_valor(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser selecionado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).select_valor('SC')" 
        for valor in args:
            self.select.select_by_value(valor)
                        
    def select_text(self,*args):
###- annotation: 
###    text_description:
###        - "**select_text(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser selecionado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).select_text('Santa Catarina')" 
        for valor in args:
            self.select.select_by_visible_text(valor)
            
    def deselect_index(self,*args):
###- annotation: 
###    text_description:
###        - "**deselect_index(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser retirado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).deselect_index('1')" 
        for valor in args:
            self.select.deselect_by_index(valor)
    def deselect_valor(self,*args):
###- annotation: 
###    text_description:
###        - "**deselect_valor(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser retirado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).deselect_valor('SC')" 
        for valor in args:
            self.select.deselect_by_value(valor)
    def deselect_text(self,*args):
###- annotation: 
###    text_description:
###        - "**deselect_text(*itens:str)**:"
###    parameters:
###        - itens: ":str= Itens para ser retirado."
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).deselect_text('Santa Catarina')" 
        for valor in args:
            self.select.deselect_by_visible_text(valor)   
            
    def deselect_all(self):
###- annotation: 
###    text_description:
###        - "**deselect_text()**:"
###        - "retirar todos os itens"
###    ex:
###        - python: "select(app.elemento('user.select.list','id')).deselect_text()" 
                    
        self.select.deselect_all()
            

class MyListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        pass
    
    def after_navigate_to(self, url, driver):
        pass
    
    def before_navigate_back(self, driver):
        pass

    def after_navigate_back(self, driver):
        pass

    def before_navigate_forward(self, driver):
        pass

    def after_navigate_forward(self, driver):
        pass

    def before_find(self, by, value, driver):
        pass

    def after_find(self, by, value, driver):
        
        elements=None
        if(by == 'id'):     
            elements=driver.find_element_by_id(value)  
        elif(by == 'name'):
            elements=driver.find_element_by_name(value)
        elif(by == 'class name'):            
            elements=driver.find_element_by_class_name(value)
        elif(by == 'xpath'):            
            elements=driver.find_element_by_xpath(value)
        elif(by == 'link text'):            
            elements=driver.find_element_by_link_text(value)
        elif(by == 'tag name'):            
            elements=driver.find_element_by_tag_name(value)
        elif(by == 'partial link text'):            
            elements=driver.find_element_by_partial_link_text(value)
        elif(by == 'css selector'):            
            elements=driver.find_element_by_css_selector(value)
        driver.execute_script("arguments[0].style.border = 'medium solid red';",elements)

    def before_click(self, element, driver):
        pass

    def after_click(self, element, driver):
        pass

    def before_change_value_of(self, element, driver):
        pass

    def after_change_value_of(self, element, driver):
        pass

    def before_execute_script(self, script, driver):
        pass

    def after_execute_script(self, script, driver):
        pass

    def before_close(self, driver):
        pass

    def after_close(self, driver):
        pass

    def before_quit(self, driver):
        pass

    def after_quit(self, driver):
        pass

    def on_exception(self, exception, driver):
        print(exception)
    
    
class Condicoes_de_aguarde():
###- annotation:
###    title: Pyautomators - Classe Condicoes_de_aguarde 
###    text_description:
###        - "Esta classe é usado como atributo da classe Web"
###        - "é usado como argumento da classe Espera"

    def VISIVEL(self,elemento,tipo):
###- annotation: 
###    title: Metodos 
###    text_description:
###        - "**VISIVEL(elemento:str,tipo:str)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###    text_description1:
###        - "Aguarde um elemento ser visivel na tela."
###    ex:
###        - python: "Condicao.VISIVEL('user','id')" 
        tipo=self.__definir_by(tipo)
        return expected_conditions.visibility_of_element_located((tipo,elemento))
    
    def CLICAVEL(self,elemento,tipo):
###- annotation: 
###    text_description:
###        - "**CLICAVEL(elemento:str,tipo:str)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###    text_description1:
###        - "Aguarde um elemento ser clicavel na tela."
###    ex:
###        - python: "Condicao.CLICAVEL('user','id')" 
        tipo=self.__definir_by(tipo)
        return expected_conditions.element_to_be_clickable((tipo,elemento))
    
    def ALERTA_PRESENTE(self):
###- annotation: 
###    text_description:
###        - "**ALERTA_PRESENTE(elemento:str,tipo:str)**:"
###        - "Aguarde um alerta aparecer na tela."
###    ex:
###        - python: "Condicao.ALERTA_PRESENTE('user','id')"         
        return expected_conditions.alert_is_present()
    
    def NOVA_JANELA_ABERTA(self,indice_janela):
###- annotation: 
###    text_description:
###        - "**NOVA_JANELA_ABERTA(indice_janela:int)**:"
###    parameters:
###        - indice_janela: ":int= indice da janela que sera aberta."
###    text_description1:
###        - "Aguarde um elemento ser clicavel na tela."
###    ex:
###        - python: "Condicao.NOVA_JANELA_ABERTA(2)"         
        return expected_conditions.new_window_is_opened(indice_janela)
    
    def TITULO_SER_IGUAL_A(self,titulo_ser):
###- annotation: 
###    text_description:
###        - "**TITULO_SER_IGUAL_A(titulo_ser:str)**:"
###    parameters:
###        - titulo_ser: ":str= titulo para ser comparado na espera."
###    text_description1:
###        - "aguarde a pagina ter o titulo passado."
###    ex:
###        - python: "Condicao.TITULO_SER_IGUAL_A('Home')"     
        return expected_conditions.title_is(titulo_ser)
    
    def URL_CONTEM(self,url):
###- annotation: 
###    text_description:
###        - "**URL_CONTEM(url:str)**:"
###    parameters:
###        - url: ":str= Url para ser comparado."
###    text_description1:
###        - "aguarde a url ser igual a passada."
###    ex:
###        - python: "Condicao.URL_CONTEM('http://teste.com/home')" 
        return expected_conditions.url_contains(url)
    
    def TEXTO_ESTAR_PRESENTE_ELEMENTO(self,elemento,tipo,texto):
###- annotation: 
###    text_description:
###        - "**TEXTO_ESTAR_PRESENTE_ELEMENTO(elemento:str,tipo:str,texto:str)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - texto: ":str= texto para ser comparado."
###    text_description1:
###        - "Aguarde um elemento ser visivel na tela."
###    ex:
###        - python: "Condicao.TEXTO_ESTAR_PRESENTE_ELEMENTO('user','id','teste')" 
        tipo=self.__definir_by(tipo)
        return expected_conditions.text_to_be_present_in_element((tipo,elemento),texto)
        
    def __definir_by(self,tipo):
        if(tipo=='id'):
            return By.ID
        elif(tipo=='class'):
            return By.CLASS_NAME
        elif(tipo=='xpath'):
            return By.XPATH
        elif(tipo=='name'):
            return By.NAME
        elif(tipo=='tag'):
            return By.TAG_NAME
        elif(tipo=='partial_link'):
            return By.PARTIAL_LINK_TEXT
        elif(tipo=='link'):
            return By.LINK_TEXT
        elif(tipo=='css'):
            return By.CSS_SELECTOR
        else:
            Erro="""
            Escolha um valor de elemento Valido
            lista de elementos:
            id:    Desk,Web,Mobile
            name:    Desk,Web,Mobile
            class:    Desk,Web,Mobile
            xpath:    Desk,Web,Mobile
            link:    Web
            tag:    Web,Mobile
            css:    Web,Mobile
            partial_link:    Web
            
            
            """
            raise Elemento_erro(Erro)
        
class Tipos_de_elemento():
  
    ID='id'
    CLASS_NAME='class'
    XPATH='xpath'
    NAME='name'
    TAG_NAME='tag'
    PARTIAL_LINK='partial_link'
    LINK_TEXT='link'
    CSS_SELECTOR='css'
    
  
class Teclas_para_driver(Keys):
    pass