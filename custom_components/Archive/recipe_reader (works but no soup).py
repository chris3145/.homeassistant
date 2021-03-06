import json
import urllib.request # for getting the page from the internet
import requests
import re # for using regex 
import os # for making a directory
import sys
import html # for extracting html characters
import logging # for logging to home assistant logs


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'recipe_reader'

ATTR_URL = 'url'
DEFAULT_URL = ''
ATTR_INGR = 'ingredient'
DEFAULT_INGR = ''
INGR_AMT = 'none'

        
def setup(hass, config):
    
    # This is used to bypass some of the webpages that attempt to block access from Python
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
       
    
    # set file locations
    folderName = "recipeFiles"           
    fileName = "recipe.txt"        

    # build the file path based on the directory the script is running from
    localFile = os.path.dirname(__file__)
    localFolder = os.path.abspath(localFile)


    filePath = os.path.join(localFolder,folderName)
    rcpFile = os.path.join(filePath,fileName)

    print(rcpFile)
    
    
    # Create the recipe data folder if it doesn't exist already
    if not os.path.isdir(filePath):
        os.makedirs(filePath)
    
    
    
    def formatForAlexa(data, intent):
        '''When given a result and the type of intent,
        format a response for Alexa to speak'''
    
        print('Formatting for Alexa')
        
        # if the request was to find an ingredient amount
        if intent is 'getIngredientAmount':
            
            # if no matches were found, say that. Make sure to name the ingredient so the user knows what it was looking for.
            # This scenario should be caught elsewhere and never reach this point, but here's some code that can handle it just in case.
            if not data:
                response = "I wasn't able to find that item in the ingredient list."
                
            #if the ingredient was found    
            else:
            
                #if there was only one match, read the match
                if len(data) == 1: 
                    response = "Here's what I found: " + data[0]
                    
                # if there were multiple matches, assemble them into a single spoken response    
                else:
                    response = "I found multiple entries for that ingredient. "
                    
                    for ndx, member in enumerate(data):
                        response += '<break strength="x-strong"/> The <say-as interpret-as="ordinal">' + str(ndx+1) + '</say-as> is ' + data[ndx]          
            
        print('\n')
        print(response)
        print('\n')

        return response
    
    
    def saveRecipe(url, recipeFile):
        '''Save the contents of a url to a .txt file at a given location'''
        
        print("Retrieving webpage")
        
        # try to get the webpage content
        try:
            # Get the webpage content (using urllib request form)
            # req = opener.open(url)
            # page_content = req.read()
            
            
            # Get webpage content (with requests)
            r = requests.get(url)
            
        
        except (FileNotFoundError, ValueError):
            print("Webpage could not be reached!")
            page_content = "<title>Failed to load webpage</title>".encode()
            raise
            
        
        # save the page content to the provided .txt file
        try:
            with open(recipeFile, 'w+t', encoding='utf-8') as fid:   
                fid.write(url)
                fid.write('\n\n\n')
                fid.write(r.text)
                
                # old format with urllib
                # fid.write(page_content.decode())
                
                
                
                
        except FileNotFoundError:
            print("Destination directory not found!")
            raise
            
            
      
    def getTitle(recipeFile):
        '''Get the title from the recipe file'''
        
        print("Finding title")
        
        # open the file and get its text
        with open(recipeFile, 'rt', encoding='utf-8') as inf:              
            url = inf.readline()  # get the url from the first line of the file
            filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
          
        # escape html character encodings
        filetext = html.unescape(filetext)
        
        #search for the first thing that is found between <title></title> tags
        pattern = re.compile("(?<=\<title\>)(.*?)(?=\<\/title\>)",re.DOTALL)
        match = re.search(pattern, filetext)
        
        # check if a title was a found and clean it up
        try:
            # try to clean up the result that was found.
            title = re.sub(r'[^\x00-\x7F]+',' ', match.group(0)) #remove non-ASCII characters by replacing them with white space
            title = re.sub(r'[\t\n\r\f\v]','', title) #remove most "blank" characters that aren't spaces
            title.strip()  #remove leading or trailing white space from title
            
           
        except AttributeError:
            # if cleaning failed because no title was found, set the title to "Title not found!"
            print("Title not found!")
            title = "Title not found!"
            
        finally:
            return title


      
    def getIngredientList(recipeFile):
            
        print("Finding ingredients")
        
        # open the file and get its text
        with open(recipeFile, 'rt', encoding='utf-8') as inf:              
            url = inf.readline()  # get the url from the first line of the file
            filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
        
        filetext = html.unescape(filetext)
        #
        # find an ingredient list
        #

        # find all html tags that include contain "ingredient (keep the open quote to avoid finding extra stuff, but leave off the closing quote so that it still works if labels are plural or have suffixes)
        # or maybe leave off the open quote to help find "p-ingredient" tags or "RecipeIngredient" tags
        ingpattern1 = re.compile("<[^>]*?ingredient[^>]*>.*?<",re.IGNORECASE)
        ingList = re.findall(ingpattern1, filetext)

        # for each item that was found, strip out the html tags and leave behind what was in between them
        for ndx, member in enumerate(ingList):
            # print('\n')
            # print(ndx)
            # print(ingList[ndx])
            ingpattern2 = re.compile("(?<=>)(.*?)(?=<)") # pattern that finds everything between '>' and '<' (can also end with a new line)
            ingList[ndx] = re.search(ingpattern2,ingList[ndx]).group(0) # sets the element in ingList to the version with html stripped out
            ingList[ndx].strip()

        # remove any blank elements from ingList
        ingList = [x for x in ingList if x != '']

        return ingList
        
    def respondWithIFTTT(response):
        
        _LOGGER.info("Responding through IFTTT. Result: " +response)        
       

       # Send a request to IFTTT containing the result
        # print("Sending IFTTT request")
        
        IFTTTurl = "https://maker.ifttt.com/trigger/Text_Me/with/key/dt6NqmWkQPIXhE5OopFufv"
        values = {'value1':response}#str(ingResult[0])}
        
        params = json.dumps(values).encode('utf8')
        req = urllib.request.Request(IFTTTurl, params, headers={'content-type': 'application/json'})
        
        response = urllib.request.urlopen(req)
        
        print(response.read().decode('utf8')) #print IFTTT response
    
    
    def downloadRecipe(call):
        '''Setup function that is called when first receiving the url.
        This runs all of the functions to save the webpage, extract the title, and extract the ingredients.
        '''
        
        print("Download service called")
                
        global rcpTitle
        global rcpIngList
        
        #get the url from the service call
        url = call.data.get(ATTR_URL, DEFAULT_URL)
        
        #attempt to open the url and save the contents to a file
        # if there is an error, end code execution
        try:
            saveRecipe(url, rcpFile)
            pass
        except (FileNotFoundError, ValueError):
            _LOGGER.error("Something went wrong while retrieving the recipe. Ending execution. URL was ", url)
            # print("Something went wrong while retrieving the recipe. Ending execution.") 
            sys.exit()

            
            
        # get the recipe title and the list of ingredients
        rcpTitle = getTitle(rcpFile)      
        rcpIngList = getIngredientList(rcpFile)
        
        print('\n\n',rcpTitle)
        print('\n',rcpIngList)

        # print("Recipe setup complete!")
        _LOGGER.info("Recipe parameters loaded!")
        
        respondWithIFTTT("Recipe downloaded!")

         

    def findAmount(call):
        ''' when given an ingredient and an ingredient list, find all entries of the list that mention the ingredient'''
        ''' The function will return ingResult, which contains the dictionary of matches, but the return probably won't be used.
            It will also set the alexa_response state which is what Alexa speaks back to the person'''
               
        # when called as a home assistant service, getting the ingredient looks like this
        ingredient = call.data.get(ATTR_INGR, DEFAULT_INGR)
        
        # when called directly, use this
        # ingredient = call

        
        _LOGGER.info("Finding ingredient amount. Searching for '"+ingredient+"' in ingredient list.")
                
        try:
            ingResult = [x for x in rcpIngList if ingredient in x]
         
        # This error is thrown when no ingredient list exists            
        except NameError:

            # print("\n Point B")
            _LOGGER.error("No ingredient list found!")
            alexaResponse = "I couldn't find a list of ingredients."     
        
        # This code runs if no exception was thrown (i.e. there was an ingredient list)            
        else:

            # if the ingredient was found in the ingredient list
            if ingResult:
                # print('\n Point D')
                alexaResponse = formatForAlexa(ingResult, 'getIngredientAmount')                
                
                # for ndx, member in enumerate(ingResult):
                    # print(ingResult[ndx])                 
            
            # if the ingredient wasn't found
            else:
                # print('\n Point E')
                
                _LOGGER.error("Ingredient '" + ingredient + "' was not found.")
                alexaResponse = "I wasn't able to find " + ingredient + " in the list of ingredients."
           
        # no matter what happens, set the alexaResponse    
        finally:   
            
            # record the result in the log and set the state that Alexa reads from
            _LOGGER.info("getIngredientAmount response: " + alexaResponse)          
            hass.states.set('recipe_reader.alexa_response', alexaResponse)
            
            return ingResult

    # @app.route('/webhook', methods=['POST'])
    def webhook(request):
   
        
        print("Webhook called")
        
        # print('\n\n')
        # print("Request received as ", type(request))
        # print("Request body is ", type(request.body))
        # print(request)
        
        requestStr = str(request)
        print('\n\n')
        
        ingStartPos = requestStr.find('\'ingredient\': \'')
        ingEndPos = requestStr.find(',', ingStartPos) 
        foundIng = requestStr[ingStartPos+15:ingEndPos-1]
        
        print('Ingredient: "'+foundIng+'"')
        # print(requestStr)
       
        
        print('\n\n')
        
        
        ingAmt = findAmount(foundIng)
        
        print(ingAmt[0])
        
        respondWithIFTTT(ingAmt[0])
        
        print('\n\n')
              
    
    #these are the services that will be exposed to home assistant
    hass.services.register(DOMAIN, 'webhook', webhook)
    hass.services.register(DOMAIN, 'downloadRecipe', downloadRecipe)  
    hass.services.register(DOMAIN, 'findAmount', findAmount)
    
    print('\n\n\n')
    # # print('Previous title:', rcpTitle)
    
    try:
        _LOGGER.info("Recipe reader is attempting to load parameters from last-used recipe.")
        rcpTitle = getTitle(rcpFile)        
        rcpIngList = getIngredientList(rcpFile)
        _LOGGER.info("Data retrieval succeeded!")
    except FileNotFoundError:
        _LOGGER.warn("No recipe file found.")  
    
    # Set a state to display on the front end
    hass.states.set('recipe_reader.Title', rcpTitle)
    hass.states.set('recipe_reader.ing_amount', 'no search yet')
    
    # print('Title after update:', rcpTitle)
    # print('\n\n\n')
    
    return True