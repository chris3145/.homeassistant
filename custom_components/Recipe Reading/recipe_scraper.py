import urllib.request # for getting the page from the internet
import re # for using regex 
import sys # needed for sys.exit(), which ends execution
import os # for making a directory

#
# User-entered data
#

# folder names to save the scraped html to
folderName_Byte = "RecipeScrapes_Byte"
folderName_String = "RecipeScrapes_String"


# urls to retrieve
urls = []

# 100% functional
urls.append("http://www.pbs.org/food/kitchen-vignettes/salted-honey-cranberry-pumpkin-seed-bars")  # This one uses some ingredients multiple times in its list. It would be a good one to test that sort of thing with.
# recipe1 is a broken file here from Hershey
urls.append("http://altonbrown.com/triple-cheese-popcorn-recipe/")      # Lists butter and buttermilk. That could be tricky when asking about butter. It also has canola oil listed twice.
urls.append("http://www.mantitlement.com/recipes/creamy-sausage-spaghetti/")    # Has two ingredient items with tomatoes
urls.append("http://www.theseasonedmom.com/one-dish-garlic-herb-pork-tenderloin/")
urls.append("http://www.closetcooking.com/2011/04/jalapeno-popper-grilled-cheese-sandwich.html")
urls.append("http://www.almondtozest.com/chicken-leek-brie-pie/")
urls.append("http://www.lecremedelacrumb.com/slow-cooker-ranch-chicken-tacos/") 
urls.append("http://www.pickledplum.com/spaghetti-squash-healthy-recipe/")
urls.append("http://feedmephoebe.com/meatless-monday-turkish-eggplant-casserole-recipe-tomatoes-imam-bayildi/")
urls.append("https://naturallyella.com/baby-broccoli-frittata-with-feta/")
urls.append("http://www.healthyseasonalrecipes.com/grilled-thai-coconut-lime-skirt-steak/")
urls.append("http://www.joyfulhealthyeats.com/sesame-lime-chicken-spicy-thai-peanut-sauce/")
urls.append("http://thewoksoflife.com/2014/10/lanzhou-beef-noodle-soup/")
urls.append("http://www.thecookierookie.com/skillet-basil-cream-chicken-2/")


# Finds ingredients along with some extra
urls.append("http://damndelicious.net/2014/03/15/one-pot-chili-mac-cheese/")
urls.append("http://allrecipes.com/recipe/222085/healthier-delicious-ham-and-potato-soup/?internalSource=staff%20pick&referringId=1552&referringContentType=recipe%20hub&clickId=cardslot%205")


# Doesn't work yet, but I should be able to fix it
urls.append("http://www.seasonsandsuppers.ca/peach-dutch-baby-with-blueberry-sauce/")   # LD+JSON - Has a header that I can't parse (yet). The header is inside a <script type="application/ld+json"> tag that is smushed into a single line
urls.append("http://www.marthastewart.com/340494/honeyed-ham-with-pears-and-cranberries?czone=entertaining/holiday-entertaining/holidaycenter-menus")  # LD+JSON Inline tags don't clearly mark ingredients, but there is a multi-line section inside of a <script type="application/ld+json"> tag that shows them well


# Difficult to fix
urls.append("http://www.plainchicken.com/2014/09/french-onion-chicken-noodle-casserole.html")   # They have a <ul class="ingredients"> item with <li> child items, but the child items aren't explicitly called out as ingredients. Here's a CSS Query that works: [class*="ingred"]>*
urls.append("http://www.bettycrocker.com/recipes/easy-chocolate-banana-snack-cake/32f5b7ba-3226-4c35-bf63-bc42951f8f8a")  # Could possibly work with a proper CSS search. Weird formatting across multiple lines and html tags


# No possible way
urls.append("http://simply-delicious-food.com/steak-mushroom-pot-pies/")   # This website has no ingredient formatting at all, just line breaks (sites like this will probably never work, but the routine needs to fail gracefully)
urls.append("http://bojongourmet.com/2011/10/roasted-eggplant-pizza-with-fontina/")  # Ingredients had no formatting on webpage
urls.append("https://www.bloglovin.com/blogs/clara-persis-11388463/curried-cauliflower-fritters-2616104191")  # Ingredients had no formatting on webpage
urls.append("http://www.thelondoner.me/2015/01/travelling-noodles.html")  # Ingredients had no formatting on webpage



