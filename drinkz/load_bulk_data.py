"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package


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

    try:
	for mfg, name, typ in reader:
	    n += 1
	    db.add_bottle_type(mfg, name, typ)
    except ValueError:
	print "Incorrect line format."
	pass
    
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


def csv_reader(fp):
    """
    This is a generator function that takes in a csv.
    Ignores comments (lines that start with #) and blank lines. 

    Takes a file pointer.

    Yields a list from the parsed csv line. 
    """

    reader = csv.reader(fp)
     
    for line in reader:
        if line[0].startswith('#') or len(line) == 0: #if not line[0].strip():
	    continue 

   	yield line










