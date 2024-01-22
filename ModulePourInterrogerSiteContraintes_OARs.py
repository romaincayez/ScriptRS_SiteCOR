import requests

URL = "http://vrttools:1337/api/"

def check_url(url):
    try:
        r = requests.get(url)
        return  r.status_code == 200
    except:
        return False

def get_indication(location='', organ='', fraction='', patient=''):
    url = URL + 'indication?'
    if location:
        print('location : ', location)
        url += 'location=' + location
    if organ:
        url += '&organ=' + organ
    if fraction:
        url += '&fraction=' + fraction
    if patient:
        url += '&patient=' + patient

    print(check_url(url))

    if check_url(url):
        print('ok')
        r = requests.get(url)
        return r.json()
    else:
        return {}

doseVessie = get_indication(location='ABDOMEN',
                            organ='A_Pulmonaire',
                            fraction='1',
                            patient='Adulte')
print(doseVessie)
print('toto')