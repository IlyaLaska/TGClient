#DONE: i need to add @ to sender names in missedMsgs in sleepWarner
#TODO: why stoppropagation is not working?
#TODO: what if rozklad crashes? - handle in js send error, catch in py and send notification
#TODO: handle promise rejections in js
#DONE: finish /tt
#DONE: URGENT - deal with incorrect group input
#DONE: what if there is no teacher?

import os
import asyncio, subprocess, json, scraper
from telethon import TelegramClient, sync, events

sleeping = False
silent = False
missedMsgs = {}

client = TelegramClient('ilaska', os.environ['api_id'], os.environ['api_hash'])

def stringifyDict(dic):
  res = ''
  for key, value in dic.items():
    res += (str(key) + ':\n' + value + '\n')
  return res

async def messageKiller(msg, timer):
  await asyncio.sleep(timer)
  await msg.delete()

async def sendJSTT(e, group, sendTo):
  res = subprocess.check_output(["node", "net.js", group])
  print('Got reply from JS')
  jsonText = res.decode('utf8')
  globalList = json.loads(jsonText)
  if globalList:
    asyncio.create_task(client.send_message(sendTo, '**Timetable for ' + group + ':**'))
  else:
    asyncio.create_task(client.send_message(sendTo, 'failed to get timetable for group ' + group + '. Please check your input'))
  asyncio.create_task(e.message.delete())
  print('Got doc')
  dayOTWeek = 0
  days = ['**Monday:**\n', '**Tuesday:**\n', '**Wednesday:**\n', '**Thursday:**\n', '**Friday:**\n', '**Saturday:**\n']
  week = ['', '', '', '', '', '']
  week2 = []
  week1TT = '**WEEK 1:**\n'
  week2TT = '**WEEK 2:**\n'
  for lisI in range(len(globalList)):
    # print(globalList[0])
    if lisI == 5:
      # print('LISTS SWAP')
      # print(week)
      week2  = week.copy()
      # print(week2)
      week = ['', '', '', '', '', '']
    for lesssonDict in globalList[lisI]:
      if dayOTWeek == 6:
        dayOTWeek = 0
      # print(lesssonDict)
      lesson = ''
      lessonValues = list(lesssonDict.values())
      # print(lessonValues)
      for i in range(len(lessonValues)): #link first
        # print(i)
        if (i % 2): #remainder == 1 - useful lessonValues
          # print('remainder')
          if lessonValues[i-1]: #link exists
            # print('I: ')
            # print(i)
            lesson += ('[' + lessonValues[i] + '](' + lessonValues[i-1] + ')\n')
          elif lessonValues[i]:
            # print('elif')
            # print(lessonValues[i])
            lesson += (lessonValues[i] + '\n')
      #     print('end of remainder')
      #   print('lesson so far')
      #   print(lesson)
      # print('lesson:')
      # print(lesson)
      if lesson:
        # week[dayOTWeek] += lesson
        les = lisI-5 if lisI >= 5 else lisI
        week[dayOTWeek] += '**' + str(les+1) + ':**  ' + lesson
      dayOTWeek += 1
  
  for i in range(len(days)):
    week1TT += days[i]
    week1TT += week2[i]
  
  for i in range(len(days)):
    week2TT += days[i]
    week2TT += week[i]
  await client.send_message(sendTo, week1TT, link_preview=False)
  await client.send_message(sendTo, week2TT, link_preview=False)
  print('end of tt')

