# Importação das bibliotecas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import openpyxl

# Importando e inicializando o driver do Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-animations")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
s = Service("chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)

df = pd.DataFrame(columns=['Time', 'Nome', 'Posição', 'Jogos', 'Gols', 'Assistências', 'Minutos'])
links = ['https://www.transfermarkt.com.br/atletico-mineiro/leistungsdaten/verein/330/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/botafogo-fr/leistungsdaten/verein/537/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/ceara-sc/leistungsdaten/verein/2029/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/cr-flamengo/leistungsdaten/verein/614/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/cr-vasco-da-gama/leistungsdaten/verein/978/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/cruzeiro-ec/leistungsdaten/verein/609/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/ec-bahia/leistungsdaten/verein/10010/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/ec-juventude/leistungsdaten/verein/10492/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/ec-vitoria/leistungsdaten/verein/2125/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/fluminense-fc/leistungsdaten/verein/2462/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/fortaleza-ec/leistungsdaten/verein/10870/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/gremio-fbpa/leistungsdaten/verein/210/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/mirassol-fc/leistungsdaten/verein/3876/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/rb-bragantino/leistungsdaten/verein/8793/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/santos-fc/leistungsdaten/verein/221/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/sao-paulo-fc/leistungsdaten/verein/585/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/sc-corinthians/leistungsdaten/verein/199/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/sc-internacional/leistungsdaten/verein/6600/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/se-palmeiras/leistungsdaten/verein/1023/reldata/%262024/plus/1',
         'https://www.transfermarkt.com.br/sport-recife/leistungsdaten/verein/8718/reldata/%262024/plus/1']

for link in links:

    # Carregar a página após aceitar os cookies
    driver.get(link)
    time.sleep(5)

    team = driver.find_element(By.XPATH, '/html/head/title').get_attribute('innerHTML').replace(' - Desempenho - Plantel (Visão detalhada) | Transfermarkt', '')
    #print(team)

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
        
        df.loc[len(df)] = [team, name, position, games, goals, assist, minutes]

        i = i + 1

df['G+A'] = df['Gols'] + df['Assistências']

df['G+A / J'] = df['G+A'] / df['Jogos']

df['Min / G+A'] = df['Minutos'] / df['G+A']

df.sort_values('Min / G+A', ascending=True, inplace=True)
df.to_excel("C:/VScode_projects/soccerstats/goals_assist.xlsx", index=False)

#while True:
#    time.sleep(1)
