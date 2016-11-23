import getopt
import json
import sys
import urllib.request

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
        '''Given a list of IDs, returns a dictionary {ID : JSON}
        pulled from the server URL.'''

        out = {}
        for num in nums:
            out[num] = self.get_id(num)
        return out

    def get_id(self,num):
        '''Given an integer ID, returns a JSON pulled from the server URL.'''

        if num in self.ids:
            return self.ids[num][0]

        else:
            url = self.url + '/{0}/{1}?f=json&pretty=true'.format(self.layer, num)
            with urllib.request.urlopen(url) as site:
                resp = site.read().decode('utf-8')

            out = json.loads(resp)
            self.ids[num] = (out, False)
            return out

    def convert_id(self,num, geom_type='Polygon'):
        '''Converts given integer ID from JSON to geo-JSON.'''

        data, flag = self.ids[num]
        if not flag:
            self.ids[num] = (to_geojson(data, geom_type=geom_type), True)
        return None

    def convert_all(self,geom_type='Polygon'):
        '''Converts all queried IDs from JSON to geo-JSON.'''

        for num in self.ids:
            self.convert_id(num, geom_type=geom_type)

        return None

    def save_all(self, loc):
        '''Given a directory location (string), saves all queried IDs
        as JSON files to that directory.'''

        if loc[-1] != '/':
            loc += '/'

        for num,data in self.ids.items():
            with open(loc + '{}.json'.format(num), 'w') as f:
                json.dump(data,f)

    def __init__(self, base_url, layer=0):
        self.url = base_url
        self.layer = layer
        self.ids = {}

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

def main():
    return None

if __name__=='__main__':
    main()