async def sendTT(e, group, sendTo):
  # res = subprocess.check_output(["node", "net.js", group])
  # print('Got reply from JS')
  # jsonText = res.decode('utf8')
  # globalList = json.loads(jsonText)
  globalList = scraper.getTT(group)
  if globalList:
    asyncio.create_task(client.send_message(sendTo, '**Timetable for ' + group + ':**'))
  else:
    asyncio.create_task(client.send_message(sendTo, 'failed to get timetable for group ' + group + '. Please check your input'))
  asyncio.create_task(e.message.delete())
  print('Got doc')
  dayOTWeek = 0
  days = ['**Monday:**\n', '**Tuesday:**\n', '**Wednesday:**\n', '**Thursday:**\n', '**Friday:**\n', '**Saturday:**\n']
  week = ['', '', '', '', '', '']
  week2 = []
  week1TT = '**WEEK 1:**\n'
  week2TT = '**WEEK 2:**\n'
  for lisI in range(len(globalList)):
    # print(globalList[0])
    if lisI == 5:
      # print('LISTS SWAP')
      # print(week)
      week2  = week.copy()
      # print(week2)
      week = ['', '', '', '', '', '']
    for lesssonDict in globalList[lisI]:
      if dayOTWeek == 6:
        dayOTWeek = 0
      # print(lesssonDict)
      lesson = ''
      lessonValues = []
      [lessonValues.extend([k,v]) for (k, v) in lesssonDict.items()]
      for i in range(len(lessonValues)):
        if not (i % 2):#0, 2, 4...
          lesson += ('[' + lessonValues[i] + '](' + lessonValues[i+1] + ')\n')

                                # lessonValues = list(lesssonDict.values())
                                # # print(lessonValues)
                                # for i in range(len(lessonValues)): #link first
                                #   # print(i)
                                #   if (i % 2): #remainder == 1 - useful lessonValues
                                #     # print('remainder')
                                #     if lessonValues[i-1]: #link exists
                                #       # print('I: ')
                                #       # print(i)
                                #       lesson += ('[' + lessonValues[i] + '](' + lessonValues[i-1] + ')\n')
                                #     elif lessonValues[i]:
                                #       # print('elif')
                                #       # print(lessonValues[i])
                                #       lesson += (lessonValues[i] + '\n')
      #     print('end of remainder')
      #   print('lesson so far')
      #   print(lesson)
      # print('lesson:')
      # print(lesson)
      if lesson:
        # week[dayOTWeek] += lesson
        les = lisI-5 if lisI >= 5 else lisI
        week[dayOTWeek] += '**' + str(les+1) + ':**  ' + lesson
      dayOTWeek += 1
  
  for i in range(len(days)):
    week1TT += days[i]
    week1TT += week2[i]
  
  for i in range(len(days)):
    week2TT += days[i]
    week2TT += week[i]
  await client.send_message(sendTo, week1TT, link_preview=False)
  await client.send_message(sendTo, week2TT, link_preview=False)
  print('end of tt')

async def main():
  # await client.start()
  await client.connect()
  if not (await client.is_user_authorized()):
    await client.send_code_request(os.environ['phone_number']) #should i wrap with func and then await???
    myself = await client.sign_in(os.environ['phone_number'], client.get_messages('Telegram')[0].message[12:17])
  await client.run_until_disconnected()
  # msgs = client.get_messages('Telegram')

@client.on(events.NewMessage(outgoing=True, pattern='Die'))
async def killer(event):
  notification = await event.reply('Dying!')
  # await notification.delete()
  # await e.message.delete()
  client.disconnect()

@client.on(events.NewMessage(outgoing=True, pattern='/sleep'))
async def sleepOn(e):
  global sleeping
  sleeping = True
  global missedMsgs
  missedMsgs = {}
  asyncio.create_task(e.message.delete())
  notification = await client.send_message(e.from_id, 'Sleep mode active')
  asyncio.create_task(messageKiller(notification, 5))

@client.on(events.NewMessage(outgoing=True, pattern='/wake'))
async def sleepOff(e):
  asyncio.create_task(e.message.delete())
  global sleeping
  sleeping = False
  notification = await client.send_message(e.from_id, 'Sleep mode deactivated')
  if missedMsgs:
    mailNotification = await client.send_message('me', 'You have mail!')
  await client.send_message('me', stringifyDict(missedMsgs))
  asyncio.create_task(messageKiller(notification, 5))
  asyncio.create_task(messageKiller(mailNotification, 6))

@client.on(events.NewMessage(func=lambda e: sleeping, from_users=(os.environ['users']))) #--------------------
async def sleepWarner(e):
  notification = await asyncio.create_task(client.send_message(e.from_id, 'I am currently asleep, please contact me later'))
  sender = (await client.get_entity(e.from_id)).username
  if sender: #sender has username
    sender = '@' + sender
    if sender in missedMsgs: #not the first message from sender
      missedMsgs[sender] += '\n' + e.message.message
    else: #the first message from sender
      missedMsgs[sender] = e.message.message
  else: #sender has no username
    ent = await client.get_entity(e.from_id)
    # print(e)
    name = ent.first_name + ' ' + ent.last_name
    if name in missedMsgs: #not the first message from sender
      missedMsgs[name] += ('\n' + e.message.message)
    else: #the first message from sender
      missedMsgs[name] = e.message.message
  asyncio.create_task(messageKiller(notification, 60))

@client.on(events.NewMessage(outgoing=True, pattern='/shut'))
async def silencerSwitch(e):
  await client.delete_messages(None, e.message.id)
  global silent
  # print('sSwStart', silent)
  if silent: #silent on - need to turn off
    silent = False
  else: #silent off - need to turn on
    silent = True
  # print('sSwEnd', silent)
  # await e.silencerSwitch();
  # raise StopPropagation

