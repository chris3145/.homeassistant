import urllib.request # for getting the page from the internet
import re # for using regex 
import sys # needed for sys.exit(), which ends execution
import os # for making a directory
import html # for converting escape characters into ascii (e.g. turns &amp; into &)
import testFunc


# recipe to search and ingredient to search for
# recipeNum = 3
ingredient = 'salt'

# folders where pages are saved
folderName_String = "RecipeScrapes_String"
folderName_Results = "ProcessResults"

        
print('\n\n')
print('-----------------------------------------------------------')
print('\n')




# Find the path that the script is running from
localFolder = os.path.dirname(__file__)

# Create the complete path to folders (so they are placed in the directory where the script is running from)
filePath_String = localFolder + "\\" + folderName_String
filePath_Results = localFolder + "\\" + folderName_Results

# Create the results folder if it doesn't exit already
if not os.path.isdir(filePath_Results):
    os.makedirs(filePath_Results)

ndx=3

for ndx in range(1):

    #read the contents of a file
    print("Reading text file", ndx)
    
    testFunc.hello()
    
    
    #get the file name
    recipeFile = "recipe" + str(ndx) + ".txt"

    with open(filePath_String + "\\" + recipeFile, 'rt', encoding='utf-8') as inf:              
                url = inf.readline()  # get the url from the first line of the file
                filetext = inf.read()  # get the rest of the file (doesn't include the first line because that was already read)
      

    filetext = html.unescape(filetext)

      
    # Find the title of the recipe

    #search for the title. It will probably be the first thing that is found between <title></title> tags
    pattern = re.compile("(?<=\<title\>)(.*?)(?=\<\/title\>)",re.DOTALL)
    match = re.search(pattern, filetext)
    

    try:
        # clean up the found title by removing junk
        title = re.sub(r'[^\x00-\x7F]+',' ', match.group(0)) #remove non-ASCII characters by replacing them with white space
        title = re.sub(r'[\t\n\r\f\v]','', title) #remove most "blank" characters that aren't spaces
        title.strip()  #remove leading or trailing white space from title
    except AttributeError:
        title = "Title not found."
    
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
        ingList[ndx].strip()
        # print(ingList[ndx])

    # remove any blank elements from ingList
    ingList = [x for x in ingList if x != '']

    
   
    # open a file. Write the url, title, and ingredient list to that file
    with open(filePath_Results + "\\" + recipeFile, 'w+t', encoding='utf-8') as fid:   
        fid.write(url)
        fid.write('\n\n\n')
        fid.write(title)
        fid.write('\n------------------------------------------------\n')
        
        for ndx, member in enumerate(ingList):
            fid.write('\n'+ingList[ndx])

     
    # find ingredients in the ingredient list
    ingResult = [x for x in ingList if ingredient in x]
            
    print(ingResult)        
            
print("Done.")

print('\n\n')
print('-----------------------------------------------------------')
print('\n')





