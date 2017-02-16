import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def read_roster(url):
        
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    page.close

    rows = soup.find_all('tr')
    data = []

    for row in rows:
        info = {}
        cells = row.findChildren('td')
    
        for cell in cells:
            info[cell['data-th']] = cell.text
            data.append(info)
            
        
    frame = pd.DataFrame(data)
    frame.dropna(inplace=True)
    return frame



if __name__ == '__main__':

    url = "http://basketball.realgm.com/nba/players"

    frame = read_roster(url)

    frame.to_csv('roster.csv', encoding='utf-8')
