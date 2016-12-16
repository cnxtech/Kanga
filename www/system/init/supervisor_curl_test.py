from urllib2 import urlopen, Request, URLError, HTTPError





try:
    timeout = 2
    url = 'http://10.251.21.176:9001/index.html?processname=elasticsearch&action=start'
    response = urlopen(Request(url), timeout=timeout)
    html = response.read()
except (URLError, HTTPError) as e:
    print e
