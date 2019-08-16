# importing the requests library 
import requests 
  
# defining the api-endpoint  
API_ENDPOINT = "http://127.0.0.1:5000/booking"

  
# data to be sent to api 
data = {'param':'panji'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, json = data) 
  
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 