import urllib3

def test_url():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://35.234.133.4:5000/') # can use post method too ## or ip address of the website:5000 when its running on another machine
    assert 200 == r.status  #200 = successful connection