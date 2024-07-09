'''
This code is teh whole brain of teh script. It first checks teh system with tahe data from home assistant, checks the stock and the data. It weill be supported with teh use of OpenAis Chat GPT-4o and will control a robot arm.
'''
from GenerateData import *
from MongoDB import *
from CreateOrders import *
from SystemViewer import *
import configparser
import openai



if __name__ == "__main__":

    #Get all KEys and Tokens
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgM = config['MONGODB']
    cfgD = config['DISCORD']
    openai.api_key = config['OPENAI']['chat_gpt_key']
 
    client = connectToDB(cfgM['username'], cfgM['password'])
   
   
   
   
   
   
   
    #uploadData(client, 'Testing', "generalInfo", allIndoorData)


#collections = ['mushrooms', 'substrate', 'culture']
#getStockOfAll(client, collections, cfgD['webhook_url'])


#datas = [{'substrate': 'Yeast', 'stock': 100, 'stockMax': 2000}, {'substarte': 'Woode', 'stock': 100, 'stockMax': 2000}, {'substrate': 'Malt', 'stock': 100, 'stockMax': 2000}]

#for data in datas:
#    updateStock(data, client, 'substrate')





'''
-> Runs once a day
Create Order:
    - get Stock
    - palce orders for Stock
    - get Sales Data
    - get in Production
    - calculate
    - place Order {Mushroom, recipy, amount, date}

-> Runs every day
Check Order:
    - check Stock
    - check Systems/Production
    - start Production
    1. 


Sales:
- Sales analyzis

Stock:
- Mushrooms
- Substrate
- Culture


In growth:
{mushroomType: mushroom_type, plantDate: date, id: id}


Production plan:

'''



'''
1. Check stock
2. Check Production

'''

