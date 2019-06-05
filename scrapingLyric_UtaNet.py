import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

#取得対象（検索結果一覧）のURL定義
strUrl = 'https://www.uta-net.com/artist/18955/'
#置換対象の文字列定義
strBeforeCode = 'http://www.utamap.com/showkasi.php?surl='
#置換後の文字列定義
strAfterCode = 'http://www.utamap.com/phpflash/flashfalsephp.php?unum='
#歌詞ファイル出力先
lyricDir = r'G:\01.work\01.project\00.CloudWord\lyric' + '\\'

#Uta-Netの結合URL
lyricURL = 'https://www.uta-net.com'

#postgreSQL connect関数
def get_connection():
    strCon = " user=postgres dbname= LoveLive_music password= ll0630 port= 5432 host= localhost"
    return psycopg2.connect(strCon)

#requestsを用いてWebページのHTMLを取得する
def get_Html(url):
    responceList = requests.get(url)
    responceList.status_code
    #BeautifulSoupを用いてURL要素を抽出する
    soup = BeautifulSoup(responceList.content,"lxml")
    return soup

#歌詞ページから歌詞だけを抽出する
def get_lyric(url):
    responceList = requests.get(url)
    responceList.status_code
    #BeautifulSoupを用いてURL要素を抽出する
    soup = BeautifulSoup(responceList.content,"lxml")
    lyric = soup.find_all(id='kashi_area')
    #print(lyric[0].text)
    return lyric[0].text

soupList = get_Html(strUrl)
classUrl = soupList.find_all(class_='td1')

#メイン処理
urls = []
for tags in classUrl:
    aTag = tags.select('a')
    for a in aTag:
        url = lyricURL + a.attrs['href']
        urls.append(url)
        #urls.append(a.attrs['href'])

#CSV作成
f = open(lyricDir + 'lyric_{0:%Y%m%d%H%M%S}'.format(datetime.now()) + '.csv','w')
writer = csv.writer(f, lineterminator='\n')
csvlist = []
#抽出したURLを元に歌詞を取得する
for lyricUrl in urls:
    soup = get_lyric(lyricUrl)
    print(soup)
    csvlist.append(soup)

# 出力
writer.writerow(csvlist)

# ファイルクローズ
f.close()
