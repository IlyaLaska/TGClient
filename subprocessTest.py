import subprocess, json

b = {'a':1, 'b':2, 'c':''}
c = b.values()
d = list(c)
print(1)
# a = subprocess.check_output(["node", "net.js"])
# text = a.decode('utf8')
# doc = json.loads(text)
# for k in doc:
#   for d in k:
#     for el, v in d.items():
#       print('[' + el + '](' + v + ')') #check for empty v

# lists = text.split(']')
# del lists[-2:]
# # del lists[-1]
# for i in range(len(lists)):
#   if not i:
#     lists[i] = lists[i][4:]
#   else:
#     lists[i] = lists[i][6:]
#   lists[i] = lists[i].split('}')
#   for k in lists[i]:
#     print(k)
#     print('=================================================')
#   print('-----------------------------------------------------------------------------------------------')

# print(len(lists))


