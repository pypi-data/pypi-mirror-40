# -*- coding: utf-8 -*-
'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
import argparse,shutil
import os
"""Importando bibliotecas internas"""
from Pyautomators.pyautomator import Project
from Pyautomators.Runner_Pyautomators import orquestrador
from Pyautomators.Runner_in_Container import Runner_Container
from Pyautomators import Ambiente
from Pyautomators.Documentacao import criar_documento_cliente
from Pyautomators.remote import Runner_Client,Runner_Master

###- annotation:
###    mainTitle: Pyautomators inLine
###    text_description:
###        - O modulo __main__ trabalha com a execução dos testes em linha de comando
###    parameters:
###        - string: "comando [CHAVE ARGUMENTOS]" 
###    ex:
###        - python: "python -m Pyautomators COMANDO [CHAVE ARGUMENTOS]"
###        - python: "python -m Pyautomators criar_projeto -n Testes_Web\n"

"""So vai usar a main, caso este arquivo ou modulo seja chamado"""
if('__main__'==__name__):
   
    ARG=argparse.ArgumentParser()
    """criando um objeto para receber os argumentos"""

###- annotation:    
###    title:
###        - "**Comandos**\n"
###    text_description:
###        - "**criar_projeto:** Usado para gerar projeto de automação e a arquitetura de diretório\n"
###        - "\t**CHAVES:** -f -d (Opcional)\n"
###        - "**execute:** Usado para executar um projeto orquestrado com base em um yaml\n"
###        - "\t**CHAVES:** -f -d (Opcional)\n"
###        - "**criar_doc:** Usado para gerar um documento de evidencia do projeto, com base no dos arquivos de resultados da pasta docs/reports"
###        - " as imagens para cada step deve conter o nome da funcionalidade, cenario e step no nome da imagem a qual ela pertence.\n"
###        - "\t**CHAVES:** -d(Opcional)\n"
###        - "**Master_Remote:** Usado para abrir um conector master para executar testes em clients remote\n"
###        - "\t**CHAVES:** -f \n"
###        - "**Client_Remote:** Usado para abrir um servidor master para executar testes\n"
###        - "\t**CHAVES:** -f \n"  
###        - "**Gerar_zip:** Usado para abrir um servidor master para executar testes\n"

###- annotation:
###    title: "**Parametros**\n"
###    text_description:
###        - "Os Parametros ou argumentos são passados para especificar a execução de um determinado comando.\n" 
###        - "**-f ou --file_yaml:** Arquivo Yaml base para execucoes em threads e containers.\n" 
###        - "**-n ou --nome_projeto:** Criar um projeto com a base do Pyautomators.\n"
###        - "**-d ou --diretorio:** Para indicar um diretorio para a execução das ações.\n"
###        - "**--volume_host:** Volume do host.\n"
###        - "**--volume_container:** Volume do container.\n"
###        - "**--master_host:** IP do master.\n"
###        - "**--instancia:** Instancia do Yaml a ser executada.\n"
###        - "**-i ou --retorn_result:** Retornar resultados.\n"
###    ex:
###        - python: "python -m Pyautomators execute -f data/run.yaml\n"
###        - python: "python -m Pyautomators criar_projeto -n Testes_Web\n"

    """Adicionando os argumento"""
    ARG.add_argument("comando",help="COMANDOS:\n\t<criar_projeto>\n\t<execute>\n\t<criar_doc>\n\t<Master_Remote>\n\t<Client_Remote>\n\t<Gerar_zip>")
    ARG.add_argument('-f','--file_yaml',required=False,help='Arquivo Yaml base para execucoes em threads e containers')
    ARG.add_argument("-n",'--nome_projeto',required=False,help="Criar um projeto com a base do Pyautomators")
    ARG.add_argument("-d",'--diretorio',default=Ambiente.path_atual(),required=False,help="Indique um diretorio para a execução das ações")
    ARG.add_argument('--volume_host',required=False,help="Volume do Host")
    ARG.add_argument('--volume_container',required=False,help="Volume do Container")
    ARG.add_argument('--master_host',required=False,help="IP do master")
    ARG.add_argument('--instancia',required=False,default=None,help='Instancia do Yaml a ser executada')
    ARG.add_argument("-i",'--retorn_result',default=False,help='Retornar resultados')
    projeto=vars(ARG.parse_args())

    """Chamadas de funcao para cada argumento"""
    if(projeto['comando']=='criar_projeto'):
        Project.Criar_Projeto(projeto['nome_projeto'], projeto['diretorio'])

    elif(projeto['comando']=="execute"):
        Ambiente.irDiretorio(Ambiente._tratar_path(projeto['diretorio']))
        orquestrador(projeto["file_yaml"],projeto['instancia'])

    elif(projeto['comando']=="criar_doc"):
        Ambiente.irDiretorio(Ambiente._tratar_path(projeto['diretorio']))
        path=Ambiente.path_atual()
        v=1
        for jsons in os.listdir(path+'docs/reports/'):
            print(jsons)
            if(jsons.find('.json')!=-1):
                criar_documento_cliente(path+'docs/doc{}.doc'.format(v), path+'docs/reports/'+jsons, path+'docs/')
                v+=1

    elif(projeto['comando']=="Master_Remote"):
        runner=Runner_Master(projeto["file_yaml"])
        runner.execute()
        runner.results()

    elif(projeto['comando']=="Client_Remote"):
        runner=Runner_Client(projeto["file_yaml"])
        runner.execute()
        runner.results()

    elif(projeto['comando']=="Gerar_zip"):
        shutil.make_archive("docs/docs", "zip",  base_dir="docs")
        shutil.make_archive('docs/logs',"zip",base_dir="log")
        
    else:
        Error="""
                Passe um valor de comando valido:
                COMANDOS:\n
                    criar_projeto: 
                    
                    execute:
                    
                    criar_doc: 
                    
                    Master_Remote:
                    
                    Client_Remote:
                    
                    Gerar_zip:
                """
        raise Exception(Error)
    