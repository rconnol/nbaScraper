import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver


def remove_punctuation(s):
    s = ''.join([i for i in s if i not in ".,'"])
    return s


def process_id(roster):
    roster['538id'] = roster['Player'].apply(remove_punctuation)
    roster['538id'] = roster['538id'].apply(lambda x: x.replace(" ", "-"))
    roster['538id'] = roster['538id'].apply(lambda x: x.lower())
    roster['538id'].replace(name_corrections, inplace=True)

    return roster


def nba_links():
    active_links = []
    inactive_links = []

    for player in roster['538id']:

        target_url = url + player + '/'

        try:
            page = urlopen(target_url)
        except:
            inactive_links.append(target_url)
            print(player + " - no web page available")
            continue

        active_links.append(target_url)

    return active_links


def initialize_web_driver(url):

    driver = webdriver.Firefox()

    driver.get(url)

    html = driver.page_source

    driver.quit()

    return html


def read_player(player, target_url):
    
    not_in_carmelo = []   
    
    url = target_url + player + '/'

    try:

        page = initialize_web_driver(url)

    except:

        not_in_carmelo.append(player)
        print(player + " - no data available")
        return 'No Data'

    print(player)

    return page

def return_table_data(page):

    soup = BeautifulSoup(page, 'lxml')

    rows = soup.find_all('tr')

    for row in rows:

        cells = row.findChildren('td')

        print(cells.text)


if __name__ == '__main__':

    
    roster = pd.read_csv('~/nbaData/roster/roster.csv')

    url = 'http://projects.fivethirtyeight.com/carmelo/'

    name_corrections = {
    
    'matt-dellavedova' : 'matthew-dellavedova',
    'marcelinho-huertas' : 'marcelo-huertas',
    'derrick-jones' : 'derrick-jones-jr',
    'john-lucas' : 'john-lucas-iii',
    'james-mcadoo' : 'james-michael-mcadoo',
    'raulzinho-neto' : 'raul-neto',
    'otto-porter' : 'otto-porter-jr',
    'glenn-robinson' : 'glenn-robinson-iii',
    'domas-sabonis' : 'domantas-sabonis',
    'lou-williams' : 'louis-williams',
    'joe-young' : 'joseph-young',

}
    
    roster = process_id(roster)

    code = read_player(roster['538id'][15],url)

    print(code)
