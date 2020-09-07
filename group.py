from shapely.geometry import Polygon, Point, shape
from shapely.ops import unary_union
from shapely import affinity
import uuid

import math


class Group:
    def __init__(self, buildings):
        self.id = str(uuid.uuid4())
        self.buildings = buildings
        self.area = None
        self.typificated = None
        self.unioned = None
        self.type = None

    def __eq__(self, other):
        return self.id == other.id

    def add_building(self, building):
        self.buildings.append(building)

    def add_buildings(self, buildings):
        self.buildings.extend(buildings)

    def merge(self, group):
        self.buildings.append(group.buildings)


    def typification(self):
        self.area = sum(list(map(lambda b: b.area, self.buildings)))
        polygon_for_typification = unary_union(list(map(lambda b: b.bufferForTypification, self.buildings)))
        rotated_rectangle = polygon_for_typification.minimum_rotated_rectangle
        factor = math.sqrt(self.area) / math.sqrt(rotated_rectangle.area)
        self.typificated = affinity.scale(rotated_rectangle, xfact=factor, yfact=factor, origin='center')

    def get_building_ids_string(self):
        return ' ,'.join(list(map(lambda b: str(b.id), self.buildings)))

    def union(self):
        unioned = unary_union(list(
            map(lambda b: b.polygon if not b.isRectangle else b.polygon.minimum_rotated_rectangle, self.buildings)))
        if unioned.geom_type == 'MultiPolygon':
            unioned = unary_union([Polygon(component.exterior).buffer(0.01) for component
                                          in unioned])
            self.unioned = unioned.buffer((-0.01))
        else:
            self.unioned = unioned.buffer(0.01).buffer(-0.01)

    @property
    def error_group_type(self):
        return -1

    def set_type(self):
        temp_type = self.buildings[0].type
        for i in range(1, len(self.buildings)):
            building = self.buildings[i]

            if temp_type and building.type in [10, 3, 0]:
                continue
            if building.type not in [10, 3, 0]:
                if temp_type in [10, 3, 0]:
                    temp_type = building.type
                elif temp_type != building.type:
                    self.type = self.error_group_type
                    return

        self.type = temp_type
