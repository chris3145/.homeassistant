#
#
#This thing might fix the issue where FancyURLOpener doesn't report 403 errors
#
#

from urllib.request import FancyURLopener



class FixFancyURLOpener(FancyURLopener):

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        if errcode == 403:
            raise ValueError("403")
        return super(FixFancyURLOpener, self).http_error_default(
            url, fp, errcode, errmsg, headers
        )

# Monkey Patch
urllib.request.FancyURLopener = FixFancyURLOpener




#
#
#   Some possible ways to read a webpage that might detect a 403 error
#
#



req = urllib.request.urlopen(urls[ndx])

url = urllib.request.request('https://www.figma.com/afasdffwe')
# url = urllib.request.urlopen('https://www.figma.com/afasdffwe')
code = url.getcode()
print(code)
