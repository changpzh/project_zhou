try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import webbrowser
webpage = urlopen('http://www.baidu.com')
print(webpage)
# webbrowser.open('http://www.python.org')