@client.on(events.NewMessage(func=lambda e: silent, from_users=(os.environ['users']))) #--------------------
async def silencer(e):
  # print('sStart', silent)
  asyncio.create_task(e.message.delete())
  msg = await client.send_message(e.from_id, 'Zip it!')
  asyncio.create_task(messageKiller(msg, 5))
  # print('sEnd', silent)

@client.on(events.NewMessage(outgoing=True, pattern='/(yell|крик).*'))# yell as your new message
async def yeller(e):
  asyncio.create_task(client.edit_message(e.message, e.message.message[5:].upper()))

@client.on(events.NewMessage(outgoing=True, pattern='/(yell|крик) {0,1}$'))
async def yellerAsReply(e):
  asyncio.create_task(client.delete_messages(None, e.message.id))
  if e.message.message and e.message.reply_to_msg_id: #sent as reply command - else thought to be sent by mistake and cleaned
    msg = await client.get_messages(None, ids=e.message.reply_to_msg_id)
    asyncio.create_task(client.edit_message(msg, msg.message.upper()))

@client.on(events.NewMessage(outgoing=True, pattern='/(bold|жирн).*'))
async def bolder(e):
  await client.edit_message(e.message,'**' + e.message.message[5:] + '**')

@client.on(events.NewMessage(outgoing=True, pattern='/(bold|жирн) {0,1}$'))
async def bolderAsReply(e):
  asyncio.create_task(client.delete_messages(None, e.message.id))
  if e.message.message and e.message.reply_to_msg_id: #sent as reply command - else thought to be sent by mistake and cleaned
    msg = await client.get_messages(None, ids=e.message.reply_to_msg_id)
    asyncio.create_task(client.edit_message(msg, '**' + msg.message + '**'))

@client.on(events.NewMessage(outgoing=True, pattern='/(ital|курс).*'))
async def italiciser(e):
  await client.edit_message(e.message,'__' + e.message.message[5:] + '__')

@client.on(events.NewMessage(outgoing=True, pattern='/(ital|курс) {0,1}$'))
async def italiciserAsReply(e):
  asyncio.create_task(client.delete_messages(None, e.message.id))
  if e.message.message and e.message.reply_to_msg_id: #sent as reply command - else thought to be sent by mistake and cleaned
    msg = await client.get_messages(None, ids=e.message.reply_to_msg_id)
    asyncio.create_task(client.edit_message(msg, '__' + msg.message + '__'))

@client.on(events.NewMessage(pattern='/(tt|рр) ?$'))
async def timeTableSender(e):
  sendTo = 0
  if e.chat_id:
    sendTo = e.chat_id
  else:
    sendTo = e.from_id
  msg = await client.send_message(sendTo, 'Sending timetable for ІП-71...')
  asyncio.create_task(sendTT(e, 'іп-71', sendTo))
  # asyncio.create_task(client.edit_message(msg, '**Timetable for ІП-71:**'))
  asyncio.create_task(messageKiller(msg, 4))

@client.on(events.NewMessage(pattern='/(tt|рр) \w{2}-\d{2}$'))
async def timeTableSenderGroup(e):
  sendTo = 0
  if e.chat_id:
    sendTo = e.chat_id
  else:
    sendTo = e.from_id
  group = e.message.message[4:]
  msg = await client.send_message(sendTo, 'Sending timetable for ' + group + '...')
  asyncio.create_task(sendTT(e, group, sendTo))
  # asyncio.create_task(client.edit_message(msg, '**Timetable for ' + group + ':**'))
  asyncio.create_task(messageKiller(msg, 4))


# with client:
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
  # client.start()
# client.connect()
# if not client.is_user_authorized():
#   client.send_code_request(os.environ['phone_number']) #should i wrap with func and then await???
#   myself = client.sign_in(os.environ['phone_number'], client.get_messages('Telegram')[0].message[12:17])
# # msgs = client.get_messages('Telegram')
# print(msgs[0].message[12:17])
  # startup()
  # client.run_until_disconnected()

# try:
#   client.connect()
#   if not client.is_user_authorized():
#     client.send_code_request(os.environ['phone_number'])
#     myself = client.sign_in(os.environ['phone_number'], input('Enter code: '))

#   # AS = client.get_entity('')
#   # print(AS)
#   # chats10 = client.get_dialogs(limit=10)
#   # for chat in chats10:
#     # print(chat)
#     # print(type(chat))
#     # if chat.name = 'A' : print('FOUND')


#   # me = client.get_me()
#   # print(me.stringify())



# client.run_until_disconnected()

# finally:
#   print('Done')
#   client.disconnect()
