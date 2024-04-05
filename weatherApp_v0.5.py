# 크롤링에 필수적인 App 2가지 설치
import requests  # 사전에 pipinstall requests 필요
from bs4 import BeautifulSoup  # 사전에 pipinstall beautifulsoup4 필요

# https://search.naver.com/search.naver?&query=한남동날씨

inputArea = input("날씨를 조회하려는 지역을 입력하세요:")

weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
# print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
# print(weatherSoup)

# 날씨지역이름 가져오기
areaText = weatherSoup.find("h2", {"class":"title"}).text  # tag는 필요없고 text만 추출
areaText = areaText.strip()
print(f"지역이름: {areaText}")

todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text
todayTempText = todayTempText[6:11].strip()
# print(todayTempText[6:11])
print(f"현재온도: {todayTempText}")

yesterdayTempText = weatherSoup.find("p", {"class":"summary"}).text
yesterdayTempText = yesterdayTempText[:15].strip()
print(f"어제날씨비교: {yesterdayTempText}")

todayWeatherText = weatherSoup.find("span", {"class":"weather before_slash"}).text
todayWeatherText = todayWeatherText.strip()
print(f"오늘날씨: {todayWeatherText}")

senseTempText = weatherSoup.find("dd", {"class":"desc"}).text
senseTempText = senseTempText.strip()
print(f"체감온도: {senseTempText}")

# 미세먼지, 초미세먼지, 자외선, 일몰 등 모두 갖고 옴
todayInfoText = weatherSoup.select("ul.today_chart_list>li")
# print(todayInfoText[0:2])

dustInfo = todayInfoText[0].find("span", {"class":"txt"}).text
dustInfo = dustInfo.strip()
print(f"미세먼지: {dustInfo}")

superdustInfo = todayInfoText[1].find("span", {"class":"txt"}).text
superdustInfo = superdustInfo.strip()
print(f"초미세먼지: {superdustInfo}")




