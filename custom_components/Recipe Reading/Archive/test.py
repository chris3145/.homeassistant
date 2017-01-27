import urllib.request # for getting the page from the internet
import re # for using regex 



# url to retrieve
url = "http://www.thewickednoodle.com/turkey-tetrazzini/#_a5y_p=5810571"


print("Retrieving webpage...")


# Get the webpage and save it to recipe.txt
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})  #This user agent business gets around some sites that block calls from Python  
page = urllib.request.urlopen( req )
page_content = page.read()
with open('recipe.txt', 'wb') as fid:   
    fid.write(page_content) 
    
    
print("Webpage retrieved.")
print("Finding recipe title.")