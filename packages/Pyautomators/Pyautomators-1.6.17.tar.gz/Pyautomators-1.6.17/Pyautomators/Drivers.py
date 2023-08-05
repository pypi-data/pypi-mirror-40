# -*- coding: utf-8 -*-
'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager,EdgeDriverManager
from selenium.webdriver.firefox.options import Options
"""Importando bibliotecas internas"""
from Pyautomators.Error import Driver_erro

class Tipos_de_navegadores():
    ''' Tipos de navegadores para a Class Web'''
    CHROME='Chrome'
    FIREFOX='Firefox'
    IE='Ie'
    EDGE='Edge'
    OPERA='Opera'
    SAFARI='Safari'
    
class Manager_Install():
###- annotation:
###    mainTitle: Pyautomators - Classe Manager_Install
###    text_description:
###        - "Esta classe tem o intuito de promover conexao com drivers binarios sem a necessidade de ter um driver instalado.\n"
###    title: "Parametros"
###    text_description1:
###        - "**tipo(obrigatorio):**Qual driver deve instalar dos browsers.\n"
###        - "**versão:** qual a versao deve ser baixada.\n"
###    ex:
###        - python: "from Pyautomators.web import Web"
###        - python: "from Pyautomators.Drivers import Manager_Install"
###        - python: "context.app = Web ('Chrome',Manager_Install('Chrome').get_manager())"
###    exception: "Driver_erro"

    '''Esta classe tem o intuito de promover conexao com driver binarios sem a necessidade de ter un driver instalado'''
    def __init__(self,tipo,version=None):

        """Escolhendo qual o driver e verificando uma versao"""
        if(tipo == 'Chrome'):  
            self.__manager=ChromeDriverManager(version)
        elif(tipo == 'Firefox'): 
            self.__manager=GeckoDriverManager(version)
        elif(tipo == 'Ie'): 
            self.__manager=IEDriverManager(version)
        elif(tipo == 'Edge'): 
            self.__manager=EdgeDriverManager(version)
        else:
            Erro="""
                Não é um driver de manager valido!
                Digite um driver valido:
                Ie
                Firefox
                Chrome 
                Edge    
                    """
            raise Driver_erro(Erro) 
        
    def get_manager(self):
###- annotation:
###    title: Metodos
###    text_description:
###        - "**get_manager():** retorna a instancia de memoria do driver instalado.\n"
###    ex:
###        - python: "get_manager()"
        """retorna a instancia do objeto driver"""
        return self.__manager.install()
    
class Chrome():
    '''Esta classe tem o intuito de retornar uma classe chromedriver'''
    def __init__(self,path_driver='chromedriver',opcoes=None,binario=None):
        """Este contrutor cria um obejto webdriver-chrome
        parametros:
        path_driver: caminho para o driver, caso seja omitido ele entende que o caminho e o atual
        opcoes: opções que são fornecidos pela classe Options_Chrome, e este parametro recebe a instancia da classe
        log é um arquivo que registra os acontecimentos no driver
        binario é o executavel no crhome no pc"""
        
        """criando um objeto chromedriver"""
        des=None
        """verificando se foi passado binario"""
        if(opcoes!=None):
            des=opcoes.to_capabilities()
            
        if(binario!=None and opcoes!=None):
            des['binary_location']=binario
        elif(binario!=None):
            des={'binary_location':binario}
        self.__driver=webdriver.Chrome(executable_path=path_driver, service_log_path='log/driverChrome.log', service_args=['--verbose'],desired_capabilities=des)
        
    def get_driver(self):
        """Retorna o objeto do driver"""
        #retornando a instancia chromedriver
        return self.__driver
    
class Firefox():
    '''Esta classe tem o intuito de retornar uma classe firefoxdriver'''
    def __init__(self,path_driver='geckodriver',options=None,binario=None):
        """Este contrutor cria um obejto webdriver-firefox
        parametros:
        path_driver: caminho para o driver, caso seja omitido ele entende que o caminho e o atual
        log é um arquivo que registra os acontecimentos no driver
        opcoes: opções que são fornecidos pela classe Firefox-perfil e Firefox-options, e este parametro recebe a instancia da classe
        binario: caso tenha necessidade de passar o binario do mozila Firefox"""
        #verificando se o binario foi passado
        perfil=None
        opcoes=None
        if(options is not None):
            perfil=options['perfil']
            opcoes=options['opcoes']
        self.__driver=webdriver.Firefox(executable_path=path_driver, service_log_path='log/driverFirefox.log',firefox_profile=perfil,firefox_binary=binario,firefox_options=opcoes)

    def get_driver(self):
        #retorna a instancia do Firefor
        return self.__driver

class Options_Firefox():
###- annotation:
###    title: "Classe Options_Firefox"
###    text_description:
###        - "Faz uso de opções do navegador firefox;"
###    ex:
###        - python: "from Pyautomators.web import Web"
###        - python: "from Pyautomators.Drivers import Options_Firefox"
###        - python: "context.app = Web ('Firefox',\"Firefox\",Options_Firefox().get_options())"
###    title1: Metodo

    def __init__(self):
        #Criando o objeto 
        self.__perfil=webdriver.FirefoxProfile()
        self.__options=Options()
        
    def backgroud(self):
###- annotation:
###    text_description:
###        - "**backgroud()**:"
###        - "Criando uma instancia do driver sem a interface grafica."
###    ex:
###        - python: "backgroud()"

        self.__options.headless=True
        return self
    
    def private(self):
