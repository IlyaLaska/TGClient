from requests import get, post
from bs4 import BeautifulSoup
import re
#TODO handle faild request
def getUrl(url, payload, headers):
  try:
    result = get(url, data=payload, headers=headers)
    if result.status_code == 200:
      return result.text
    else:
      return None
  # except RequestException as e:
  #   print(e)
  #   return None
  except:
    print('Request failed. Probable cause - no internet connection')
    return None


def parseWeather(weather):
  soup = BeautifulSoup(weather, 'html.parser')
  overview = soup.find('div', {'class':'hourly-table overview-hourly'}).find_all('td')
  # print(overview)
  precip = soup.find('div', {'class':'hourly-table precip-hourly'}).find_all('td')

  text = ['', '', '', '', '', '', '', '']
  pos = 0
  for td in overview:
    if td.div:#add time
      text[pos] += str(td.div.text).zfill(4) + ' '
      pos += 1
    if td.span:#add temp
      strn = td.span.text
      if strn.find('°') > -1:
        if len(strn) == 2:
          strn = '0' + strn
        text[pos] += strn.zfill(3) + ' '
        pos += 1
    if pos == 8:#reset pos
      pos = 0
  # for hour in text:
  #   print(hour)
  #   hour += '|||'
  #   print(hour)
  for td in precip:
    if td.span and pos < 8:#add rain prob
      strn = str(td.span.text)
      if strn.find('%') > -1:
        if len(strn) == 2:
          strn += ' '
        text[pos] += strn + ' '#dealt with double digits

        pos += 1
    if pos == 8:#reset pos
      pos = 0
  # pos = 0
  for td in overview:
    if td.span and not re.search(r'\d', td.span.text):
      strn = td.span.text
      StrPos = strn.find('ly')
      if StrPos > -1:
        strn = strn[:StrPos] + strn[StrPos+2:]
      text[pos] += '' + strn
      pos += 1
  return text


def stringifyText(text):
  result = '** Time  T° Feel Rain Snow Ice Sky**\n--------------------------------------------------------------\n'
  for hour in text:
    result += hour + '\n'
  return result

# a = getUrl('https://www.google.com/search?source=hp&ei=rSTVXMeRL8ewrgS06I_QDg&q=weather&oq=&gs_l=psy-ab.1.0.35i39l6.0.0..10537...1.0..1.327.567.2-1j1......0......gws-wiz.....6.Roghf-ajiDs', '')
# a = getUrl('https://www.google.com/search?q=weather&amp;ie=UTF-8&amp;gbv=1&amp;sei=XibVXNyePKGk1fAPncaSyAg', '')
def scrapeWeather():
  weather = getUrl('https://www.accuweather.com/en/ua/kyiv/324505/hourly-weather-forecast/324505', payload='', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
  if not weather:
    return None
  text = parseWeather(weather)
  res = stringifyText(text)
  return res

# print(scrapeWeather())
# page = getUrl('https://www.google.com/search?oq=weather', '')
