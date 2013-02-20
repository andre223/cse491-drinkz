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
	    print listOfTuples            
	    
	    stockAmount = 0            
	    
	    for tuple in listOfTuples:                
		amt = db.get_liquor_amount(tuple[0],tuple[1])                
		if amt>stockAmount:                    
		    stockAmount = amt
	    deptAmount = stockAmount - self.convert_to_ml(ingredient[1])
	    
	    if ( deptAmount < 0 ):
		missingList.append((ingredient[0],deptAmount*-1.))        
	return missingList

    def convert_to_ml(self,amount):        
	amounts = amount.split(" ")        
	total = 0        
	if amounts[1] == "oz":            
	    total += float(amounts[0])*29.5735
	elif amounts[1] == "ml":            
	    total += float(amounts[0])        
	elif amounts[1] == "liter":            
            total += float(amounts[0])*1000.0        
	elif amounts[1] == "gallon":            
	    total += float(amounts[0])*3785.41178
	return total        

	return aSet    

    def __eq__(self, other):         
	return self._recipeName == other._recipeName                    
