import fiona
from fiona.crs import from_epsg
from shapely.geometry import Polygon, mapping
from building import Building

buildings = []
buildingsRectangles = []
buildingsNotRectangles = []

#loading data from file and saving it as instances of Building
for building_data in fiona.open('./data/budynki_wybrane.shp'):
    building = Building(
        building_data['properties'],
        Polygon(building_data['geometry']['coordinates'][0]),
        Polygon(building_data['geometry']['coordinates'][0]).area
    )
    buildings.append(building)

for building in buildings:
    if building.isRectangle:
        buildingsRectangles.append(building)
    else:
        buildingsNotRectangles.append(building)

schema = {
    'geometry': 'Polygon',
    'properties': {'OBJECTID': 'int', 'DATA_WPROW': 'str', 'WYSOKOSC': 'str'}
}

# Write a new Shapefile with generalised objects
with fiona.open('./data/generalised_to_rectangle.shp', 'w', 'ESRI Shapefile', schema, crs=from_epsg(2177)) as file:
    for building in buildingsRectangles:
        file.write({
            'geometry': mapping(building.polygon.minimum_rotated_rectangle),
            'properties': {'OBJECTID': building.properties['OBJECTID'], 'DATA_WPROW': building.properties['DATA_WPROW'],
                           'WYSOKOSC': building.properties['WYSOKOSC']},
        })
