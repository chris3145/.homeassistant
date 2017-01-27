import urllib2
import os

# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'hello_service'

ATTR_NAME = 'name'
DEFAULT_NAME = 'World'


def setup(hass, config):
    """Setup is called when Home Assistant is loading our component."""
	    
    
    # page = urllib2.urlopen('http://stackoverflow.com')

    # page_content = page.read()

    with open('myotherfile.txt', 'w') as fid:
        fid.write('asdsad')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def handle_hello(call):
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set('hello_service.hello', name)
		
        print('\n\nTest\n\n')

        print(os.path.abspath("myfile.txt"))

        # f = open('myfile.txt', 'w')
        # f.write('hello there\n')  # python will convert \n to os.linesep
        # f.close()  # you can omit in most cases as the destructor will call it
        
        
        # with open('page_content.html', 'w') as fid:
            # fid.write(page_content)
            
    hass.services.register(DOMAIN, 'hello', handle_hello)
	
	

    # Return boolean to indicate that initialization was successfully.
    return True