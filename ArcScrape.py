import urllib.request
import json

class Server(object):

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self,url):
        if url[-1] == '/':
            self.__url = url[:-1]
        else:
            self.__url = url 

    def get_range(self, nums):
        out = {}
        for num in nums:
            out[num] = self.get_id(num)
        return out

    def get_id(self,num):
        url = self.url + '/0/{}?f=pjson'.format(num)
        with urllib.request.urlopen(url) as site:
            resp = site.read().decode('utf-8')

        return json.loads(resp)

    def __init__(self, base_url):
        self.url = base_url

def to_geojson(data,geom_type='Polygon'):
    '''Currently only supports Polygon and Points.'''

    if geom_type=='Polygon':
        geojson = { 
        "type": "Feature",
        "geometry": {
            "type": geom_type,
            "coordinates": data['feature']['geometry']['rings']},
        "properties":
        data['feature']['attributes']
        }
    else:
        geojson = { 
        "type": "Feature",
        "geometry": {
            "type": geom_type,
            "coordinates": [data['feature']['geometry']['x'], 
                data['feature']['geometry']['y']]},
        "properties":
        data['feature']['attributes']
        }

    return geojson 
