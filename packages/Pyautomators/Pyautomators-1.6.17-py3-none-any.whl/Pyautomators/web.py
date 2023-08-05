# -*- coding: utf-8 -*-

'''
@author: KaueBonfim
'''
"""Importando bibliotecas externas"""
from time import sleep
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium import webdriver
from selenium.webdriver import ActionChains
"""Importando bibliotecas internas"""
from Pyautomators.web_extensao import Espera,Js_Script,Simula,Alerta,MyListener,Condicoes_de_aguarde,Select_model,Tipos_de_elemento,Teclas_para_driver
from Pyautomators.Error import Driver_erro,Elemento_erro
from Pyautomators.Drivers import Firefox,Chrome
''' Este arquivo prove os metodos em selenium para web,
    na qual os passamos um elemento chave e seu tipo e ele executa a acao descrita'''

class Web(Espera,Js_Script,Simula):

    def __init__(self,driver,path_driver=None,options=None,binarios=None):

###- annotation:
###    mainTitle: Pyautomators - Classe Web
###    text_description:
###        - "Esta classe tem o intuito de prover conexão com selenium em Web. No construtor temos um parâmetro sendo um obrigatorio 'driver'."
###        - "Ao instanciarmos um objeto da classe Web é necessário passar os seguintes parâmetros (driver,path_driver)."
###        - "Os Tipos de Navegadores a serem passados como parâmetro, são:"
###    unorderedList:
###        - Ie
###        - Firefox
###        - Chrome
###        - Edge
###    text_description1:
###        - "**Exteções:**"
###    unorderedList1:
###        - Espera
###        - Js_Script
###        - Simula
###    ex:
###        - python: "context.app = Web('Chrome', context.path+'driver/chromedriver.exe')"        
                  
        if(driver == 'Chrome'):
            if(path_driver==None):
                path_driver="chromedriver"
            self.__driver=Chrome(path_driver=path_driver,opcoes=options,binario=binarios).get_driver()  
            self.driver=EventFiringWebDriver(self.__driver,MyListener())
        elif(driver == 'Firefox'):  
            if(path_driver==None):
                path_driver="geckodriver"          
            self.__driver=Firefox(path_driver=path_driver,options=options,binario=binarios).get_driver()
            self.driver=EventFiringWebDriver(self.__driver,MyListener())
            
                    
        elif(driver == 'Ie'):    
            if(path_driver==None):
                path_driver="IEDriverServer.exe"          
            self.driver=webdriver.Ie(executable_path=path_driver)
            
        elif(driver == 'Edge'):    
            if(path_driver==None):
                path_driver="MicrosoftWebDriver.exe"          
            self.driver=webdriver.Edge(executable_path=path_driver)
        else:
            Erro="""
                NÃ£o é um driver de servidor valido!
                Digite um driver valido:
                
                Ie
                Firefox
                Chrome    
                Edge 
                    """
            raise Driver_erro(Erro) 
        self.alert=Alerta(self.driver)
        self.ActionChains=ActionChains(self.driver)
        self.Condicao=Condicoes_de_aguarde()
        self.select=Select_model
        self.tipo=Tipos_de_elemento
        self.teclas=Teclas_para_driver  


    def print_janela(self,path_imagem):

###- annotation:       
###    title: Métodos
###    text_description:
###        - "**print_janela(path_imagem:str)**:"
###    parameters:
###        - path_imagem: ":str=Nome da imagem mais o caminho dela caso seja em outro diretorio."
###    text_description1:
###        - "Este metodo tira um print do conteudo atual da janela que esta sendo usada."
###    ex:
###        - python: context.app.print_janela('c:/teste.png')
###        - python: context.app.print_janela('teste.png')              
        self.driver.get_screenshot_as_file(path_imagem)

    def fechar_programa(self):
