from requests import get, post
from bs4 import BeautifulSoup

defUrl = 'http://rozklad.kpi.ua/Schedules/'
mainPageUrl = 'ScheduleGroupSelection.aspx'

def getUrl(url):
  try:
    result = get(url)
    if result.status_code == 200:
      return result.text
    else:
      return None
  except RequestException as e:
    print(e)
    return None

def postUrl(url, payload):
  try:
    result = post(url, data=payload)
    if result.status_code == 200:
      return result.text
    else:
      return None
  except RequestException as e:
    print(e)
    return None

def getInputFields(soup, group):
  inputFields = {}
  for field in soup.find_all('input'):
    try:
      inputFields[field['name']] = field['value']
    except:
      if field['type'] == 'text':
        inputFields[field['name']] = group
      else:
        inputFields[field['name']] = ''
  return inputFields

def sortDotWeekOut(DotWeek):
  links = DotWeek.find_all('a')#can be empty or contain several links
  DotWeek = {}
  if links:#if at least smth
    DotWeek[links[0]['title']] = links[0]['href'].replace(' ', '_').replace(')', '%29')#P.E. dealt with
    if len(links) > 1:#not P.E.
      for pos in range(len(links)-2):#wil work once for each teacher present, leaving the last link untouched
        DotWeek[links[pos+1]['title']] = 'http://rozklad.kpi.ua' + links[pos+1]['href'].replace(' ', '')#replace just in case
      nums = [True for x in links[len(links)-1].text if x.isdigit()] #if last link has numbers - it is an auditorium, else - another teacher
      if nums: #if last link is an auditorium
        DotWeek[links[len(links)-1].text] = links[len(links)-1]['href'].replace(' ', '')#Auditorium always last
      else:
        DotWeek[links[len(links)-1]['title']] = 'http://rozklad.kpi.ua' + links[len(links)-1]['href'].replace(' ', '')#replace just in case
  return DotWeek

def sortLesTimeOut(lesTime):
  DotWeekList = lesTime.find_all('td')#got list of days - mon-sat for each row(lessonTime)
  del DotWeekList[0]
  DotWeekList = list(map(sortDotWeekOut, DotWeekList))#for each day
  return DotWeekList

def sortTableOut(table):
  table = table.find_all('tr')#got list of rows - 1-5 lesson for each table
  del table[0]
  table = list(map(sortLesTimeOut, table))#for each row
  return table

def getTT(group):
  mainPage = postUrl(defUrl + mainPageUrl, '') #check if None
  soup = BeautifulSoup(mainPage, 'html.parser')
  formDest = defUrl + soup.form['action']
  inputFields = getInputFields(soup, group)
  response = postUrl(formDest, inputFields)
  responseSoup = BeautifulSoup(response, 'html.parser')
  tablesList = responseSoup.find_all('table')#array of two weeks
  tablesList = list(map(sortTableOut, tablesList))#for each week
  tablesList = tablesList[0] + tablesList[1]
  return tablesList


# Subject, Teacher  , Auditorium
# Always , Sometimes, Often(Not on P.E.)
# len = 0 - free day
# len = 1 - P.E.
# len = 2 - No teacher
# len = 3 - One teacher
# len > 3 - Several teachers
# DotWeek = 
# {
#             lessonLink: '',
#             lesson: '',
#             teacherLink: '',
#             teacher: '',
#             classroomLink: '',
#             classroom: '',
#         }


# a = getTT('іп-71')
# print(a)
