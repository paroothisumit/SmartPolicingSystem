import requests

#returns a dictionary with latitude and longitude of given address
def get_position_coordinates(address):
    geocoding_api_key='AIzaSyBHGIUrn1sEzxi2ws7OOxpnjW2lO6ihVzM'
    response=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={1}&key={0}'.format(geocoding_api_key,address))
    return response.json()['results'][0]['geometry']['location']

#print(get_position_coordinates('G-5, Ground Floor, City Park, Hiranandani Business Park, Hiranandani Gardens, Powai, Mumbai, Maharashtra 400087'))