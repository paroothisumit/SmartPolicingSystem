import requests


# original
def get_client_info(id,server_address):
    response = requests.post(server_address + 'get_site_info', json={'site_id': id})
    return response.json()

def get_all_surveillance_sites(server_address):
    print('Getting information for all surveillance sites')
    response=requests.get(server_address+'get_all_surveillance_sites');
    #print(response)
    #print(response.json())
    return response.json()
