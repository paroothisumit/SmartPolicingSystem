from connection_manager import DB
import geolocation_utility as gu


def check_if_id_exists(table_name, id):
    query_string = 'Select * from ' + table_name + ' where id=%s'
    result_set = DB().query(query_string, [id, ])
    if result_set.rowcount == 1:
        return True
    return False


def get_site_info(id):
    all_data = fetch_settings(id)
    if all_data is None:
        return None

    info = {'description': all_data['description'],
            'contact': all_data['contact'], 'address': all_data['address']}
    return info


def register_clienta(client_info):
    print('Registering clienta')
    client_id = client_info['site_id']
    address = client_info['address']
    description = client_info['description']
    contact = client_info['contact']
    nearest_node = client_info['nearest_node']
    is_prohibited = client_info['is_prohibited']
    position = gu.get_position_coordinates(address)

    q = 'INSERT INTO ClientA (ID,Description,Address,Contact,' \
        'NearestNode,IsProhibited,Latitude,Longitude) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    DB().query(q, (client_id, description, address, contact,
                   nearest_node, is_prohibited, position['lat'], position['lng']))
    return None


def fetch_settings(site_id):
    query_string = 'Select * from ClientA where ID=%s'
    db_obj = DB()
    result_set = db_obj.query(query_string, (site_id,))
    if result_set.rowcount == 0:
        return None
    #TODO:more columns have been added
    id, description, address, contact, nearest_node, is_prohibited = result_set.fetchone()
    config_settings = {'site_id': id, 'description': description, 'address': address,
                       'contact': contact, 'nearest_node': nearest_node,
                       'isProhibited': is_prohibited}
    return config_settings


def register_clientb(client_info):
    print('Registering clientb')
    client_id = client_info['site_id']
    address = client_info['address']
    description = client_info['description']
    contact = client_info['contact']
    q = 'INSERT INTO ClientB (ID,Description,Address,Contact) values(%s,%s,%s,%s)'
    DB().query(q, (client_id, address, description, contact))
    return None


def store_new_alert(siteid, activity_recognized, cctv_location, time):
    print('recieved new alert from ' + str(siteid) + 'at ' + time)
    query_string = 'Select NearestNode,Description,Address from ClientA where ID=%s'
    db_obj = DB()
    result_set = db_obj.query(query_string, (siteid,))
    nearest_node, description, address = result_set.fetchone()
    description = cctv_location + ' ' + description

    query_string = 'Insert into Messages (SourceID,DestinationID,Time,Activity_Recognized,' \
                   'Location_Description,Location_Address) values(%s,%s,%s,%s,%s,%s)'

    DB().query(query_string, (siteid, 1, time, activity_recognized, description, address))
    DB().query(query_string,
               (siteid, nearest_node, time, activity_recognized, description, address))


def check_new_alerts(site_id, last_checked):
    query_string = 'Select * from Messages where DestinationID=%s and Time>%s'
    db_obj = DB()
    result_set = db_obj.query(query_string, (site_id, last_checked))
    message_list = []
    for (source_id, destination_id, time, location_description, activity_recognized,
            location_address) \
            in result_set:
        new_message = {'SourceID': source_id,
                       'DestinationID': destination_id,
                       'Time': time,
                       'activity_recognized': activity_recognized,
                       'location_description': location_description,
                       'location_address': location_address}
        message_list.append(new_message)

    #print(message_list)
    return message_list


def get_all_surveillance_sites():
    query_string = 'Select * from Clienta '
    db_obj = DB()
    result_set = db_obj.query(query_string, ())
    site_list = []
    for (id, nearest_node, description, address, contact, is_prohibited, latitude,
         longitude) in result_set:
        client_info = {'id': id,
                       'description': description,
                       'address': address,
                       'contact': contact,
                       'is_prohibited': is_prohibited,
                       'latitude': latitude,
                       'longitude': longitude};
        site_list.append(client_info)

    return site_list