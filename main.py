import fiona
from fiona.crs import from_epsg
from shapely.geometry import Polygon, mapping
from building import Building
from grouper import Grouper
from group import Group
from cache import Cache
from context import Context, Scale, Mode
from generalisation_helpers import GeneralisationHelpers
from generalise10k import Generalise10k
from generalise25k import Generalise25k

buildings = []
buildings_cache_name = 'buildings'
groupsDict = {}
groups_dict_cache_name = 'groups'

buildingsNotConnected = []
buildingsEliminated = []
buildingsRectangles = []
buildingsSignature = []
buildingsForManualGeneralisation =[]
groupTipificated = []
groupUnioned = []

context = Context(Scale.SCALE10K, Mode.UNION)

cache = Cache()

if cache.exists(buildings_cache_name) is False:
    # loading data from file and saving it as instances of Building
    counter = 0
    for building_data in fiona.open('./data_egib/_budynki_wybrane_luzne.shp'):
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
    groupsDict = Grouper.run(buildings, context)
    cache.save(groups_dict_cache_name, groupsDict)
    cache.save(buildings_cache_name, buildings)
else:
    print('Loaded ' + groups_dict_cache_name + ' from cache')
    groupsDict = cache.load(groups_dict_cache_name)

valid_groups, not_valid_groups = GeneralisationHelpers.validate_groups(groupsDict)

result = None

if context.scale == Scale.SCALE10K:
    generalisator = Generalise10k(context, buildings, valid_groups)
    result = generalisator.run()
elif context.scale == Scale.SCALE25K:
    generalisator = Generalise25k(context, buildings, valid_groups)
    result = generalisator.run()

result.save()

