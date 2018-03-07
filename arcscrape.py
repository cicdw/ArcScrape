import json
import requests


BASE_URL = '''https://**/**/MapServer/0/query'''
params = {
          'text': None,
#         'where': '1=1',
#          'objectIds': 2273,
          'time': None,
          'geometry': None,
          'geometryType': 'esriGeometryEnvelope',
          'inSR': None,
          'spatialRel': 'esriSpatialRelIntersects',
          'relationParam': None,
          'outFields': '*',
          'returnGeometry': 'true',
          'returnTrueCurves': 'false',
          'maxAllowableOffset': None,
          'geometryPrecision': None,
          'outSR': None,
          'returnIdsOnly': 'false',
          'returnCountOnly': 'false',
          'orderByFields': None,
          'groupByFieldsForStatistics': None,
          'outStatistics': None,
          'returnZ': 'false',
          'returnM': 'false',
          'gdbVersion': None,
          'returnDistinctValues': 'false',
          'resultOffset': None,
          'resultRecordCount': None,
          'queryByDistance': None,
          'returnExtentsOnly': 'false',
          'datumTransformation': None,
          'parameterValues': None,
          'rangeValues': None,
          'f': 'pjson'}


def get_json_data(**kwargs):
    '''Given specific kwargs to update params dict with, querys the MapServer
    and converts the resulting request into a dictionary.'''
    new_params = params.copy()
    for key, value in kwargs.items():
        new_params[key] = value
    web_data = requests.get(BASE_URL, params=new_params)
    if web_data.ok:
        return json.loads(web_data.text)
    else:
        raise ValueError('{} resulted in a bad web request.'.format(kwargs))


def to_geojson(data):
    '''Given a dictionary, formats the data into a standard geojson polygon format'''
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": 'Polygon',
            "coordinates": data['features'][0]['geometry']['rings']},
        "properties":
        data['features'][0]['attributes']
    }

    return geojson


def get_all_object_ids():
    '''Retrieves all available object IDs from the MapServer, and returns them
    as a list of integers'''
    object_ids = get_json_data(returnIdsOnly='true', returnGeometry='false', objectIds=None, where='1=1')
    ids = []
    for oid in object_ids['objectIds']:
        ids.append(int(oid))
    return ids


def main():
    oids = get_all_object_ids()
    for oid in oids:
        data = to_geojson(get_json_data(objectIds=oid))
        with open('{}.json'.format(oid), 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
