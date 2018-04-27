#
# Funções do hash_useless, onde todo o trabalho funciona.
#
# Funções: 
# Display Message() HashFile()  ValidateDirectory()
# ParseCommandLine()  WalkPath()
# ValidateDirectoryWritable() Ascii()

import os       
import stat         
import time
import hashlib
import argparse
import csv
import logging



# Nome: ParseCommand() - Função

# Desc: Processa e válida os comandos.
# Usa a bilioteca padrão "Argparse"
# Input: none

# Actions:
# Usa a biblioteca padrão "Argparse" para processar as linhas de comando
# Estabelece variaveis globais onde qualquer função pode obte-los.

def Ascii():
    print("""
    888                     888      
    888                     888      
    888                     888      
    88888b.  8888b. .d8888b 88888b.  
    888 "88b    "88b88K     888 "88b 
    888  888.d888888"Y8888b.888  888 
    888  888888  888     X88888  888 
    888  888"Y888888 88888P'888  888 """)
    time.sleep(2)
    print("""
                            888                         
                            888                         
                            888                         
    888  888.d8888b  .d88b. 888 .d88b. .d8888b .d8888b  
    888  88888K     d8P  Y8b888d8P  Y8b88K     88K      
    888  888"Y8888b.8888888888888888888"Y8888b."Y8888b. 
    Y88b 888     X88Y8b.    888Y8b.         X88     X88 
    "Y88888 88888P' "Y8888 888 "Y8888  88888P' 88888P' """)
    time.sleep(2)
    print("""                                                    
    888                   888 
    888                   888 
    888                   888 
    888888 .d88b.  .d88b. 888 
    888   d88""88bd88""88b888 
    888   888  888888  888888 
    Y88b. Y88..88PY88..88P888 
    "Y888  "Y88P"  "Y88P" 888 """)
def ParseCommandLine():
    parser = argparse.ArgumentParser('Sistema de hashing em Python: P-Fish')
    parser.add_argument('-v','--verbose', help="Permite mostrar mensagens sobre o progresso",action='store_true')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--md5',help="Especifica a Hash pelo algoritmo MD5",action="store_true")
    group.add_argument('--sha256',help="Especifica a Hash pelo algoritmo SHA-256",action="store_true")
    group.add_argument('--sha512',help="Especifica a Hash pelo algoritmo SHA-512",action="store_true")
    
    parser.add_argument("-d","--rootPath",type=ValidateDirectory,required=True,help="Especifica o diretório root para o Hash")
    parser.add_argument("-r","--reportPath",type=ValidateDirectoryWritable,required=True,help="Especifica o diretório e um arquivo log será escrito")

    global gl_args
    global gl_hashtype
    gl_args = parser.parse_args()
    if gl_args.md5:
        gl_hashtype = "MD5"
    elif gl_args.sha256:
        gl_hashtype = "SHA256"
    elif gl_args.sha512:
        gl_hashtype = "SHA512"
    else:
        gl_hashtype = "Unknown"
        logging.error("Tipo de Hash desconhecida. Um argumento(válido) para Hash deve ser passado")
    DisplayMessage("Resultado da linha de comando: Sucesso")
    return
# Fim da Função: ParseCommandLine ===========================================================================


# N: WalkPath() - Função

# Desc: Caminha sobre o caminho especificado na linha de comando
# Usa a biblioteca sys e OS

# Input: none, Usa argumentos de linha de comando

# Actions:
# Usa as bibliotecas padrões sys e os 
# para atravesssar a estrutura do caminho começando no caminho
# root especificado pelo usuário. Para cada arquivo descoberto, a função WalkPath
# vai chamar a função HashFile() para fazer o hashing dos arquivos

def WalkPath():
    processCount = 0
    errorCount = 0
    logging.info("Caminho do root: " + gl_args.rootPath)

    text = open(gl_args.reportPath+"relatorio.csv", 'w',newline='')
    reader = csv.writer(text)
    reader.writerow(["Arquivo:","Caminho:","Tamanho(MB):","Data(modificação):","Data(Acesso):",
    "Data(Criação):","Hash({}):".format(gl_hashtype),"ID(dono):","ID(grupo):","Modo(bin)"])
    for root, dirs, files in os.walk(gl_args.rootPath):
        del dirs
        for file in files:
            fname = os.path.join(root, file)
            result = HashFile(fname, file, text)
           #Se o Hashing foi um sucesso, então encrementa mais 1 
            if result is True:
                processCount += 1
            else:
                errorCount += 1
    text.close()
    return processCount 
# Fim da função WalkPath() ===========================================


