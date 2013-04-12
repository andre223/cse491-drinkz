import db 

   
class Recipe(object):    

    def __init__(self, name, ingredientList):        
	self._ingredients = set()
	self._recipeName = name        
	for ingredient in ingredientList:
	    self._ingredients.add(ingredient)    

    def need_ingredients(self):
	missingList = list()        
	for ingredient in self._ingredients:   #go through current ingredients
	    listOfTuples = db.check_inventory_for_type(ingredient[0])
	    
	    stockAmount = 0            
	    for tuple in listOfTuples:                
		amt = db.get_liquor_amount(tuple[0],tuple[1])                
		if amt>stockAmount:                    
		    stockAmount = amt
	    debtAmount = stockAmount - db.convert_to_ml(ingredient[1])
	    
	    if ( debtAmount < 0 ):
		missingList.append((ingredient[0],debtAmount*-1.))        
	return missingList

    def __eq__(self, other):         
	return self._recipeName == other._recipeName
    
    def get_name(self):
        return self._recipeName

    def get_ingredients(self):
        return self._ingredients