###- annotation:
###    text_description:
###        - "**private()**:"
###        - "Abrindo o Driver com a instancia do usuario em privado"
###    ex:
###        - python: "private()"

	
        self.__perfil.set_preference("browser.privatebrowsing.autostart", True)        
        return self
    
    def proxy(self,endereco:str,porta:int):

###- annotation:
###    text_description:
###        - "**proxy(endereco:str,porta:int)**:"	
###    text_description1:
###        - "Setar o valor do proxy no navegador."
###    parameters:
###        - endereco: ":str= ip, ou endereco do proxy."
###        - porta: ":int= Porta de entrada do proxy."	
###    ex: 
###        - python: "proxy('proxy',8080)"

        self.__perfil.set_preference("network.proxy.type", 1)
        self.__perfil.set_preference("network.proxy.http", endereco)
        self.__perfil.set_preference("network.proxy.http_port", porta)
        return self
    
    def get_options(self):
###- annotation:
###    text_description:
###        - "**get_options()**:"	
###        - "Retorna as opções."
###    ex: 
###        - python: "get_options()"
###    return:
###        - Dict: "retorna um dicionario de opções."
        return {'opcoes':self.__options,'perfil':self.__perfil}
    
    
    
class Options_Chrome():
###- annotation:
###    title: "Classe Options_Chrome"
###    text_description:
###        - "Faz uso de opções do navegador Chrome."
###    ex:
###        - python: "from Pyautomators.web import Web"
###        - python: "from Pyautomators.Drivers import Options_Chrome"
###        - python: "context.app = Web ('Chrome',\"Chrome\",Options_Chrome().get_options())"
###    title1: Metodo
    
    def __init__(self):
        self.options=ChromeOptions()
        
    def private(self):
###- annotation:
###    text_description:
###        - "**private()**:"
###        - "Abrindo o Driver com a instancia do usuario em privado"
###    ex:
###        - python: "private()"
	
        self.options.add_argument("--incognito")
        return self
    
    def backgroud(self):
###- annotation:
###    text_description:
###        - "**backgroud()**:"
###        - "Criando uma instancia do driver sem a interface grafica."
###    ex:
###        - python: "backgroud()"
        self.options.add_argument("--headless")
        return self
    
    def maximizado(self):
###- annotation:
###    text_description:
###        - "**maximizado()**:"
###        - "Abrir o driver maximizado."
###    ex:
###        - python: "maximizado()"	
        self.options.add_argument('--start-maximized') 
        return self
    
    def posicao_janela(self,x,y):
###- annotation:
###    text_description:
###        - "**posicao_janela(x:int,y:int)**:"
###        - "Colocar a posição inicial do driver na tela."
###    parameters:
###        - x-y: ":int= local na tela."
###    ex:
###        - python: "posicao_janela(100,20)"      
        self.options.add_argument('--window-position={},{}'.format(x,y))
        return self
    
    def tamanho_janela(self,largura,altura):
###- annotation:
###    text_description:
###        - "**tamanho_janela(largura:int,altura:int)**:"
###        - "Tamanho da largura e altura da tela."
###    parameters:
###        - largura-altura: ":int= sao as dimensões do driver."
###    ex:
###        - python: "tamanho_janela(1000,300)"
        '''Tamanho da largura e altura da tela
        parametros:
        largura,altura: sao as dimensões do driver
        Exemplo:
        tamanho_janela(self,1000,300)
        '''
        self.options.add_argument('--window-size={},{}'.format(largura,altura))
        return self
    
    def perfil(self,perfil_path):
###- annotation:
###    text_description:
###        - "**perfil(perfil_path)**:"
###    parameters:
###        - perfil_path: ":str= local aonde esta seu perfil."
###    text_description1:
###        - "Recebe o caminho de memoria do perfil do chrome"
###    ex:
###        - python: "perfil('C:/Users/koliveirab/AppData/Local/Google/Chrome/User Data/')"
	
        '''Recebe o caminho de memoria do perfil do seu chrome que utiliza
        parametros:
        perfil_path: local aonde esta seu perfil
        
        Exemplo:
        perfil('C:/Users/koliveirab/AppData/Local/Google/Chrome/User Data/')
        '''
        self.options.add_argument('user-data-dir={}'.format(perfil_path))
        return self
    
    def proxy(self,auto=True,endereco=None,porta=None):
###- annotation:
###    text_description:
###        - "**proxy(auto:bool,endereco:str,porta:int)**:"	
###    parameters:
###        - auto: ":bool= detecta o proxy nativo na maquina."
###        - endereco: ":str= ip, ou endereco do proxy."
###        - porta: ":int= Porta de entrada do proxy."
###    text_description1:
###        - "Setar o valor do proxy no navegador."
###    ex: 
###        - python: "proxy(endereco='proxy',porta=80)"
###        - python: "proxy()"

        if(auto):
            self.options.add_argument('--proxy-auto-detect')
        else:
            self.options.add_argument("--proxy-server='{}:{}'".format(endereco,porta))
        return self
    
    def root(self):
###- annotation:
###    text_description:
###        - "**root()**:"	
###    text_description1:
###        - "Abrir o navegador como admin."
###    ex: 
###        - python: "root()"
        self.options.add_argument('--no-sandbox')
        return self
    
    def get_options(self):
###- annotation:
###    text_description:
###        - "**get_options()**:"	
###        - "Retorna as opções."
###    ex: 
###        - python: "get_options()"
###    return:
###        - Dict: "retorna um dicionario de opções."
        return self.options