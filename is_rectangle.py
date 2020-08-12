import fiona
from fiona.crs import from_epsg
from shapely.geometry import Polygon, mapping
from building import Building
from grouper import Grouper
from group import Group
from cache import Cache

buildings = []
buildings_cache_name = 'buildings'
groupsDict = {}
groups_dict_cache_name = 'groups'

buildingsRectangles = []
buildingsNotRectangles = []
buildingsSignature = []
buildingsNotSignature = []
buildingsConnected = []
buildingsNotConnected = []

cache = Cache()

if cache.exists(buildings_cache_name) is False:
    # loading data from file and saving it as instances of Building
    counter = 0
    for building_data in fiona.open('./data/budynki_wybrane.shp'):
        # if counter > 1000:
        #     break
        # counter += 1
        building = Building(
            building_data['properties'],
            Polygon(building_data['geometry']['coordinates'][0]),
            Polygon(building_data['geometry']['coordinates'][0]).area
        )
        buildings.append(building)
    cache.save(buildings_cache_name, buildings)
else:
    print('Loaded ' + buildings_cache_name + ' from cache')
    buildings = cache.load(buildings_cache_name)

if cache.exists(groups_dict_cache_name) is False:
    groupsDict = Grouper.run(buildings)
    cache.save(groups_dict_cache_name, groupsDict)
else:
    print('Loaded ' + groups_dict_cache_name + ' from cache')
    groupsDict = cache.load(groups_dict_cache_name)

for group in groupsDict.values():
    group.scale()

schema = {
    'geometry': 'Polygon',
    'properties': {'OBJECTID': 'int', 'DATA_WPROW': 'str', 'WYSOKOSC': 'str'}
}

# for building in buildings:
#     if building.isRectangle:
#         buildingsRectangles.append(building)
#     else:
#         buildingsNotRectangles.append(building)

# # Write a new Shapefile with generalised objects to rectangles
# with fiona.open('./data/generalised_to_rectangle.shp', 'w', 'ESRI Shapefile', schema, crs=from_epsg(2177)) as file:
#     for building in buildingsRectangles:
#         file.write({
#             'geometry': mapping(building.polygon.minimum_rotated_rectangle),
#             'properties': {'OBJECTID': building.properties['OBJECTID'], 'DATA_WPROW': building.properties['DATA_WPROW'],
#                            'WYSOKOSC': building.properties['WYSOKOSC']},
#         })

# # Write a new Shapefile with generalised objects with Douglas_Peucker alghorithm
# with fiona.open('./data/generalised_by_DPa.shp', 'w', 'ESRI Shapefile', schema, crs=from_epsg(2177)) as file:
#     for building in buildingsNotRectangles:
#         file.write({
#             'geometry': mapping(building.polygon.simplify(0.8, preserve_topology=True)),
#             'properties': {'OBJECTID': building.properties['OBJECTID'], 'DATA_WPROW': building.properties['DATA_WPROW'],
#                            'WYSOKOSC': building.properties['WYSOKOSC']},
#         })


# for building in buildings:
#     if building.signatureRotation is None:
#         buildingsNotSignature.append(building)
#     else:
#         buildingsSignature.append(building)

# schemaSignature = {
#     'geometry': 'Point',
#     'properties': {'OBJECTID': 'int', 'DATA_WPROW': 'str', 'WYSOKOSC': 'str', 'ROTACJA': 'float'}
# }

# # Write a new Shapefile with generalised objects to signature
# with fiona.open('./data/minus_generalised_to_signature.shp', 'w', 'ESRI Shapefile', schemaSignature,
#                 crs=from_epsg(2177)) as file:
#     for building in buildingsSignature:
#         file.write({
#             'geometry': mapping(building.polygon.centroid),
#             'properties': {'OBJECTID': building.properties['OBJECTID'], 'DATA_WPROW': building.properties['DATA_WPROW'],
#                            'WYSOKOSC': building.properties['WYSOKOSC'], 'ROTACJA': building.signatureRotation},
#         })

schemaGroups = {
    'geometry': 'Polygon',
    'properties': {'GROUPID': 'str', 'BUILDING_ID': 'str', 'AREA': 'float', 'RTAREA': 'float'}
}

# Write a new Shapefile with typificated groups
with fiona.open('./data/typificated11.shp', 'w', 'ESRI Shapefile', schemaGroups, crs=from_epsg(2177)) as file:
    for group in groupsDict.values():
        file.write({
            'geometry': mapping(group.scaled),
            'properties': {'GROUPID': group.id, 'BUILDING_ID': group.get_building_ids_string(), 'AREA': group.area, 'RTAREA': group.rotatedRectangleArea},
        })
