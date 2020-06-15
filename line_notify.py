import requests
from bs4 import BeautifulSoup

# 武漢疫情通知
LINE_NOTIFY_TOKEN = 'KKuN5pic5SOeGaWYGIwcxrGX5B9CUrubZVEsEyo2kyr'

def crawl():
  # 資料來源：yahoo新聞
  info_url = "https://news.campaign.yahoo.com.tw/2019-nCoV/index.php"

  response = requests.get(info_url)
  soup = BeautifulSoup(response.text, "html.parser")
  row_list = soup.select(".row")

  update_time = soup.select(".update-box .time")[0].string.split("日")[0] + "日"

  message = "\n{}".format(update_time)
  
  for row in row_list:
    country = row.select(".dataCountry p")[0].string
    total_confirmed = row.select(".current")[0].string
    new_confirmed = row.select(".no")[0].string.split('+')[1]

    # if country == "全球":
      # new_confirmed = str(format(int(new_confirmed),","))

    mortality = row.select(".current")[1].string
    mortality_rate = int(int(mortality.replace(",", "")) / int(total_confirmed.replace(",", "")) * 100)

    message += "\n\n{}\n確診： {}\n本日新增： {}".format(country, total_confirmed, new_confirmed)

  return message

def line_noify_message(token, msg):
  headers = {
      "Authorization": "Bearer " + token, 
      "Content-Type" : "application/x-www-form-urlencoded"
  }

  payload = {
  	'message': msg,
  }

  r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
  return r.status_code

if __name__ == '__main__':
  message = crawl()
  line_noify_message(LINE_NOTIFY_TOKEN, message)
