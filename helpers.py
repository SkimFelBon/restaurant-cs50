import requests, urllib.parse, json
from flask import request
from models import Language, Product_translation


def translateOrder(cookieKey, pageLang):
    ## This function translates cookie file(Order) to desired language
    # DONE Check id for specific language
    lang_id = Language.query.filter_by(name=pageLang).first()
    ## DONE read cookie
    escapedCookie = request.cookies.get(cookieKey, 0)
    if escapedCookie == 0:
        return 0
    strCookie = urllib.parse.unquote(escapedCookie)
    # DONE convert string to dictionary type
    Order = json.loads(strCookie)
    if len(Order['Pizza']) == 0:
        return 0
    ## FIXED! needed to rework this part of code
    ## !!!! Modifying keys of an array while looping over it is generally a bad idea !!!!
    ## so i first create array of keys
    ## and for every index in array translate Object keys
    keyList = []
    # Create array of keys
    for v in Order['Pizza'].keys():
        keyList.append(v)

    for i in range(len(keyList)):
        lang_ = Product_translation.query.filter_by(name=keyList[i]).first()
        ## DONE If order-language same as document-language skip
        if lang_.language.name == pageLang:
            continue
        oldKey = str(lang_.name)
        ## DONE query database for the same items in page language
        # sql SELECT name FROM product_translation WHERE product_non_trans_id = '5' AND language_id = '2';
        translatedName = Product_translation.query.filter_by(product_non_trans_id = lang_.product_non_trans_id, language_id = lang_id.id).first()
        newKey = str(translatedName.name)
        # DONE translate(swap) keys in Order
        Order['Pizza'][newKey] = Order['Pizza'][oldKey]
        del Order['Pizza'][oldKey]
    ## DONE stringify Order
    stringifiedOrder = json.dumps(Order)
    ## DONE escape Order
    escapedOrder = urllib.parse.quote(stringifiedOrder)
    ## DONE return escaped string Order
    return escapedOrder

#------------TRELLO---------------------
# DONE Add Card
def trelloCard(name, phone, address, order):
    # Contact API
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    TrelloKey = data['myTrello']['TrelloKey']
    TrelloToken = data['myTrello']['TrelloToken']
    #BoardID = data['myTrello']['idBoard']
    ListID = data['myTrello']['idList']
    if address == "self-pickup":
        labels = data['myTrello']['idLabels']['Self_pickup']
    else:
        labels = data['myTrello']['idLabels']['Delivery']
    # Create description for a card
    keyList = []
    orderInfo = ""
    for v in order['Pizza'].keys():
        price = order['Pizza'][v][0]['Price']
        amount = order['Pizza'][v][1]['Amount']
        orderInfo = orderInfo + "**" + v +"**: amount x" + str(amount) + " price: " + str(price) + " UAH \n"
    description = "**Customer info:**\n**Address:** " + str(address) + "\n**Name:** " + str(name) + "\n**Phone:** " + str(phone) + "\n**Order info:**\n" + str(orderInfo)
    try:
        url = "https://api.trello.com/1/cards"
        querystring = {"name":address,
                        "desc":description,
                        "pos":"top",
                        "idList":ListID,
                        "idLabels":labels,
                        "keepFromSource":"all",
                        "key":TrelloKey,
                        "token":TrelloToken
                        }
        response = requests.request("POST", url, params=querystring)
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse response
    try:
        quote = response.json()
        return {
            "idCard":quote['id'],"key":TrelloKey,
        }
    except (KeyError, TypeError, ValueError):
        return None
#-----------------------------
# DONE Add checklist
def trelloChecklist(newCard):
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    TrelloKey = data['myTrello']['TrelloKey']
    TrelloToken = data['myTrello']['TrelloToken']
    try:
        url = "https://api.trello.com/1/checklists"
        querystring = {"idCard":newCard['idCard'],
                        "name":"Order",
                        "pos":"top",
                        "key":TrelloKey,
                        "token":TrelloToken
        }
        response = requests.request("POST", url, params=querystring)
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        quote = response.json()
        return {
            "checkListID": quote['id']
        }
    except (KeyError, TypeError, ValueError):
        return None
#-----------------------------
# DONE Add an item to checklist
def addCheckListItem(pizzaName,newChecklist):
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    TrelloKey = data['myTrello']['TrelloKey']
    TrelloToken = data['myTrello']['TrelloToken']
    checklistID = newChecklist['checkListID']
    try:
        url = "https://api.trello.com/1/checklists/" + checklistID + "/checkItems"
        querystring = {
            "name":pizzaName,
            "pos":"bottom",
            "checked":"false",
            "key":TrelloKey,
            "token":TrelloToken
        }
        response = requests.request("POST", url, params=querystring)
        #response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        quote = response.json()
        return quote
    except (KeyError, TypeError, ValueError):
        return None
