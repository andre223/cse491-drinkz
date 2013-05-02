#! /usr/bin/env python
from wsgiref.simple_server import make_server
from db import save_db, load_db
from Cookie import SimpleCookie

import sys
import urlparse
import simplejson
import db
import recipes
import os.path
import fileinput
import jinja2
import unicodedata
import sys
import socket
import uuid
import random

usernames = {}

dispatch = {
    '/' : 'login1',
    '/index' : 'index',
    '/recipesList' : 'recipesList',
    '/inventoryList' : 'inventoryList',
    '/liquorTypes' : 'liquorTypes',
    '/partyPage' : 'partyPage',
    '/hostneedsPage' : 'hostneedsPage',
    '/rating' : 'rating',
    '/convertToML' : 'formConvertToML',
    '/recvAmount' : 'recvAmount',
    '/recv_wsgiserver' : 'recv_wsgiserver',
    '/addType' : 'addType',
    '/addInventory' : 'addInventory',
    '/addRecipe' : 'addRecipe',
    '/addHostNeedsItem' : 'addHostNeedsItem',
    '/addRating' : 'addRating',
    '/rpc'  : 'dispatch_rpc',
    '/error' : 'error',
    '/wsgi_server' : 'wsgi_server',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/status' : 'status'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
	name1 = ''
	name1_key = '*empty'
	if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1=='':
            return self.login1(environ,start_response) 

        data = """\

<html>
<head>
<title>HOME</title>
<style type='text/cc'>
h1 {color:green;}
body {font-size: 20px;}
</style>
<script>
function alertBox()
{
alert("You have reached the ALERT BOXX!");
}
</script>
</script>
<h1><center><font color="green">DRINKZ HOME PAGE</font></center></h1>
<a href='recipesList'><center>RECIPES</center><p></a>
<a href='inventoryList'><center>INVENTORY</center><p></a>
<a href='liquorTypes'><center>LIQUOR TYPES</center><p></a>
<a href='convertToML'><center>CONVERT TO ML</center><p></a>
<a href='wsgi_server'><center>WSGI SERVER TEST PAGE</center><p></a>
<a href='partyPage'><p><center><font size = +3>PARTY PAGE</font></center><p></a>
<p>
<a href='logout'><center>LOGOUT</center><p></a>
<center>
<input type="button" onclick="alertBox()" value="ALERT BOX" />
</center></head>
<body>

"""
        start_response('200 OK', list(html_headers))
        return [data]
    
    def login1(self, environ, start_response):
        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1:
            return self.index(environ,start_response)          
        else:
            start_response('200 OK', list(html_headers))
            title = 'login'
            loader = jinja2.FileSystemLoader('../drinkz/templates')
            env = jinja2.Environment(loader=loader)
            template = env.get_template('login1.html')
            return str(template.render(locals()))

    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        content_type = 'text/html'

        # authentication would go here -- is this a valid username/password,
        # for example?

        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/index'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to /index..."]

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /status..."]
    
    def status(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
                
        title = 'login status'
        loader = jinja2.FileSystemLoader('../drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('status.html')
        return str(template.render(locals()))

    def recipesList(self, environ, start_response):    
        data = recipesList()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def inventoryList(self, environ, start_response):
        data = inventoryList()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def liquorTypes(self, environ, start_response):
        data = liquorTypesList()
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def formConvertToML(self, environ, start_response):
	content_type = 'text/html'
	data = open('../drinkz/somefile.html').read()
        start_response('200 OK', list(html_headers))
	return [data]
    
    def recvAmount(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

	amount = results['amount'][0]
	amount = str(db.convert_to_ml(amount))

        content_type = 'text/html'
        data = "<font size = +4>The amount converted to ml = %s ml</font><p><a href='./'>GO TO HOME PAGE</a>" % (amount)
        start_response('200 OK', list(html_headers))
        return [data]
    #HW6
    def wsgi_server(self, environ, start_response):
	content_type = 'text/html'
	data = wsgiserver()
	start_response('200 OK', list(html_headers))
	return [data]

    def partyPage(self, environ, start_response):
	data = partyList()
	start_response('200 OK', list(html_headers))
	return [data]

    def hostneedsPage(self, environ, start_response):
	data = hostneedsList()
	start_response('200 OK', list(html_headers))
	return [data]

    def rating(self, environ, start_response):
	data = ratingPage()
	start_response('200 OK', list(html_headers))
	return [data]

    def addRating(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	rating = results['rating'][0]
	rating = db.add_rating(rating)

	content_type = 'text/html'
	data = "<font size = +4>The number of people who gave a: <p>"
	data += "<center>Rating of 1: %d <p>" %(db.get_num_of_one_ratings())
	data += "Rating of 2: %d <p>" %(db.get_num_of_two_ratings())
	data += "Rating of 3: %d <p></center></font>" %(db.get_num_of_three_ratings())
	data += "<p><a href='./partyPage'> GO TO PARTY PAGE</a>"

	start_response('200 OK', list(html_headers))
	return [data]

    def addHostNeedsItem(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	item_no = str(results['item'][0])
	
	if (db.check_hostneeds_list(item_no)):
	    item = db.get_hostneeds_item(item_no)
	    db.add_to_partylist(item)
	    db.delete_hostneeds_item(item_no)
	
	content_type = 'text/html'
	data = hostneedsList()

	start_response('200 OK', list(html_headers))
	return [data]

    def recv_wsgiserver(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	if ('port' in results.keys()):
	    port = int(results['port'][0])
	else:
	    port = 0

   	s = socket.socket()
	host = socket.gethostname()

	d = dict(method='add', params=[3,2], id = "0")
	encoded = simplejson.dumps(d)

	s.connect((host,port))
    	s.send('POST /rpc HTTP/1.0\n' + encoded + '\n\r\n\r\n')
	
	buffer = ""
	while "\r\n\r\n" not in buffer:
	    data = s.recv(1024)
	    buffer += data

	s.close()
	
	print 'gotbuffer:', buffer
        result = buffer.splitlines()
        num = result[2]
        
        content_type = 'text/html'
        
        data = "Server tested success<br>2+3="+num+"<p><a href='./'>Index</a>"
        
        start_response('200 OK', list(html_headers) )
        return [data]

    #HW5
    def addType(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	mfg = results['mfg'][0]
	liquor = results['liquor'][0]
	typ = results['typ'][0]

	db.add_bottle_type(mfg, liquor, typ)

	content_type = 'text/html'
	data = liquorTypesList()

	start_response('200 OK', list(html_headers))
	return [data]
    #HW5
    def addInventory(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	mfg = results['mfg'][0]
	liquor = results['liquor'][0]
	amt = results['amt'][0]
	
	try:
	    db.add_to_inventory(mfg, liquor, amt)
	    data = inventoryList()
	except Exception:
	    data = inventoryList() +"""<script> alert("That liquor is not an added type.");
</script>"""

	content_type = 'text/html'
	start_response('200 OK', list(html_headers))
	return [data]

    #HW5
    def addRecipe(self, environ, start_response):
	formdata = environ['QUERY_STRING']
	results = urlparse.parse_qs(formdata)

	name = results['name'][0]
	ings = results['ing'][0]
	myList = ings.split(',')
	myIngSet = set()
	
	i = 0
	while i < len(myList):
	   val = (ingred, amount) = (myList[i],myList[i+1])
	   myIngSet.add(val)
	   i+=2

	r = recipes.Recipe(name,myIngSet)

	try:
	    db.add_recipe(r)
	    data = recipesList()
	except Exception:
	    data = recipesList()

	content_type = 'text/html'
	start_response('200 OK', list(html_headers))
	return [data]



    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    # HW 5 Starts here

    def rpc_convert_units_to_ml(self,amount):        
	return str(db.convert_to_ml(amount))    

    def rpc_get_recipe_names(self):        
	recipeList = db.get_all_recipes()        
	nameList = list()        

	for recipe in recipeList:            
	    nameList.append(recipe._recipeName)        
	return nameList    

    def rpc_get_liqour_inventory(self):        
	liqourInvList = list()        

	for (m,l) in db.get_liquor_inventory():
            liqourInvList.append((m,l))
        return liqourInvList

    def rpc_get_liqour_types(self):
        liqourTypeList = list()

        for (m,l) in db.get_liquor_types():
            liqourTypeList.append((m,l))
        return liqourTypeList
                       
    def rpc_add_bottle_type(self,mfg,liquor,typ):
        returnVal = False

        try:
            db.add_bottle_type(mfg, liquor, typ)
            returnVal = True;
        except Exception:
            returnVal = False
        return returnVal

    def rpc_add_to_inventory(self,mfg,liquor,amount):
        returnVal = False

        try:
            db.add_to_inventory(mfg, liquor, amount)
            returnVal = True;
        except Exception:
            returnVal = False
        return returnVal

    def rpc_add_recipe(self,name,ings):
        myList = ings.split(',')
        myIngSet = set()
        i = 0

        while i < len(myList):
            
            val = (ingred,amount) = (myList[i],myList[i+1])
            myIngSet.add(val)
            i+=2
            
        r = recipes.Recipe(name,myIngSet)

        try:
            db.add_recipe(r)
            returnVal = True
        except Exception:
            returnVal = False
        return returnVal
    # HW 5 Ends here

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
''' 
def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
<p><a href='/'>Home</a>
"""
'''

'''
def convertToML():
    # this sets up jinja2 to load templates from the 'templates' directory
    loader = jinja2.FileSystemLoader('../drinkz/templates')

    env = jinja2.Environment(loader=loader)
    # pick up a filename to render
    filename = "pages.html"
    
    # variables for the template rendering engine
    vars = dict(title = 'Convert to ML', addtitle = "",
                form = """<form action='recvAmount'><center>
Enter amount(eg. 11 gallon or 120 oz or 15 liter)<input type='text' name='amount' size'20'>
<input type='submit'></center></form>""", names="")

    x = env.get_template(filename).render(vars).encode('ascii','ignore')
    return x
'''

# HW5 Changes Start Here

def recipesList():
    # this sets up jinja2 to load templates from the 'templates' directory
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "pages.html" #recipe nonsense
    recipeList = db.get_all_recipes()
    recipeNameList = list()
    for recipe in recipeList:
        if recipe.need_ingredients():
            val = "no"
        else:
            val = "yes"
        recipeNameList.append(recipe._recipeName + " " + val)
    
    
    # variables for the template rendering engine
    vars = dict(title = 'Recipe List', addtitle = "Add Recipe",
                form = """<form action='addRecipe'>
Name<input type='text' name='name' size'20'><p>
Ingredients (eg.'vodka,5 oz,grape juice,10 oz')<input type='text' name='ing' size'20'><p>
<input type='submit'>
</form>""", names=recipeNameList)

    try:
        template = env.get_template(filename)
    except Exception:# for nosetests
        loader = jinja2.FileSystemLoader('./drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template(filename)
        
    x = template.render(vars).encode('ascii','ignore')
    return x


def inventoryList():
    # this sets up jinja2 to load templates from the 'templates' directory
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "pages.html"

    inventoryList = list()
    for (m,l) in db.get_liquor_inventory():
        inventoryList.append(str(m)+ " " + str(l)+ " " + str(db.get_liquor_amount(m,l))+" ml")
    
    
    # variables for the template rendering engine
    vars = dict(title = 'Inventory List', addtitle = "Add to Inventory",
                form = """<form action='addInventory'>
Manufacturer<input type='text' name='mfg' size'20'><p>
Liquor<input type='text' name='liquor' size'20'><p>
Amount<input type='text' name='amt' size'20'><p>
<input type='submit'>
</form>""", names=inventoryList)

    template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')
    return x

def liquorTypesList():
    # this sets up jinja2 to load templates from the 'templates' directory
    
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "pages.html"

    liqourTypesList = list()
    for (m,l) in db.get_liquor_types():
        liqourTypesList.append(str(m)+ " " + str(l))

    # variables for the template rendering engine
    vars = dict(title = 'Liquor Types List', addtitle = "<p>Add Liquor Type",
                form = """<form action='addType'>
Manufacturer<input type='text' name='mfg' size'20'><p>
Liquor<input type='text' name='liquor' size'20'><p>
Generic Type<input type='text' name='typ' size'20'><p>
<input type='submit'>
</form>""", names=liqourTypesList)

    template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')
    return x


#HW 6.2
def partyList():
    # this sets up jinja2 to load templates from the 'templates' directory
    
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "party.html"

    partyList = list()
    complete_list = db.get_all_partylist()

    for item in complete_list:
        partyList.append(item)

    # variables for the template rendering engine
    vars = dict(title = 'Party List', names=partyList)

    #template = env.get_template(filename)
    try:
        template = env.get_template(filename)
    except Exception:# for nosetests
        loader = jinja2.FileSystemLoader('./drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')
    return x


def ratingPage():
    # this sets up jinja2 to load templates from the 'templates' directory
    
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "rating.html"

    # variables for the template rendering engine
    vars = dict(title = 'Rate this Party', addtitle = "", form = """<form
action='addRating'> Rate (on a scale of 1 to 3, 3 being the best)<input
type='text' name='rating' size'10'><p><input type='submit'></form>""", names =
"")

    x = env.get_template(filename).render(vars).encode('ascii','ignore')
    return x

def hostneedsList():
    # this sets up jinja2 to load templates from the 'templates' directory
    
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    # pick up a filename to render
    filename = "host_needs.html"

    hostNeedsList = list()
    for (m,l) in db.get_all_hostneeds_list():
        hostNeedsList.append(str(m) + "-" + str(l))
    print hostNeedsList

    # variables for the template rendering engine
    vars = dict(title = 'HOST NEEDS LIST', addtitle = "", form = """<form
action='addHostNeedsItem'>Enter the Item# associated with the Item that you
would like to bring<input type='text' name='item' size'20'><p>
<input type='submit'>
</form>""", names=hostNeedsList)

    template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')
    return x

#6.1
def wsgiserver():
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    filename = "wsgiserver.html"

    vars = dict(title = "Test WSGI server", title2 = "Enter the port # it is running on:", addtitle="Port:", form = """ <form action='recv_wsgiserver'><input type='text' name='port' size'20'><input type='submit'></form></body></html>""", bodyFormat = "")

    template = env.get_template(filename)

    result = template.render(vars).encode('ascii','ignore')
    
    return result


def WebServer():
    import random, socket
    port = random.randint(8000,9999)

    filename = 'myDatabase'
    load_db(filename)
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
