# def fun(n):
#   return n ** n
# # print(fun(20))

# def function(a, b):
#   for i in range(10):
#     print(i);
#     num = a or b and b or not a
#   return num

# func = lambda a: a+1

# # print(func(5), func(1), sep='       ', end='')
# # print('111wewewewe111'.strip(chars='1'))

# for i, stri in enumerate([5,6,7]):
#   print(stri)
# if('5' in '567'): print('asda')
# dic = {'f': 1}
# if dic.__contains__('f'): print('1111')
# # help(str)

# def diamond(height):
#     print(height)
#     str = []
#     k = 1
#     while k <= height:
#         for i in range(height-k):
#             str.append(' ')
#         for i in range(k):
#             str.append('/')
#         for i in range(k):
#             str.append('\\')
#         str.append('\n')
#         k +=1
#     k-=1
#     while height > 0:
#         for i in range(k-height):
#             str.append(' ')
#         for i in range(height):
#             str.append('\\')
#         for i in range(height):
#             str.append('/')
#         str.append('\n')
#         height -=1
# #     print(str)
#     ret = ''.join(str)
#     print(ret)
# def diamond2(height):
#     s = ''
#     # The characters currently being used to build the left and right half of 
#     # the diamond, respectively. (We need to escape the backslash with another
#     # backslash so Python knows we mean a literal "\" character.)
#     l, r = '/', '\\'
#     # The "radius" of the diamond (used in lots of calculations)
#     rad = height // 2
#     for row in range(height):
#         # The first time we pass the halfway mark, swap the left and right characters
#         if row == rad:
#             l, r = r, l
#         if row < rad:
#             # For the first row, use one left character and one right. For
#             # the second row, use two of each, and so on...
#             nchars = row+1
#         else:
#             # Until we go past the midpoint. Then we start counting back down to 1.
#             nchars = height - row
#         left = (l * nchars).rjust(rad)
#         right = (r * nchars).ljust(rad)
#         s += left + right + '\n'
#     # Trim the last newline - we want every line to end with a newline character
#     # *except* the last
#     return s[:-1]
# # diamond(11)

# import math

# pi = "pi to 10: {:.20}".format(math.pi)
# print(pi)
# help(print)


# import ast
# import random


# # Either a single item or a list of them will work for the chats.
# # You can also use the IDs, Peers, or even User/Chat/Channel objects.
# @client.on(events.NewMessage(chats=('TelethonChat', 'TelethonOffTopic')))
# async def normal_handler(event):
#     if 'roll' in event.raw_text:
#         await event.reply(str(random.randint(1, 6)))


# # Similarly, you can use incoming=True for messages that you receive
# @client.on(events.NewMessage(chats='TelethonOffTopic', outgoing=True,
#                              pattern='eval (.+)'))
# async def admin_handler(event):
#     expression = event.pattern_match.group(1)
#     await event.reply(str(ast.literal_eval(expression)))

# aa = {'a': ('qwe', 2), 'b': 'DD\nDD'}

# print(type(aa['a']))
# print(str('a\na'))

# def stringifyDict(dic):
#   print('cl')
#   res = ''
#   for key, value in dic.items():
#     res += (key + ': ' + value + '\n')
#   print(res)
#   return res

# stringifyDict({'a': 'asas', 'b': 'qweqweq'})

# les = les-5 if les >= 5 else les
# a = [1, 2]
# for i in range(len(a)-2):
#   print('aaaaa')

# a = {'a': 1, 'b':2, 'c': 3}

# b = a.items()
# # print(list(b))
# c = []
# [c.extend([k,v]) for k,v in a.items()]
# print(c)

# a = 'qweqwe'
# b = [True for x in a if x.isdigit()]
# if b:
#   print(b)


# import telethon

# print(repr(telethon.client.telegrambaseclient.TelegramBaseClient))

print(1)
