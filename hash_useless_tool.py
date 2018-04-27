#
# p-fish : Sistema de hash escrito em Python

import logging
import time
import sys
import hash_useless_fucking_sucking_tits_tool
# hash_useless_fucking_suck_tits_tool Módulo para funções de suporte, que sustentam esse arquivo.

if __name__ == '__main__':
    hash_ ='1.0'
    # Inicia o logging
    logging.basicConfig(filename='hash_log.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    # Processa as linhas de comando
    hash_useless_fucking_sucking_tits_tool.ParseCommandLine()
    # Salva o tempo de inicio
    startTime = time.time()
    # Salva uma mensagem de boas-vindas
    logging.info('Hash Useless Tool-----Novo escaneamento iniciado.')
    logging.info( '' )
    hash_useless_fucking_sucking_tits_tool.Ascii()
    print("\nEu odeio minha vida...\n")
    time.sleep(2)
    time.sleep(1)
    # Salve algumas informações a respeito do sistema
    logging.info( 'Sistema: ' + sys.platform)
    logging.info( 'Versão: ' + sys.version)
    # Atravessa os arquivos do sistema e faz uma chave hash para os arquivos.
    filesProcessed = hash_useless_fucking_sucking_tits_tool.WalkPath()
    # Salva o fim e termina e faz o cálculo de tempo
    endTime = time.time()
    duration = endTime - startTime
    logging.info('Arquivos processados: '+ str(filesProcessed))
    logging.info('Tempo de execução durou: '+ str(duration) +'seconds')
    logging.info('')
    logging.info('O programa foi executado normalmente.')
    logging.info('')
    hash_useless_fucking_sucking_tits_tool.DisplayMessage("Um arquivo chamado \"hash_log.log\" foi criado no diretório atual.")
    hash_useless_fucking_sucking_tits_tool.DisplayMessage("Um arquivo chamado \"relatorio.csv\" foi criado no caminho especificado.")
    hash_useless_fucking_sucking_tits_tool.DisplayMessage("Fim do programa.")