# Nome: HashFile() - Função
#
# Desc: Processa um único arquivo que inclui a execução de um hash do arquivo
# E a extração da metadata referente ao arquivo processado
# Usa os módulos padrões hashlib, os, e sys

# Input: theFile = O caminho completo do Path do arquivo
# simpleName = Apenas o nome em si

# Actions:
# Tenta fazer o hash do arquivo e extrair a metadata
# Chama o gerador de relatórios para as execuções com sucesso


def HashFile(theFile, simpleName, o_result):
    # Verifica se o caminho especificado realmente existe
    if os.path.exists(theFile):
        # Verifica se o caminho especificado não é apenas um link
        if not os.path.islink(theFile):
            # Verifica se o arquivo no path é REAL
            if os.path.isfile(theFile):
                try:
                    # Tenta abrir  arquivo
                    f = open(theFile, 'rb')
                    rd = f.read()
                    #theFileStats = os.stat(theFile)
                    mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = os.stat(theFile)
                    DisplayMessage("Arquivo sendo processado: " + str(theFile))
                    del ino,dev,nlink
                    fileSize = str(size)
                    modifiedTime = time.ctime(mtime)
                    accessTime = time.ctime(atime)
                    createdTime = time.ctime(ctime)
                    ownerID = str(uid)
                    groupID = str(gid)
                    #filemode = bin(mode)
                    # Se a opção for --md5
                    if gl_args.md5:
                        hash = hashlib.md5()
                        hash.update(rd)
                        hexMD5 = hash.hexdigest()
                        hashvalue = hexMD5.upper()
                    # Se a opção for --sha256
                    elif gl_args.sha256:
                        hash = hashlib.sha256()
                        hash.update(rd)
                        hexSHA256 = hash.hexdigest()
                        hashvalue = hexSHA256.upper()
                    # Se a opção for --sha512
                    elif gl_args.sha512:
                        hash = hashlib.sha512()
                        hash.update(rd)
                        hexSHA512 = hash.hexdigest()
                        hashvalue = hexSHA512.upper()
                    else: 
                        logging.error("Hash não selecionada")
                    f.close()
                    o_result.write(str(simpleName)+'\t'+theFile+'\t'+
                    str((int(fileSize)/1024)/1024)+'MB'+'\t'+modifiedTime+'\t'+accessTime+'\t'
                    +createdTime+'\t'+
                    str(hashvalue)+'\t'+ownerID+'\t'+groupID+'\t'+str(mode)+'\n')
                    return True
                except IOError:
                    logging.warning("Falha ao tentar abrir: {}".format(str(theFile)))
                    return False
                else:
                    logging.warning( '['+ repr(simpleName) +', Pulou um não-arquivo'+']' )
                    return False 
        else:
            logging.warning( '['+ repr(simpleName) +', Pulou um link não um arquivo'+']' )
            return False
    else:
        logging.warning( '['+ repr(simpleName) +', Caminho não existente'+']' )
        return False
# Fim da função HashFile() ==========================================================


# Nome: ValidateDirectory - Função

# Desc: Função que vai validar se um caminho 
# existe e se pode ser lido. Usado apenas para a validação.

# Input: Uma string contendo um diretório

# Actions:
# Se válidado, irá retornar uma string
# Se for inválido, irá retornar: "raise an ArgumentTypeError" da ArgParse
# que irá virar um relatório com argumentos para o usuário


def ValidateDirectory(theDir):
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError("O diretório não existe!")
    if os.access(theDir, os.R_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError("O diretório não pode ser lido. Falta de permissões.")
# Fim da função ValidateDirectory() =============================================================


# Nome: ValidateDirectoryWritable() - Função

# Desc: Função que vai validar se um caminho
# existe e se pode ser escrito. Usado para a validação de argumentos apenas.

# Input: Uma string com um caminho.

# Actions:
# Se for válido vai retornar uma string com um caminho de diretório.

# Se válidado, irá retornar uma string
# Se for inválido, irá retornar: "raise an ArgumentTypeError" da ArgParse
# que irá virar um relatório com argumentos para o usuário


def ValidateDirectoryWritable(theDir):
    # Verifica se o caminho não é um diretório
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('O Diretório não existe!')
    # Verifica se o caminho é editável
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('O diretório não pode ser escrito. Falta de permissões.')

# Fim da função ValidateDirectoryWritable() =============================================================


# Nome: DisplayMessage() - Função

# Desc: Exibe a mensagem se o comando verbose foi ativado na linha de comando.

# Input: Mensagem do tipo string.

# Actions:
# Usa a função padrão print para imprimir a mensagem.


def DisplayMessage(msg):
    if gl_args.verbose:
        print("==========================")
        print(msg)
    return 
# Fim da função DisplayMessage() =============================================================



