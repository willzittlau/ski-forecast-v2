def get_map_coordinates(coordinates):
    lat = coordinates[4:12]
    lon = coordinates[17:]
    map_coordinates = lat + ',' + lon
    src = 'https://maps.google.com/maps?width=100%%25&amp;height=500&amp;hl=en&amp;q=%s&amp;t=p&amp;z=12&amp;ie=UTF8&amp;iwloc=B&amp;output=embed' % map_coordinates
    return src