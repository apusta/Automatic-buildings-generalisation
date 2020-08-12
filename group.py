from shapely.geometry import Polygon, Point, shape
from shapely.ops import unary_union
from shapely import affinity
import math


class Group:
    def __init__(self, id, buildings):
        self.id = str(id)
        self.buildings = buildings
        self.rotatedRectangle = None
        self.area = None
        self.rotatedRectangleArea = None
        self.polygon = None
        self.scaled = None

    def __eq__(self, other):
        return self.id == other.id

    def add_building(self, building):
        self.buildings.append(building)

    def add_buildings(self, buildings):
        self.buildings.extend(buildings)

    def merge(self, group):
        self.buildings.append(group.buildings)

    def union(self):
        self.polygon = unary_union(list(map(lambda b: b.buffer, self.buildings)))
        return self.polygon

    def is_connected(self, group):
        return self.polygon.intersects(group.polygon)

    def create_rotated_rectangle(self):
        self.rotatedRectangle = self.union().minimum_rotated_rectangle

    def calculate_area(self):
        self.area = sum(list(map(lambda b: b.area, self.buildings)))

    def typification(self):
        self.rotatedRectangleArea = self.rotatedRectangle.area
        factor = math.sqrt(self.area)/math.sqrt(self.rotatedRectangleArea)
        self.scaled = affinity.scale(self.rotatedRectangle, xfact=factor, yfact=factor, origin='center')

    def scale(self):
        self.create_rotated_rectangle()
        self.calculate_area()
        self.typification()

    def get_building_ids_string(self):
        return ' ,'.join(list(map(lambda b: str(b.properties['OBJECTID']), self.buildings)))
