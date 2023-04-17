import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_champions():
    url = "https://leagueoflegends.fandom.com/wiki/List_of_champions"
    html = requests.get(url)
    page = BeautifulSoup(html.content, "html.parser")
    table = page.find('table', class_='article-table')

    skin_url = "https://leagueoflegends.fandom.com/wiki/List_of_skins_by_champion"
    skin_html = requests.get(skin_url)
    skin_page = BeautifulSoup(skin_html.content, "html.parser")
    skin_table = skin_page.find('table', class_='article-table')

    champions = []

    rows = table.find_all('tr')
    skin_rows = skin_table.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all('td')
        name = cells[0]["data-sort-value"]
        release_date = cells[2].text.strip()
        date_obj = datetime.strptime(release_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        for skin_row in skin_rows[1:]:
            skin_cells = skin_row.find_all("td")
            if skin_cells[0]["data-champion"] == name:
                skin_count = int(skin_cells[5].text)
                last_skin_days_ago = 0 if skin_cells[7].text == "Upcoming" else int(skin_cells[7].text)
                break
        champions.append({"champion_name": name, "champion_release_date": formatted_date, "champion_skin_count": skin_count, "champion_last_skin_days_ago": last_skin_days_ago})
    
    return champions

if __name__ == "__main__":
    print(get_champions())