"""
Database functionality for drinkz information.
"""
import os
#from cPickle import dump, load
import cPickle
import recipes
import sqlite3
import base64

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

_partylist_db = set()
_hostneeds_list_db = {}

#Rating 1,2,3 counter
_one_counter = 0
_two_counter = 0
_three_counter = 0

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db, _partylist_db, _hostneeds_list_db, _one_counter, _two_counter, _three_counter
    _bottle_types_db = set()	
    _inventory_db = {}		
    _recipes_db = set()		
    _partylist_db = set()
    _hostneeds_list_db = {}
    _one_counter = _two_counter = _three_counter = 0

    conn = sqlite3.connect('myDatabase')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS bottletypes''')
    c.execute('''DROP TABLE IF EXISTS inventory''')
    c.execute('''DROP TABLE IF EXISTS recipes''')
    c.execute('''DROP TABLE IF EXISTS party''')
    c.execute('''DROP TABLE IF EXISTS hostneeds''')
 
    conn.commit()
    conn.close()


# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass

#SAVE to a file
def save_db(filename):
    '''
    fp = open(filename, 'wb')

    toSave = (_bottle_types_db, _inventory_db, _recipes_db, _partylist_db, _hostneeds_list_db)
    dump(toSave, fp)

    fp.close()
    '''
    
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('''CREATE TABLE bottletypes(mfg TEXT, liquor TEXT, type TEXT)''')
    c.execute('''CREATE TABLE inventory(mfg TEXT, liquor TEXT, amount TEXT)''')
    c.execute('''CREATE TABLE recipes(recipe TEXT)''')
    c.execute('''CREATE TABLE party(item TEXT)''')
    c.execute('''CREATE TABLE hostneeds(num TEXT, item TEXT)''')
 
    for i in _bottle_types_db:
	c.execute("INSERT INTO bottletypes (mfg,liquor,type) VALUES (?,?,?)",i)
  
    for i in _inventory_db:
	(m,l) = i
	amt = _inventory_db[i]
    	c.execute("INSERT INTO inventory (mfg,liquor,amount) VALUES (?,?,?)",(m,l,amt))

    for i in _recipes_db:
	s = cPickle.dumps(i)
	c.execute("INSERT INTO recipes (recipe) VALUES (?)",[sqlite3.Binary(s)])
    
    for i in _partylist_db:
        s = cPickle.dumps(i)
	c.execute("INSERT INTO party (item) VALUES (?)", [sqlite3.Binary(s)])

    for (item_no,item) in _hostneeds_list_db.items():
	#item_no = i
	#item = _hostneeds_list_db[item_no]
	c.execute("INSERT INTO hostneeds (num,item) VALUES (?,?)",(item_no,item))

    conn.commit()
    conn.close()


#LOAD from a file
def load_db(filename):
    '''
    global _bottle_types_db, _inventory_db, _recipes_db, _partylist_db, _hostneeds_list_db
   
    fp = open(filename, 'rb')
    loaded = load(fp)

    (_bottle_types_db, _inventory_db, _recipes_db, _partylist_db, _hostneeds_list_db) = loaded

    fp.close()
    '''

    con = sqlite3.connect(filename)
    c = con.cursor()

    c.execute('SELECT * FROM bottletypes')
    results = c.fetchall()
    for (mfg,liquor,type) in results:
	add_bottle_type(mfg,liquor,type)

    c.execute('SELECT * FROM inventory')
    results = c.fetchall() 
    for (mfg,liquor,amount) in results:
	add_to_inventory(mfg,liquor,amount+' ml')
 
    for item in c.execute("SELECT * FROM party"):
	add_to_partylist(cPickle.loads(str(item[0])))

    c.execute('SELECT * FROM hostneeds')
    results = c.fetchall()
    for (x,item) in results:
	add_to_hostneeds(x,item)
    
    for r in c.execute("SELECT * FROM recipes"):
	add_recipe(cPickle.loads(str(r[0])))

    c.close()


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ)) 	#HW3 1

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."

    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    total = convert_to_ml(amount)
 
    if (mfg, liquor) in _inventory_db:        
	_inventory_db[(mfg, liquor)] += total    
    else:        
	_inventory_db[(mfg, liquor)] = total

#HW4 Part 1 (unit convertion)
def convert_to_ml(amount):
    amounts = amount.split(" ")
    amountTotal = 0.0

    if amounts[1] == "ml":        
	amountTotal += float(amounts[0])    
    elif amounts[1] == "oz":        
	amountTotal += float(amounts[0]) * 29.5735
    elif amounts[1] == "gallon":        
	amountTotal += float(amounts[0]) * 3785.4118    
    elif amounts[1] == "liter":
	amountTotal += float(amounts[0])*1000.0
    
    return amountTotal

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = [] 
    total = 0
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
	    total = float(str(_inventory_db[(m,l)]))
    return float("%.2f" % total)


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l

def get_liquor_types():
    "Retrieve all liquor types, in the form: (mfg, liquor)."
    for (m,l,_) in _bottle_types_db:
        yield m,l
        
def add_recipe(r):
    for recipe in _recipes_db:        
	if recipe._recipeName == r._recipeName:            
	    raise DuplicateRecipeName
    _recipes_db.add(r)    

def get_recipe(name):    
    for recipe in _recipes_db:        
	if name == recipe._recipeName:         
	    return recipe    
    return 0

def get_all_recipes():    
    return _recipes_db

def check_inventory_for_type(type):
    aList = list()       
    for (m, l, t) in _bottle_types_db:        
	if(type == t or type == l): #checks for generic or label            
	    aList.append((m,l))    
    return aList

#HW 6.2 Party Page stuff

def add_to_partylist(listItem):
    _partylist_db.add(listItem)

def get_all_partylist():
    return _partylist_db



#HW 6.2 Host Needs Page stuff

def add_to_hostneeds(item_no, listItem):
    _hostneeds_list_db[item_no] = listItem 

def check_hostneeds_list(item_no):
    for (i,item) in _hostneeds_list_db.items():
        if i == item_no:
            return True
    return False


def get_hostneeds_item(item_no):
    for (i,item) in _hostneeds_list_db.items():
	if i == item_no:
	    return item

def delete_hostneeds_item(item_no):
   for (i,item) in _hostneeds_list_db.items():
       	if i == item_no:
	    del _hostneeds_list_db[i]

def get_all_hostneeds_list():
   return _hostneeds_list_db.items()
	
#HW 6.2 Rating stuff

def add_rating(rating):
    global _one_counter, _two_counter, _three_counter
    if rating == "1":
	print rating
	_one_counter += 1
    elif rating == "2":
	_two_counter += 1
    elif rating == "3":
	_three_counter += 1
    
def get_num_of_one_ratings():
    return _one_counter

def get_num_of_two_ratings():
    return _two_counter

def get_num_of_three_ratings():
    return _three_counter