###- annotation: 
###    text_description:
###        - "**fechar_programa()**:"
###        - "Este metodo fecha o driver Web."
###    ex:
###        - python: "fechar_programa()"
        self.driver.quit()  

    def get_url(self):
###- annotation:       
###    text_description:
###        - "**get_url()**:"
###        - "Este metodo retorna a Url atual."
###    ex:
###        - python: get_url()
###    return:
###        - String: "Url atual no navegador"   
        return self.driver.current_url

    def pagina(self,url):
###- annotation:       
###    text_description:
###        - "**pagina(url:str)**:"
###    parameters:
###        - url: ":str= pagina de redirecionamento."
###    text_description1:
###        - "Este metodo acessa a pagina passada para a url."
###    ex:
###        - python: "pagina('http://google.com.br')  "    
        self.driver.get(url)

    def maximiza(self):
###- annotation:       
###    text_description:
###        - "**maximiza()**:"
###        - "Este metodo maximiza a janela do driver utilizado."
###    ex:
###        - python: "maximiza()"        
        self.driver.maximize_window()

    def preencher_tela(self):
###- annotation:       
###    text_description:
###        - "**preencher_tela()**:"
###        - "Este metodo preenche a tela inteira com a pagina."
###    ex:
###        - python: "preencher_tela() " 
        self.driver.fullscreen_window()

    def atualizar(self):
###- annotation:       
###    text_description:
###        - "**atualizar()**:"
###        - "Este metodo atualiza a pagina atual."
###    ex:
###        - python: "atualizar()"       
        self.driver.refresh()

    def voltar(self):
###- annotation:       
###    text_description:
###        - "**voltar()**:"
###        - "Este metodo retorna a pagina anterior."
###    ex:
###        - python: "voltar()"         
        self.driver.back()


    def frente(self):
###- annotation:       
###    text_description:
###        - "**frente()**:"
###        - "Este método segue para a próxima página em sequência."
###    ex:
###        - python: "frente()"    
        self.driver.forward() 
    
    def limpar(self):
###- annotation:       
###    text_description:
###        - "**frente()**:"
###        - "Este método segue para a próxima página em sequência."
###    ex:
###        - python: "frente()"    
        self.driver.clear()

    def get_titulo(self):
###- annotation:       
###    text_description:
###        - "**get_titulo()**:"
###        - "Este metodo retorna o titulo atual da pagina."
###    ex:
###        - python: "get_titulo()"    
###    return:
###        - String: "Titulo da pagina."    
        return self.driver.title
    
    def get_html(self):
###- annotation:       
###    text_description:
###        - "**get_html()**:"
###        - "Este método retorna o código-fonte HTML a uma variável."
###    ex:
###        - python: "get_html()"   
###    return:
###        - String: "HTML da pagina"  
        return self.driver.page_source
    
    def get_navegador(self):
