from GenerateData import *
from MongoDB import *
import requests
import json
from DiscordIntegration import *


'''
-> Runs once a day
Create Order:
    - get Stock : Done
    - palce orders for Stock : Done
    - get Sales Data
    - get in Production
    - calculate
    - place Order {Mushroom, recipy, amount, date}
'''


def mainCreateOrder(client, collections, url):
    stock = getStockOfAll(client, collections, url)
    sales = getSalesInfo(client)
    inProduction = getInProduction(client)
    print("Starting App...")


def getStockOfAll(client, collections, url):
    stock = []
    for collectionName in collections:
        allProducts = getData(client, 'Stock', collectionName)
        for product in allProducts:
            stock.append(getStockSize(product))
    return stock

def getStockSize(product, url):
    #check if stock is below 15%
    if claculatePercentage(product['stock'], product['stockMax']) < 15:
        sendDiscordMessage(f"Ordering more of {product['name']} because stock is below 15%. Get it from {product['dealer']}.", url)
        return {product['name']: product['stock']}       
    else:
        return {product['name']: product['stock']}       

def claculatePercentage(stock, stockMax):
    return stock / stockMax * 100
    
def getSalesInfo(client):
    allSales = getData(client, 'Sales', 'lastWeekSales')
    for sale in allSales:
        return sale

def getInProduction(client):
    allProduction = getData(client, 'Production', 'inProduction')
    for production in allProduction:
        return production