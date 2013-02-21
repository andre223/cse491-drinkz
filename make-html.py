#! /usr/bin/env python

import os
import drinkz.db
import drinkz.recipes


try:
    os.mkdir('html')
except OSError:
    pass


drinkz.db._reset_db()

drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

drinkz.db.add_bottle_type('Charles Heidsieck', 'champagne', 'champagne')
drinkz.db.add_to_inventory('Charles Heidsieck', 'champagne', '5 liter')

drinkz.db.add_bottle_type('Crystal Palace', 'vodka', 'unflavored vodka')
drinkz.db.add_to_inventory('Crystal Palace', 'vodka', '1 liter')

drinkz.db.add_bottle_type('Jack Daniel\'s', 'whiskey', 'whiskey')
drinkz.db.add_to_inventory('Jack Daniel\'s', 'whiskey', '16 oz')

r = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
drinkz.db.add_recipe(r)

r = drinkz.recipes.Recipe('ultimate margarita', [('white tequila','2 oz'),('lemon and lime juice','1 oz'),('syrup','1 oz')])
drinkz.db.add_recipe(r)

r = drinkz.recipes.Recipe('kunamatata', [('vodka', '1 oz'),('rasberry liqueur','1 oz'),('dark rum','1 oz'),('orange juice','2 oz'),('7-Up Soda','2 oz')])
drinkz.db.add_recipe(r)

###
fp = open('html/index.html', 'w')
print >>fp, "<p><a href='recipes.html'>RECIPES</a><p><a href='inventory.html'>INVENTORY</a><p><a href='liquor_types.html'>LIQUOR TYPES</a>"

fp.close()

###
fp = open('html/recipes.html', 'w')

recipeList = drinkz.db.get_all_recipes()
print >> fp,"<ul>"

for recipe in recipeList:
    if recipe.need_ingredients():
	val = "  NOOOOOOO"
    else:
	val = "  OOOHHHH YYEAAAHHHH!!"
    print >> fp, "<li>" + recipe._recipeName + " " + val + "<p>"

print >> fp, "</ul>"
print >>fp, "<a href='index.html'>HOME</a><p><a href='inventory.html'>INVENTORY</a> <p><a href='liquor_types.html'>Liquor Types</a>"

fp.close()

###
fp = open('html/inventory.html', 'w')

print >>fp,"<ul>"

for (m,l) in drinkz.db.get_liquor_inventory():
    print >> fp, "<li>" + str(m) + " " + str(l) + " " + str(drinkz.db.get_liquor_amount(m,l)) + " ml"+ "<p>"
print >> fp, "</ul>"

print >>fp, "<a href='index.html'>HOME</a><p><a href='recipes.html'>RECIPES</a><p><a href='liquor_types.html'>Liquor Types</a>"

fp.close()

###
fp = open('html/liquor_types.html', 'w')

print >>fp,"<ul>"

for (m,l) in drinkz.db.get_liquor_inventory():
    print >> fp, "<li>" + str(m) + " " + str(l) +"<p>"
print >> fp, "</ul>"

print >>fp, "<a href='index.html'>HOME</a><p><a href='recipes.html'>RECIPES</a><p><a href='inventory.html'>Inventory</a>"

fp.close()






