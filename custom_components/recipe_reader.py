# import json
import urllib.request # for getting the page from the internet
import requests
import re # for using regex 
import os # for making a directory
import sys
import html # for extracting html characters
import logging # for logging to home assistant logs
from bs4 import BeautifulSoup # BeautifulSoup is used for most of the HTML parsing


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
       
    print('\n\n\n\n\n\n')
    # set file locations
    folderName = "recipeFiles"           
    fileName = "recipe.txt"        

    # build the file path based on the directory the script is running from
    localFile = os.path.dirname(__file__)
    localFolder = os.path.abspath(localFile)


    filePath = os.path.join(localFolder,folderName)
    rcpFile = os.path.join(filePath,fileName)

    print(rcpFile)
    print('\n\n\n\n\n\n')
    
    # Create the recipe data folder if it doesn't exist already
    if not os.path.isdir(filePath):
        os.makedirs(filePath)
        
        
    print('\n\n\n\n\n\n')  
    print('Point A')
        
        
    
    def trim(s):
        '''
        remove whitespace on left and right of string s.
        trim whitespace between characters to a single space
        ''' 
        # This seems to be the only way to properly handle the Betty Crocker website which has a bunch of stuff in between the amount for an ingredient and the rest of the ingredient entry
        
        return " ".join(s.split())
    
    
    print('\n\n\n\n\n\n')  
    print('Point B')  


    
    def isSchemaOrgStandard(soup):
        '''Determine if the recipe uses the schema.org/Recipe standard'''
        
        # see if any tags are found that contain the itemtype flag for schema.org/Recipe standard
        try:
            return soup.findAll(True, {"itemtype" : re.compile("http://schema.org/Recipe", re.IGNORECASE)}) != []
            
        except Exception as e:
            logging.debug(e)
            return False    
 
    print('\n\n\n\n\n\n')  
    print('Point C')  

 
    def findIngList(soup):
        '''Extract the list of ingredients from the HTML'''
        
        # if the soup fits the schema.org format
        if isSchemaOrgStandard(soup):
            ingList = soup.findAll(True, {"itemprop" : re.compile("ingredients", re.IGNORECASE)})    
            
            # for each element in the list, set the element to the text inside the html tags (i.e. remove the html tags themselves)
            for ndx, member in enumerate(ingList):            
                ingList[ndx] = trim(ingList[ndx].get_text()) # set the list elements to be just the text without the HTML tags and strip any whitespace off the ends
        
            return ingList
            
        return ['']
        
    def findStepList(soup):
        '''Extract the list of recipe steps from the HTML'''
        
        # if the soup fits the schema.org format
        if isSchemaOrgStandard(soup):
            stepList = soup.findAll(True, {"itemprop" : re.compile("instructions", re.IGNORECASE)})
        
            # for each element in the list, set the element to the text inside the html tags (i.e. remove the html tags themselves)
            for ndx, member in enumerate(stepList):            
                stepList[ndx] = trim(stepList[ndx].get_text()) # set the list elements to be just the text without the HTML tags and strip any whitespace off the ends
        
            return stepList
        return ['']
        
    def findTitle(soup):

        # first try to use og:title tag
        og_title = (soup.find("meta", attrs={"property": "og:title"}) or soup.find("meta", attrs={"name": "og:title"}))
        
        if og_title and og_title["content"]:
            print("Title found using og:title tag.")
            return og_title["content"]
        
      
        # if that didn't work get the recipe title from a <title> tag
        if soup.title and soup.title.string:
            print("Title found using <title> tag.")
            return soup.title.string
        
        # if nothing worked, return None
        return ''   


    
        
    
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
            # Get webpage content (with requests)
            r = requests.get(url)
            
            
            # Get the webpage content (using urllib request form)
            # req = opener.open(url)
            # page_content = req.read()
            
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
        
    def htmlParse(recipeFile):
        global rcpTitle
        global rcpIngList
        global rcpStepList

        
        # open the file and read it
        with open(recipeFile, 'rt', encoding='utf-8') as inf:              
            url = inf.readline()  # get the url from the first line of the file
            filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
            filetext = html.unescape(filetext)
            soup = BeautifulSoup(filetext, 'html.parser')
            
        
        # get the recipe title and the list of ingredients
        rcpTitle = findTitle(soup)      
        rcpIngList = findIngList(soup)
        rcpStepList = findStepList(soup)
        
        
            
    def downloadRecipe(call):
        '''Setup function that is called when first receiving the url.
        This runs all of the functions to save the webpage, extract the title, and extract the ingredients.
        '''
        
        print("Download service called")
                

        
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


    print('\n\n\n\n\n\n')  
    print('Point D')         
    
    #these are the services that will be exposed to home assistant
    hass.services.register(DOMAIN, 'downloadRecipe', downloadRecipe)  
    hass.services.register(DOMAIN, 'findAmount', findAmount)
    
    print('\n\n\n\n\n\n')  
    print('Point E')  
    # # print('Previous title:', rcpTitle)
    
    try:
        _LOGGER.info("Recipe reader is attempting to load parameters from last-used recipe.")
        htmlParse(rcpFile)
        _LOGGER.info("Data retrieval succeeded!")
    except FileNotFoundError:
        _LOGGER.warn("No recipe file found.")  
    
    print('\n\n\n\n\n\n')  
    print('Point F')  
    
    print(rcpTitle)
    
    # Set a state to display on the front end
    hass.states.set('recipe_reader.Title', 'no title yet')
    hass.states.set('recipe_reader.ing_amount', 'no search yet')
    
    # print('Title after update:', rcpTitle)
    # print('\n\n\n')
    
    return True