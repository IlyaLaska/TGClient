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

def getVotes():
  patio = getUrl('https://gb.kyivcity.gov.ua/projects/11/2147', '', '')
  patioSoup = BeautifulSoup(patio, 'html.parser')
  hub = getUrl('https://gb.kyivcity.gov.ua/projects/11/2149', '', '')
  hubSoup = BeautifulSoup(hub, 'html.parser')
  # print(patioSoup.prettify())
  patioVotes = patioSoup.find_all('strong')
  hubVotes = hubSoup.find_all('strong')
  # print(patioVotes[6].text)
  result = '**Патио(Сквер): ' + patioVotes[6].text + '**\n' + '**Патио Хаб(Белка): ' + hubVotes[6].text + '**'
  return result

# print(getVotes())
