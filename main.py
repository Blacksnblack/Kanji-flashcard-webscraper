import requests
from bs4 import BeautifulSoup

saveFileName = "kanjiG"  # kanji (G)rade [grade number] [.txt]

url = "https://kanjicards.org/kanji-list-by-grade.html"
mainurl = "https://kanjicards.org/"

data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')

# get list of all kanji links
grades = []
for p in soup.find_all('p'):
    item = p.find_all('a', href=True)
    if len(item) > 0:
        grades.append(item)

for grade in range(len(grades)):
    # for each link goto the website and scrape the data
    cards = []
    for i, item in enumerate(grades[grade]):
        print(f"Grade {grade+1}/{len(grades)} :: card {i + 1}/{len(grades[grade])}")
        try:
            tempData = requests.get(mainurl + item['href'])
            tempSoup = BeautifulSoup(tempData.text, 'html.parser')

            # print(tempData.text)

            kanji = [a.text for a in tempSoup.find_all('h2')][0]
            for listItem in tempSoup.find_all('li'):
                if 'kun' in listItem.text[:3]:
                    kun = listItem.text
                elif "on" in listItem.text[:2]:
                    on = listItem.text
                elif "meaning" in listItem.text[:7]:
                    meaning = listItem.text

            # print([a.text for a in tempSoup.find_all('li')])

            cardData = [kanji, kun, on, meaning]
            # cardData = {"kanji": kanji, "kun": kun, "on": on, "meaning": meaning}

            # print(cardData)
            cards.append(cardData)
        except Exception as E:
            print(f"Error: loading webpage; {i}/{len(grades[grade])} completed.")
            break

    print("~~~Saving Data...")
    f = open(saveFileName + f"{grade+1}.txt", "w", encoding="utf8")
    for item in cards:
        f.write(f"{item[0]}~{item[1]}\n{item[2]}\n{item[3]}\n\n")
    f.close()
    print("~~~Data Saved")

print("DONE!!!")