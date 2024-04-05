import sys
# 크롤링에 필수적인 App 2가지 설치
import requests  # 사전에 pip install requests 필요
from bs4 import BeautifulSoup  # 사전에 pip install beautifulsoup4 필요

from PyQt5 import uic  # 사전에 pip install PyQt5 필요
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from_class = uic.loadUiType("ui/weather.ui")[0]

class WeatherApp(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("img/emoji.png"))
        self.statusBar().showMessage("WEATHER SEARCH APP Ver 0.5")

        self.search_btn.clicked.connect(self.weather_search)

    def weather_search(self):
        inputArea = self.area_input.text()

        weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")

        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
        # print(weatherSoup)

        # 날씨지역이름 가져오기
        areaText = weatherSoup.find("h2", {"class": "title"}).text  # tag는 필요없고 text만 추출
        areaText = areaText.strip()
        print(f"지역이름: {areaText}")

        todayTempText = weatherSoup.find("div", {"class": "temperature_text"}).text
        todayTempText = todayTempText[6:12].strip()
        # print(todayTempText[6:11])
        print(f"현재온도: {todayTempText}")

        yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text
        yesterdayTempText = yesterdayTempText[:15].strip()
        print(f"어제날씨비교: {yesterdayTempText}")

        todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text
        todayWeatherText = todayWeatherText.strip()
        print(f"오늘날씨: {todayWeatherText}")

        senseTempText = weatherSoup.find("dd", {"class": "desc"}).text
        senseTempText = senseTempText.strip()
        print(f"체감온도: {senseTempText}")

        # 미세먼지, 초미세먼지, 자외선, 일몰 등 모두 갖고 옴
        todayInfoText = weatherSoup.select("ul.today_chart_list>li")
        # print(todayInfoText[0:2])

        dustInfo = todayInfoText[0].find("span", {"class": "txt"}).text
        dustInfo = dustInfo.strip()
        print(f"미세먼지: {dustInfo}")

        superdustInfo = todayInfoText[1].find("span", {"class": "txt"}).text
        superdustInfo = superdustInfo.strip()
        print(f"초미세먼지: {superdustInfo}")

        # 크롤링한 날씨정보텍스트를 준비된 UI에 출력하기
        self.area_disp.setText(areaText)
        self.setWeatherImage(todayWeatherText)
        self.now_temp.setText(todayTempText)
        self.label_compare.setText(yesterdayTempText)
        self.feel_temp_no.setText(senseTempText)
        self.dust_level.setText(dustInfo)
        self.super_dust_level.setText(superdustInfo)

    def setWeatherImage(self, weatherText):
        if weatherText == "맑음":
            weatherImage =QPixmap("img/sun.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        elif weatherText == "구름많음":
            weatherImage =QPixmap("img/cloud.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        elif weatherText == "흐림":
            weatherImage = QPixmap("img/cloud.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        elif weatherText == "눈":
            weatherImage =QPixmap("img/snow.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        elif weatherText == "비":
            weatherImage =QPixmap("img/rain.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        elif weatherText == "소나기":
            weatherImage =QPixmap("img/rain.png")
            self.weather_image.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_image.setText(weatherText)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())


