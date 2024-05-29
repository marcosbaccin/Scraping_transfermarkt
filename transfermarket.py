# Importação das bibliotecas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import requests

# Importando e inicializando o driver do Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-animations")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
s = Service("chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)

# Dataframe que guardará as informações dos jogadores
df = pd.DataFrame(columns=['Time', 'Nome', 'Posição', 'Jogos', 'Gols', 'Assistências', 'Minutos'])

# Links das páginas de dados de desempenho detalhados de cada clube da Série A
links = ['https://www.transfermarkt.com.br/athletico-paranaense/leistungsdaten/verein/679/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/atletico-goianiense/leistungsdaten/verein/15172/reldata/%2620231/plus/1',
         'https://www.transfermarkt.com.br/atletico-mineiro/leistungsdaten/verein/330/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/botafogo-fr/leistungsdaten/verein/537/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/cr-flamengo/leistungsdaten/verein/614/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/cr-vasco-da-gama/leistungsdaten/verein/978/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/criciuma-ec/leistungsdaten/verein/7178/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/cruzeiro-ec/leistungsdaten/verein/609/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/cuiaba-ec/leistungsdaten/verein/28022/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/ec-bahia/leistungsdaten/verein/10010/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/ec-juventude/leistungsdaten/verein/10492/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/ec-vitoria/leistungsdaten/verein/2125/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/fluminense-fc/leistungsdaten/verein/2462/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/fortaleza-ec/leistungsdaten/verein/10870/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/gremio-fbpa/leistungsdaten/verein/210/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/rb-bragantino/leistungsdaten/verein/8793/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/sao-paulo-fc/leistungsdaten/verein/585/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/sc-corinthians/leistungsdaten/verein/199/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/sc-internacional/leistungsdaten/verein/6600/reldata/%262023/plus/1',
         'https://www.transfermarkt.com.br/se-palmeiras/leistungsdaten/verein/1023/reldata/%262023/plus/1']

response = requests.get(links[0])
cookies = response.cookies
driver = webdriver.Chrome()

for cookie in cookies:
    driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'path': cookie.path, 'domain': cookie.domain})

for link in links:

    # Carregar a página após aceitar os cookies
    driver.get(link)

    # Pega o nome do time
    team = driver.find_element(By.XPATH, '/html/head/title').get_attribute('innerHTML').replace(' - Desempenho - Plantel (Visão detalhada) | Transfermarkt', '')
    #print(team)

    # Pega a tabela onde se encontra os dados de todos os jogadores do time
    tabela = driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody')
    trs_odd = tabela.find_elements(By.CLASS_NAME, 'odd')
    trs_even = tabela.find_elements(By.CLASS_NAME, 'even')
    players = []

    for tr in trs_odd:
        players.append(tr)
    for tr in trs_even:
        players.append(tr)

    #print(len(players))
    i = 1
    # Pega todas os dados referentes aos jogadores, como nome, posição, gols, assistências e minutos jogados
    for player in players:
        name = player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[2]/table/tbody/tr[1]/td[2]/div[1]/span/a').get_attribute('innerHTML')
        position = player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[2]/table/tbody/tr[2]/td').get_attribute('innerHTML')
        
        try:
            games = int(player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[6]').get_attribute('innerHTML'))
        except:
            games = 0
        
        try:
            goals = int(player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[7]').get_attribute('innerHTML'))
        except:
            goals = 0
        
        try:
            assist = int(player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[8]').get_attribute('innerHTML'))
        except:
            assist = 0
        
        try:
            minutes = int(player.find_element(By.XPATH, f'/html/body/div/main/div[1]/div/div/div[3]/div/table/tbody/tr[{i}]/td[15]').get_attribute('innerHTML').replace("'", "").replace(".", ""))

        except:
            minutes = 0

        # Carrega os dados do jogador no Dataframe
        df.loc[len(df)] = [team, name, position, games, goals, assist, minutes]

        i = i + 1

# Cria os campos de Participação direta em gols (Gols + Assistências), Gols + Assist. por jogo e minutos para participar de um gol
df['G+A'] = df['Gols'] + df['Assistências']

df['G+A / J'] = df['G+A'] / df['Jogos']

df['Min / G+A'] = df['Minutos'] / df['G+A']

# Salva os dados em uma planilha excel
df.sort_values('Min / G+A', ascending=True, inplace=True)
df.to_excel("C:/VScode_projects/soccerstats/goals_assist.xlsx", index=False)

#while True:
#    time.sleep(1)
