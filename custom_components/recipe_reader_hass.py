import urllib.request # for getting the page from the internet
import re # for using regex 
import sys # needed for sys.exit(), which ends execution
import logging # for displaying info in the HA log (I don't think this is the same as the front end)



# url to retrieve
# url = "http://www.seasonsandsuppers.ca/peach-dutch-baby-with-blueberry-sauce/"    #This one has ingredients in some kind of header
# url = "http://www.pbs.org/food/kitchen-vignettes/salted-honey-cranberry-pumpkin-seed-bars"
# url = "http://www.bettycrocker.com/recipes/easy-chocolate-banana-snack-cake/32f5b7ba-3226-4c35-bf63-bc42951f8f8a"
# url = "https://www.hersheys.com/celebrate/valentines/recipedetail.aspx?id=4780&name=Celebration-Tarts"
# url = "http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571"
# url = "http://allrecipes.com/recipe/222085/healthier-delicious-ham-and-potato-soup/?internalSource=staff%20pick&referringId=1552&referringContentType=recipe%20hub&clickId=cardslot%205"
# url = "http://simply-delicious-food.com/steak-mushroom-pot-pies/"
# url = "http://www.closetcooking.com/2011/04/jalapeno-popper-grilled-cheese-sandwich.html"
# url = "http://damndelicious.net/2014/03/15/one-pot-chili-mac-cheese/"

#
# sites that don't work are bettycrocker and simplydelicious
#
# seasonsandsuppers has recipe info in a style that this doesn't read yet
#



_LOGGER = logging.getLogger(__name__)

DOMAIN = 'recipe_reader_hass'

ATTR_URL = 'url'
DEFAULT_URL = 'http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571'
ATTR_INGR = 'ingredient'
DEFAULT_INGR = 'onion'
INGR_AMT = 'none'

def setup(hass, config):



    # This FancyURLopener helps get around websites that attempt to block python requests
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()


    
    def handle_hello(call):
        
        print('\n\n')
        print('-----------------------------------------------------------')
        print('\n')
        
        #get url and ingredient from parameters passed to the service
        url = call.data.get(ATTR_URL, DEFAULT_URL)
        ingredient = call.data.get(ATTR_INGR, DEFAULT_INGR)
        
        
        print("Retrieving webpage...")
        
       
        # files to save to
        filePath = ''
        recipeFileName = 'recipe.txt'
        ingFileName = 'ingredients.txt'   
        
        recipeFile = filePath + recipeFileName
        ingFile = filePath + ingFileName
        
        
        
        
        #
        #
        # should the file be saved in byte mode or regular mode?
        #
        #
        
        
        # Get the webpage and save it to a file
        req = opener.open(url)
        page_content = req.read()
        # with open(recipeFile, 'wb') as fid:   #original version that saved file as bytes
        with open(recipeFile, 'w+t', encoding='utf-8') as fid:   #open file in text mode with utf-8 encoding (to support all unicode characters)
            fid.write(page_content)       
        
        
        
        
        print("Opening file...")
        
        
        
        #
        #
        # should the file be opened in byte mode or regular mode?
        #
        #  
        
        # honestly, it would probably be best to skip the try,except and just start off by opening in utf-8 encoding
        
        
        try: #Try to open the file normally
            with open(recipeFile, 'r') as inf:
                filetext = inf.read()      

        except UnicodeDecodeError: #If there is an encoding error, open the file in a different format
            print("\n\nOpen failure! Trying again with with encoding=utf-8\n\n")
            with open(recipeFile, encoding='utf-8') as inf:
                filetext = inf.read()
                
         

        
        # Find the title of the recipe
        print("Finding recipe title...")

        #search for the title. It will probably be the first thing that is found between <title></title> tags
        pattern = re.compile("(?<=\<title\>)(.*?)(?=\<\/title\>)",re.DOTALL)
        match = re.search(pattern, filetext)

        # clean up the found title by removing junk
        cleanup = re.sub(r'[^\x00-\x7F]+',' ', match.group(0)) #remove non-ASCII characters by replacing them with white space
        title = re.sub(r'[\t\n\r\f\v]','', cleanup) #remove most "blank" characters that aren't spaces

        print('\n')
        print(title)
        
        
        
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
            # print(ingList[ndx])

        # remove any blank elements from ingList
        ingList = [x for x in ingList if x != '']
        
        # print the ingredient list
        print()
        for ndx, member in enumerate(ingList):
            print(ingList[ndx])
        
        
        print("Done.")
        # name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        # hass.states.set('hello_service.hello', name)
        
        print('\n\n')
        print('-----------------------------------------------------------')
        print('\n')

    hass.services.register(DOMAIN, 'hello', handle_hello)  
    
    return True   
    
    
    

