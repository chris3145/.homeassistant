import urllib.request # for getting the page from the internet
import re # for using regex 
import sys # needed for sys.exit(), which ends execution

# This FancyURLopener helps get around websites that attempt to block python requests
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

# url to retrieve
# url = "http://www.pbs.org/food/kitchen-vignettes/salted-honey-cranberry-pumpkin-seed-bars"
# url = "http://www.bettycrocker.com/recipes/easy-chocolate-banana-snack-cake/32f5b7ba-3226-4c35-bf63-bc42951f8f8a"
# url = "https://www.hersheys.com/celebrate/valentines/recipedetail.aspx?id=4780&name=Celebration-Tarts"
# url = "http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571"
# url = "http://allrecipes.com/recipe/222085/healthier-delicious-ham-and-potato-soup/?internalSource=staff%20pick&referringId=1552&referringContentType=recipe%20hub&clickId=cardslot%205"
# url = "http://simply-delicious-food.com/steak-mushroom-pot-pies/"
# url = "http://www.closetcooking.com/2011/04/jalapeno-popper-grilled-cheese-sandwich.html"
url = "http://damndelicious.net/2014/03/15/one-pot-chili-mac-cheese/"

#
#
# sites that don't work are bettycrocker and simplydelicious
#
#

# file to save to
# fileName = 'recipe.txt'
# fileName = 'Recipe Texts/PBS.txt' # url = "http://www.pbs.org/food/kitchen-vignettes/salted-honey-cranberry-pumpkin-seed-bars"
# fileName = 'Recipe Texts/bettycrocker.txt' # url = "http://www.bettycrocker.com/recipes/easy-chocolate-banana-snack-cake/32f5b7ba-3226-4c35-bf63-bc42951f8f8a"
# fileName = 'Recipe Texts/hersheys.txt' # url = "https://www.hersheys.com/celebrate/valentines/recipedetail.aspx?id=4780&name=Celebration-Tarts"
# fileName = 'Recipe Texts/thewickednoodle.txt' # url = "http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571"
# fileName = 'Recipe Texts/AllRecipes.txt' # url = "http://allrecipes.com/recipe/222085/healthier-delicious-ham-and-potato-soup/?internalSource=staff%20pick&referringId=1552&referringContentType=recipe%20hub&clickId=cardslot%205"
# fileName = 'Recipe Texts/SimplyDelicious.txt' # url = "http://simply-delicious-food.com/steak-mushroom-pot-pies/"
# fileName = 'Recipe Texts/closetCooking.txt' # url = "http://www.closetcooking.com/2011/04/jalapeno-popper-grilled-cheese-sandwich.html"
fileName = 'Recipe Texts/damndelicious.txt' # url = "http://damndelicious.net/2014/03/15/one-pot-chili-mac-cheese/"

ingredient = "eggs"

print("Retrieving webpage...")

# # Get the webpage and save it to a file
# req = opener.open(url)
# page_content = req.read()
# with open(fileName, 'wb') as fid:   
    # fid.write(page_content) 
  
print("Opening file...")

try: #Try to open the file normally
    with open(fileName, 'r') as inf:
        filetext = inf.read()      

except UnicodeDecodeError: #If there is an encoding error, open the file in a different format
    with open(fileName, encoding='utf-8') as inf:
        filetext = inf.read()
        
        
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
# or maybe leave off the open quote to help find "p-ingredient" tags used in h-recipe formats
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

print()
for ndx, member in enumerate(ingList):
    print(ingList[ndx])



#
# find a list of cooking instructions
#

instrpattern1 = re.compile("<[^>]*?recipeInstructions[^>]*>.*?<",re.IGNORECASE)
instrList = re.findall(instrpattern1, filetext)



#print the ingredient list
print()
# for ndx, member in enumerate(instrList):
    # print(instrList[ndx])


    
    
#
#   if finding an ingredient with jsoup,
#   the CSS query might look something
#   like this: [itemprop*=ingredient]:contains(butter)
#
#   This finds any item where the itemprop attribute contains ingredient and the text underneath contains butter
#
    
    
    
    
# print(ingEntry)












############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################










#
#
#   OLD REFERENCE STUFF   
#
#





#
#  Finding ingredients by looking for html tags that include "ingredient
#

# # find an ingredient list

# # find all html tags that include contain "ingredient (keep the open quote to avoid finding extra stuff, but leave off the closing quote so that it still works if labels are plural or have suffixes
# ingpattern1 = re.compile("<[^>]*?\"ingredient[^>]*>.*?<",re.IGNORECASE)
# ingList = re.findall(ingpattern1, filetext)

# # for each item that was found, strip out the html tags and leave behind what was in between them
# for ndx, member in enumerate(ingList):
    # # print(ndx)
    # # print(ingList[ndx])    
    # ingpattern2 = re.compile("(?<=>)(.*?)(?=<)") # pattern that finds everything between '>' and '<' (can also end with a new line)
    # ingList[ndx] = re.search(ingpattern2,ingList[ndx]).group(0) # sets the element in ingList to the version with html stripped out
    # # print("\n\n")

# # print(ingList)

# # remove any blank elements from ingList
# ingList = [x for x in ingList if x != '']











#find all html list items that include that ingredient
# ingpattern1 = re.compile("[(<li)(\n)][^<]*"+ingredient+".*?[(<)(\n)]",re.IGNORECASE)
# ingList = re.findall(ingpattern1, filetext)

  
# for each item that was found, strip out the html tags
# for ndx, member in enumerate(ingList):
    
    # ingpattern2 = re.compile("(?<=[(>)(\n))(.*?)(?=[<\n])") # pattern that finds everything between '>' and '<' (can also end with a new line)
    # ingList[ndx] = re.search(ingpattern2,ingList[ndx]).group(0) # sets the element in ingList to the version with html stripped out
    
    
    
    
    
    
    
    
#find all html list items that include that ingredient
# ingpattern1 = re.compile("<li[^<]*"+ingredient+".*?[<\n]",re.IGNORECASE)
# ingList = re.findall(ingpattern1, filetext)

  
# for each item that was found, strip out the html tags
# for ndx, member in enumerate(ingList):
    
    # ingpattern2 = re.compile("(?<=>)(.*?)(?=[<\n])") # pattern that finds everything between '>' and '<' (can also end with a new line)
    # ingList[ndx] = re.search(ingpattern2,ingList[ndx]).group(0) # sets the element in ingList to the version with html stripped out