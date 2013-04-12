"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#
import csv                              # Python csv package

import pprint
from . import db                        # import from local package
from . import recipes


def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = csv_reader(fp)

    x = []
    n = 0

    for line in reader:
        if(len(line) != 3):
            continue
        try:
            (mfg, name, typ) = line
        except:
            print "Incorrect line format"
        
        n += 1
        try:
            db.add_bottle_type(mfg, name, typ)
        except:
            print "Failed to add to inventory"
            
    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = csv_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:
	    (mfg, name, amount) = line;
	except:
	    print "Incorrect Line format"

        n += 1

	try:
	    db.add_to_inventory(mfg, name, amount)
	except:
	    print "Failed to add to the inventory"
            
    return n

# HW 5
def load_recipes(fp):
    '''
    Load in recipe data
    '''
    reader = csv_reader(fp)
    n = 0
    for line in reader:
        name = line[0]
        ings = line[1:]

        myIngSet = set()
        i = 0
        while(i < len(ings)):
            val = (ingred,amount) = (ings[i],ings[i+1])
            myIngSet.add(val)
            i+=2

        r = recipes.Recipe(name,myIngSet)
        try:
            db.add_recipe(r)
            n+=1
        except:
            print "Could not add to inventory"

    return n


def csv_reader(fp):
    """
    This is a generator function that takes in a csv.
    Ignores comments (lines that start with #) and blank lines. 

    Takes a file pointer.

    Yields a list from the parsed csv line. 
    """

    reader = csv.reader(fp)
     
    for line in reader:
        if not line:
	    continue
	if not line[0].strip():
 	    continue
        if line[0].startswith('#'):
	    continue 

   	yield line










