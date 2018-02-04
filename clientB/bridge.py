import requests


# original
def get_client_info(id,server_address):
    response = requests.post(server_address + 'get_site_info', json={'site_id': id})
    return response.json()

# dummy
# def get_client_info(id,server_address):
#     ret = dict()
#     ret["description"] = "it is a description"
#     ret["contact"] = "saar2119@gmail.com"
#     ret["address"] = "Room no 55, Tilak, MNNIT"
#     return ret