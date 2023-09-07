from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service= servico)
wait = WebDriverWait(navegador, 3600)

nome_do_arquivo = 'a.xlsx'  # Arquivo ontem contem os links de pesquisa dos jogadores
urls_jogadores = pd.read_excel(nome_do_arquivo, sheet_name='Plan1')  # Leitura da planilha




# DataFrame vazio para acumular informações
dataframeInfoF = pd.DataFrame()
for url in urls_jogadores['Link']:
    #Abrindo o navegador com os links da planilha
    navegador.get(url)

    #Esperando a pagina carregar
    wait.until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/div[3]')))

    #Encontrando a tabela ao lado da foto do jogador
    div_element = navegador.find_element('xpath', '/html/body/div[2]/div[3]')  


    # Pegando o html da page
    div_html = div_element.get_attribute('outerHTML')

    # Analisando o HTML com BeautifulSoup
    soup = BeautifulSoup(div_html, 'html.parser')

    #Encontrando a tabela com as informações do jogador
    elemento = soup.find('div',class_='players open')
    #pegando as linhas da tabela
    elementoDoElemento = elemento.find_all('p')

    #Pegando o nome do jogador
    info = {"Nome":(soup.find('h1')).text}
    #preenchendo os campos que nao possui o :
    index = 1
    for aqui in elementoDoElemento:
        
        #Caso o <p> venha com mais de 1 :
        if len(aqui.text.split(':')) >= 2:
            #Usando a primeira parte do : como nome da coluna que vai estar no dataframe
            chave = ((aqui.text).split(':')[0]).replace('\n', '').replace('\t', '')
            #o valor que vai ser preenchido no dataframe
            valor = ((aqui.text).split(':')[1]).replace('\n', '').replace('\t', '')
            #Verificando se é o <p> da data de nascimento
            if re.findall("\d+\/.+\/\d+", valor):
                valor = re.findall("\d+\/.+\/\d+", valor)
            #Montando o dataframe sem o ['']   
            info[chave] = valor[0]
            #Caso o <p> venha com 1 : 
        elif len(aqui.text.split(':')) <= 2:
            #Preenchendo a coluna com um numero para nao ficar vazia
            chave = index
            #Valor preenchido no dataframe com o valor do <p> encontrado
            valor = aqui.text
            #Montando o dataframe
            info[chave] = valor
            index += 1

    # Cria um DataFrame a partir do dicionário e adiciona-o ao DataFrame acumulado
    dataframeInfo = pd.DataFrame([info])
    dataframeInfoF = dataframeInfoF._append(dataframeInfo, ignore_index=True)

#Montando a planilha
dataframeInfoF.to_excel('Valor Final.xlsx',index = False)


