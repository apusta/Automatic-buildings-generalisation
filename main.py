import argparse
import sys
import os.path
from os import path

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

parser = argparse.ArgumentParser(description='Run generalisation with defined mode')
parser.add_argument('-s', '--scale', type=str, help='Output generalisation scale [10000, 25000]')
parser.add_argument('-m', '--mode', type=str, help='Generalisation mode [typification, union')
parser.add_argument('-f', '--file', type=str, help='Path to input .shp file')
parser.add_argument('-o', '--output_dir', type=str, help='Path to output folder')

args = parser.parse_args()

if args.scale != Scale.SCALE10K and args.scale != Scale.SCALE25K:
    sys.exit("Supported scales are {} or {}".format(Scale.SCALE10K, Scale.SCALE25K))

if args.mode != Mode.UNION and args.mode != Mode.TYPIFICATION:
    sys.exit("Supported modes are typification or union")

if path.isfile(args.file) is False:
    sys.exit("File not exist")

if path.isdir(args.output_dir) is False:
    sys.exit("Output directory not exist")

print("Start processing..")

context = Context(args.scale, args.mode)
# context = Context(Scale.SCALE10K, Mode.UNION)

cache = Cache()

if cache.exists(buildings_cache_name) is False:
    counter = 0
    for building_data in fiona.open(args.file):
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

result.save(args.output_dir)

