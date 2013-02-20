"""
Database functionality for drinkz information.
"""

import drinkz.recipes

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()	#HW3 1
    _inventory_db = {}		#HW3 1
    _recipes_db = set()		#HW3 Part3

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass

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

    if (mfg, liquor) in _inventory_db:        
	_inventory_db[(mfg, liquor)] += amountTotal    
    else:        
	_inventory_db[(mfg, liquor)] = amountTotal


def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True

    return False

''' Changed/Added by NIK ANDREWS'''
def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    
    amounts = [] 
    total = 0
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
	    total = float(str(_inventory_db[(m,l)]))

    return float("%.2f" % total)

''' END Changes/Additions made '''

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    
    for (m, l) in _inventory_db:
        yield m, l
    
'''HW3 PART3'''
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