# Not actually a recipe
urls.append("https://www.buzzfeed.com/melissaharrison/crock-pot-dump-dinners?utm_term=.xnae2pKZmN#.sob3qob5eD")   # This page doesn't actually have ingredients
urls.append("http://drizzleanddip.com/2014/02/10/pear-tartines-with-blue-cheese-and-pears")  # This page doesn't actually have ingredients
urls.append("http://www.goodenessgracious.com/2013/03/meals-made-easy-italian-dinner-edition.html")  # Webpage does not have ingredients


# ?
# urls.append("http://www.pipandebby.com/pip-ebby/2014/2/15/the-best-chili-on-earth.html")  # http.client.IncompleteRead: IncompleteRead(xxx bytes read, xxx more expected)


# Can't open webpage
# urls.append("http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571")  # This is one I might be blocked from now. I get a "ValueError: read of closed file"    This worked (with some extra "ingredients") back when I could access it 
# urls.append("http://www.cookingclassy.com/grilled-ginger-sesame-chicken-chopped-salad/")   #fails to open file afterward (Initially I got HTTP 403 errors, though they weren't shown properly. Then I got websocket terminations.)
urls.append("http://www.onehundreddollarsamonth.com/meyer-lemon-ginger-marmalade-recipe/")  # Failed to access webpage
urls.append("http://thepioneerwoman.com/cooking/beautiful-roasted-vegetables/")  # Failed to access webpage
# urls.append("https://www.hersheys.com/celebrate/valentines/recipedetail.aspx?id=4780&name=Celebration-Tarts")  # Page content comes back blank, but no error. It worked before. # This one uses butter twice (One item is 2 tablespoons of butter. Another is 1 tbsp of butter, melted.)




#
#
#  Rest of code
#
#



# Header for printing
print('\n\n')
print('-----------------------------------------------------------')
print('\n')



# This FancyURLopener helps get around SOME websites that attempt to block python requests
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()



# Set up file paths. Determine their absolute location, and create the directories if they don't already exist
# Find the path that the script is running from
localFolder = os.path.dirname(__file__)

# Create the complete path to folders (so they are placed in the directory where the script is running from)
filePath_String = localFolder + "\\" + folderName_String
# filePath_Byte = localFolder + "\\" + folderName_Byte

# Create directories if they don't already exist
if not os.path.isdir(filePath_String):
    os.makedirs(filePath_String)
  
# if not os.path.isdir(filePath_Byte):
    # os.makedirs(filePath_Byte)



# The loop that reads, saves, and reads each URL
for ndx, member in enumerate(urls): 
    
    recipeFile = "recipe" + str(ndx) + ".txt"
    
    print('\n')
    print("Recipe number ", ndx)
    print(urls[ndx])
    
    try :
        # Get the webpage content
        req = opener.open(urls[ndx])
        page_content = req.read()
                
    except :
        print("Failed to load webpage.")
        page_content = "<title>Failed to load webpage</title>".encode()

            
    # # save the page to a file in byte form
    # with open(filePath_Byte + "\\" + recipeFile, 'w+b') as fid:   
        # fid.write(urls[ndx].encode())
        # fid.write('\r\n\r\n\r\n'.encode())
        # fid.write(page_content)


    # save the page to a file in text (string) form
    with open(filePath_String + "\\" + recipeFile, 'w+t', encoding='utf-8') as fid:   
        fid.write(urls[ndx])
        fid.write('\n\n\n')
        fid.write(page_content.decode())

        
        
    print("Reading text file", ndx)
    with open(filePath_String + "\\" + recipeFile, 'rt', encoding='utf-8') as inf:
                filetext = inf.read()
    
    
# Footer for printing

print('\n')
print('-----------------------------------------------------------')
print('\n\n')
