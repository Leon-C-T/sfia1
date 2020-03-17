import urllib3

def test_url():
    http = urllib3.PoolManager() 
    r = http.request('GET', 'http://mintbookings.ddns.net') # can use post method too
    assert 200 == r.status  #200 = successful connection