###- annotation:       
###    text_description:
###        - "**get_navegador()**:"
###        - "Este metodo retorna o navegador que esta sendo usado no driver."
###    ex:
###        - python: "get_navegador()"    
###    return:
###        - String: "Qual driver esta sendo utilizado"  
        return self.driver.name
     
    
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
###        - link    
###        - tag   
###        - css 
###        - partial_link 
###    ex:
###        - python: "elemento('id.user','id',10)"
###        - python: "elemento('class_user_login','class',1)"
###        - python: "elemento('login','name')"
###    return:
###        - Element: "retorna um WebElement"
###    exception: "Elemento_erro"

        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        if(tipo == 'id'):
            element=self.driver.find_element_by_id(elemento)
        elif(tipo == 'name'):
            element=self.driver.find_element_by_name(elemento) 
        elif(tipo == 'class'):            
            element=self.driver.find_element_by_class_name(elemento) 
        elif(tipo == 'xpath'):            
            element=self.driver.find_element_by_xpath(elemento) 
        elif(tipo == 'link'):            
            element=self.driver.find_element_by_link_text(elemento) 
        elif(tipo == 'tag'):            
            element=self.driver.find_element_by_tag_name(elemento) 
        elif(tipo == 'css'):            
            element=self.driver.find_element_by_css_selector(elemento) 
        elif(tipo == 'partial_link'):            
            element=self.driver.find_element_by_partial_link_text(elemento) 
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Web
                name:    Web
                class:    Web
                xpath:    Web
                link:    Web
                tag:    Web
                css:    Web
                partial_link:    Web
                
                """
            raise Elemento_erro(Erro)
        return element




      
    def elemento_list(self,elemento,tipo,indice_lista,implicit=None):
###- annotation:
###    text_description:
###        - "**elemento_list(elemento:str,tipo:str,indice_lista:int,implicit:int)**:"
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
        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        elements=self.elementos_list(elemento, tipo, implicit)
        element=elements[indice_lista]
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
###        - link    
###        - tag   
###        - css 
###        - partial_link 
###    ex:
###        - python: "elementos_list('login','name')"
###    return:
###        - List: "retorna uma lista de WebElements"
###    exception: "Elemento_erro"
 
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
        elif(tipo == 'link'):            
            elements=self.driver.find_elements_by_link_text(elemento)
        elif(tipo == 'tag'):            
            elements=self.driver.find_elements_by_tag_name(elemento)
        elif(tipo == 'text'):            
            elements=self.driver.find_elements_by_partial_link_text(elemento)
        elif(tipo == 'css'):            
            elements=self.driver.find_elements_by_css_selector(elemento)
        
        else:
            Erro="""
                Escolha um valor de elemento Valido
                lista de elementos:
                id:    Web
                name:    Web
                class:    Web
                xpath:    Web
                link:    Web
                tag:    Web
                css:    Web
                partial_link:    Web
                """
            raise Elemento_erro(Erro)
        return elements
    
    def elemento_por_texto(self,elemento_base,tipo,texto_referencia,implicit=None):

###- annotation:       
###    text_description:
###        - "**elemento_por_texto(elemento_base,tipo,texto_referencia,implicit)**:"
###    parameters:
###        - elemento_base: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - texto_referencia: ":str= escolhe qual elemento da lista, baseado no texto."
###        - tipo(obrigatorio): ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###    text_description1:
###        - "Este metodo retorna em um elemento"
###    ex:
###        - python: "elemento_por_texto(\"gsfi\",\"class\",'texto valor')"
###    return:
###        - Object: "retorna um WebElement"
        elemento=None
        elements=self.elementos_list(elemento_base, tipo,implicit)
        for element in elements:
            if(element.text==texto_referencia):
                elemento=element
        return elemento
    
    
    def elemento_por_atributo(self,elemento_base,tipo,atributo_referencia,valor,implicit=None):
###- annotation:       
###    text_description:
###        - "**elemento_por_texto(elemento_base,tipo,texto_referencia,implicit)**:"
###    parameters:
###        - elemento_base: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo(obrigatorio): ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - atributo_referencia: ":str= O tipo de atributo que sera usado."
###        - valor: "Valor do atributo"
###    text_description1:
###        - "Este metodo retorna em um elemento"
###    ex:
###        - python: "elemento_por_atributo(\"gsfi\",\"class\",\"value\",\"teste\")"
###    return:
###        - Object: "retorna um WebElement"


        if(implicit!=None):  
            self.driver.implicitly_wait(implicit)
        elemento=None
        elements=self.elementos_list(elemento_base, tipo)
        for element in elements:
            if(element.get_attribute(atributo_referencia)==valor):
                elemento=element
        return elemento
    
    def escreve(self,elemento,conteudo,tipo,implicit=None,tempo=None):
###- annotation:
###    text_description:
###        - "**escreve(elemento,conteudo,tipo,implicit)**:"
###    parameters:
###        - elemento: ":str= elemento que deve ser procurado."
###        - conteudo: ":str= conteudo a ser escrito"
###        - tipo: ":str= tipo do elemento que sera procurado."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###        - tempo: ":int= É o tempo que leva para escrever cada tecla."
###    text_description1:
###        - "Este metodo escreve em um elemento"
###    ex:
###        - python: "escreve('gsfi','QUALQUER TEXTO','class',10,0.1)"
###    return:
###        - Object: "retorna um WebElement"
        element=self.elemento(elemento,tipo,implicit) 
        if(tempo is not None):
            if(self.tipo=='web'):
                for char in conteudo:
                    element.send_keys(char) 
                    sleep(tempo)
        else:
            element.send_keys(conteudo)
            
        return element
    
    def clica_elemento_atributo(self,elemento_base,tipo,atributo_referencia,valor,implicit=None):
###- annotation:       
###    text_description:
###        - "**clica_elemento_atributo(elemento_base,tipo,atributo_referencia,valor,implicit)**:"
###    parameters:
###        - elemento_base: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - atributo_referencia: ":str= O tipo de atributo que sera usado."
###        - valor: "Valor do atributo"
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo retorna em um elemento"
###    ex:
###        - python: "clica_elemento_atributo(\"gsfi\",\"class\",\"value\",\"teste\")"
        self.elemento_por_atributo(elemento_base, tipo, atributo_referencia, valor,implicit).click()
    
        
    def escreve_por_texto(self,elemento_base,tipo,conteudo,texto_referencia,implicit=None):
###- annotation:       
###    text_description:
###        - "**escreve_por_texto(elemento_base:str,tipo:str,conteudo:str,texto_referencia:str,implicit:int)**:"
###    parameters:
###        - elemento_base: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - conteudo: ":str= conteudo a ser escrito"
###        - texto_referencia: ":str= escolhe qual elemento da lista, baseado no texto."
###        - implicit: ":int= tempo que devemos esperar o elemento aparecer, caso não apareça é gerado um erro."
###    text_description1:
###        - "Este metodo escreve em um elemento"
###    ex:
###        - python: "escreve_por_texto(\"gsfi\",\"class\",\"testes\",'valeu',\"valor\")"
###    return:
###        - Object: "retorna um WebElement"	
        elemento=self.elemento_por_texto(elemento_base, tipo, texto_referencia,implicit)    
        elemento.send_keys(conteudo)
        return elemento
    
    def clica_por_text(self,elemento_base,tipo,texto_referencia):
###- annotation:       
###    text_description:
###        - "**clica_elemento_atributo(elemento_base,tipo,atributo_referencia,valor,implicit)**:"
###    parameters:
###        - elemento_base: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - texto_referencia: ":str= escolhe qual elemento da lista, baseado no texto."
###        - valor: ":str= Valor do atributo"
###    text_description1:
###        - "Este metodo escreve em um elemento."
###    ex:
###        - python: "clica_por_text('gsfi','class','texto valor')"
###    return:
###        - Object: "retorna um WebElement"
       
        elemento=self.elemento_por_texto(elemento_base, tipo, texto_referencia)
        elemento.click()
        return elemento
           
    def clica(self,elemento,tipo,implicit=None):
###- annotation:       
###    text_description:
###        - "**clica(elemento:str,tipo:str,implicit:int)**:"
###    parameters:
###        - elemento: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu ekemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - implicit: ":int= É o tempo que devemos esperar o elemento aparecer, caso não apareça e gerado um erro."
###    text_description1:
###        - "Este metodo escreve em um elemento."
###    ex:
###        - python: "clica('gsfi','class','texto valor')"
###    return:
###        - Object: "retorna um WebElement"
        element=self.elemento(elemento,tipo,implicit) 
        element.click()
        return element
             
    
    def pegar_texto(self,elemento,tipo,implicit=None):
###- annotation:       
###    text_description:
###        - "**pegar_texto(elemento,tipo,implicit)**:"
###    parameters:
###        - elemento: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - implicit: ":int= É o tempo que devemos esperar o elemento aparecer, caso não apareça e gerado um erro."
###    text_description1:
###        - "Este metodo retorna o texto de um elemento."
###    ex:
###        - python: "dado um trecho de HTML:"
###        - python: "<input class='gsfi' id='lst-ib' maxlength='2048' name='q' autocomplete='off' title='Pesquisar' >Textooo</input>"
###        - python: "valor=pegar_textto('lst-ib','id',10)"
###        - python: "print(valor)"
###        - python: ">>>Textooo"
###    return:
###        - tuple: "retorna o texto e o elemento"
        element=self.elemento(elemento,tipo,implicit) 
        return element.text,element
                
    def escrever_elemento_lista(self,elemento,conteudo,tipo,indice_lista:int,implicit=None,tempo:int=None):
###- annotation:       
###    text_description:
###        - "**escrever_elemento_lista(elemento:str,conteudo:str,tipo:str,indice_lista:int,implicit:int,tempo:int)**:"
###    parameters:
###        - elemento: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - conteudo: ":str= conteudo a ser escrito"
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= É o tempo que devemos esperar o elemento aparecer, caso não apareça e gerado um erro."
###        - tempo: ":int= É o tempo que leva para escrever cada tecla."
###    text_description1:
###        - "Este metodo escreve em um elemento de uma lista de elementos com o mesmo tipo e elemento."
###    ex:
###        - python: "dado um trecho de HTML:"
###        - python: "<input name='btn' type='submit' jsaction='sf.lck'>"
###        - python: "<input name='btn' type='submit' jsaction='sf.chk'>"
###        - python: "escrever_elemento_lista('input','QUAL QUER TEXTO','tag',2,10,0.1)"
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        element.send_keys(conteudo)     
            
    def clica_elemento_lista(self,elemento,tipo,indice_lista:int,implicit=None):
###- annotation:       
###    text_description:
###        - "**clica_elemento_lista(elemento:str,tipo:str,indice_lista:int,implicit:int)**:"
###    parameters:
###        - elemento: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= É o tempo que devemos esperar o elemento aparecer, caso não apareça e gerado um erro."
###    text_description1:
###        - "Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento."
###    ex:
###        - python: "dado um trecho de HTML:"
###        - python: "<input name='btn' type='submit' jsaction='sf.lck'>"
###        - python: "<input name='btn' type='submit' jsaction='sf.chk'>"
###        - python: "clica_elemento_lista('input','tag',1,10)"
        element=self.elemento_list(elemento,tipo,indice_lista,implicit)
        element.click()
        return element 
    
    def pegar_texto_list(self,elemento,tipo,indice_lista:int,implicit=None):
###- annotation:       
###    text_description:
###        - "**clica_elemento_lista(elemento,tipo,indice_lista:int,implicit)**:"
###    parameters:
###        - elemento: ":str= Qual é o elemento que iremos buscar para realizar a escrita, necessariamente oque invididualiza seu elemento pela descricao."
###        - tipo: ":str= O tipo para do elemento que iremos usar(id ,class, name, xpath ...)."
###        - indice_lista: ":int= indice da linsta que esta o elemento que sera retornado"
###        - implicit: ":int= É o tempo que devemos esperar o elemento aparecer, caso não apareça e gerado um erro."
###    text_description1:
###        - "Este metodo clica em um elemento de uma lista de elementos com o mesmo tipo e elemento."
###    ex:
###        - python: "dado um trecho de HTML:"
###        - python: "<input name='btn' type='submit' jsaction='sf.lck'>"
###        - python: "<input name='btn' type='submit' jsaction='sf.chk'>"
###        - python: "pegar_texto_list('input','tag',1,10)"
        element=self.elementos_list(elemento,tipo,indice_lista,implicit)
        return element.text 