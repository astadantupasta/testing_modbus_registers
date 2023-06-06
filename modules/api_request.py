import requests
import jwt
import os
import array

def getJwtToken(ip,username,password):
    url = "http://{}/api/login".format(ip)
    header = {"user":"admin","password":"Admin123"}
    response = requests.post(url, json={"username":username,"password":password})
    return response
    
def sendAPI(URL,response):
   
    auth= response.json()  
    print(auth["jwtToken"])
    headers = {'Authorization': "Bearer {}".format(auth["jwtToken"])}
    rezults = requests.get(URL,headers=headers)
    results = rezults.json()
    print(results['data']['static']['fw_version'])

def request():
    response = getJwtToken("192.168.1.1","admin","Admin123")
    sendAPI("http://192.168.1.1/api/system/device/info",response)
    n = array.array('i',[1,2,3])
    print(type(n))
request()