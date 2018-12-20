# import time,datetime
# # now = time.time()
# # print( now )
# # timeArray = time.localtime(now)
# # print( timeArray)
# # otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
# # print(otherStyleTime)
# print(datetime.datetime.t)


import requests,time
# url = 'http://127.0.0.1:5000/map/123'
# ADDdata = {
# 	'f' : 0,
# 	'add' : 1,
# 	'timestamp': time.time()
# }

# postdata = {
# 	'f' : 0,
# 	'add' : 0,
# 	'longitude' : '118.1221',
# 	'latitude' :  '32.3242'
# }
# html = requests.post(url,data=postdata)
# print(html.text)
# headers = {
# 	"Content-Type":"multipart/form-data"
# }
url = 'http://127.0.0.1:5000/photo/'
# data = {
# 	'name' : 'src',
# 	'filename':"C:\\Users\\10630\\Desktop\\为什么电流被一分为2.jpg"
# } 
data= None
filename = {
	'src' : open("C:\\Users\\10630\\Desktop\\为什么电流被一分为2.jpg",'rb')
}
# html = requests.post(url,data=data,files=filename)
html = requests.post(url,files=filename)

# html = requests.post(url,data=data)
print(html.text)
# t = 1545230000
# import time,datetime
# print( type(time.time()))
# print( time.strftime("%Y--%m--%d %H:%M:%S",time.localtime(t)))
# a = "2018--12--19 22:33:20"
# t = time.strptime(a,"%Y--%m--%d %H:%M:%S")
# print( time.mktime(t))

# html = requests.get('http://127.0.0.1:5000/')
# print(html.text)