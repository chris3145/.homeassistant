import urllib.request # for getting the page from the internet
import re # for using regex 

# This FancyURLopener helps get around websites that attempt to block python requests
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

# url to retrieve
# url = "http://www.bettycrocker.com/recipes/dishes/brownie-recipes/heart-shaped-brownies"
url = "https://www.hersheys.com/celebrate/valentines/recipedetail.aspx?id=4780&name=Celebration-Tarts"
# url = "http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571"
# url = "http://www.fooducate.com/app#!page=product&id=56F0B4FE-95E8-DAED-4239-9A990A5F831C"


# url = "http://simply-delicious-food.com/steak-mushroom-pot-pies/"
ingredient = "butter"

# file to save to
fileName = 'recipe.txt'



print("Retrieving webpage...")

# Get the webpage and save it to a file
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


print(title)

#find a specific ingredient

#find all html list items that include that ingredient
ingpattern1 = re.compile("[(<li)(^)][^<]*"+ingredient+".*?[(<)(\n)]",re.IGNORECASE|re.MULTILINE)
ingmatch = re.findall(ingpattern1, filetext)

print(ingmatch)
# for each item that was found, strip out the html tags
for ndx, member in enumerate(ingmatch):
    print(ndx)
    print(ingmatch[ndx])    
    ingpattern2 = re.compile("(?<=>)(.*?)(?=[(<)(\n)])") # pattern that finds everything between '>' and '<' (can also end with a new line)
    ingmatch[ndx] = re.search(ingpattern2,ingmatch[ndx]).group(0) # sets the element in ingmatch to the version with html stripped out
    print("\n\n")

print(ingmatch)
#guess that the shortest string is the one that lists an ingredient amount
AmtGuess = min(ingmatch, key=len)

print(AmtGuess)








#find all html list items that include that ingredient
# ingpattern1 = re.compile("[(<li)(\n)][^<]*"+ingredient+".*?[(<)(\n)]",re.IGNORECASE)
# ingmatch = re.findall(ingpattern1, filetext)

  
# for each item that was found, strip out the html tags
# for ndx, member in enumerate(ingmatch):
    
    # ingpattern2 = re.compile("(?<=[(>)(\n))(.*?)(?=[<\n])") # pattern that finds everything between '>' and '<' (can also end with a new line)
    # ingmatch[ndx] = re.search(ingpattern2,ingmatch[ndx]).group(0) # sets the element in ingmatch to the version with html stripped out
    
    
    
    
    
    
    
    
#find all html list items that include that ingredient
# ingpattern1 = re.compile("<li[^<]*"+ingredient+".*?[<\n]",re.IGNORECASE)
# ingmatch = re.findall(ingpattern1, filetext)

  
# for each item that was found, strip out the html tags
# for ndx, member in enumerate(ingmatch):
    
    # ingpattern2 = re.compile("(?<=>)(.*?)(?=[<\n])") # pattern that finds everything between '>' and '<' (can also end with a new line)
    # ingmatch[ndx] = re.search(ingpattern2,ingmatch[ndx]).group(0) # sets the element in ingmatch to the version with html stripped out