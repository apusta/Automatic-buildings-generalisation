from shapely.geometry import Polygon, Point, shape
import math
import uuid


class Building:

    def __init__(self, properties, polygon, area):

        self.properties = properties
        self.id = str(uuid.uuid4())
        self.type = properties['SRdBdWgKs']
        self.polygon = polygon
        self.bufferForTypification = self.polygon.buffer(0.5)
        self.bufferForUnion = self.polygon.buffer(0.01)
        self.area = area
        self.isRectangle = self.rectangle_check(0.70, 1.30)
        self.signatureRotation = None
        self.groupId = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def rectangle_check(self, min_area_factor, max_area_factor):

        box = self.polygon.minimum_rotated_rectangle
        area_rectangle = box.area
        min_area = min_area_factor * self.area
        max_area = max_area_factor * self.area

        if min_area < area_rectangle < max_area:
            return True
        else:
            return False

    def azimuth_count(self, xp, yp, xk, yk):
        dX = xk - xp
        dY = yk - yp
        azimuth = 0

        if dX == 0 and dY == 0:
            azimuth = 0
        elif dX == 0 and dY > 0:
            azimuth = math.pi / 2
        elif dX == 0 and dY < 0:
            azimuth = (3 / 2) * math.pi
        elif dX > 0 and dY == 0:
            azimuth = 0
        elif dX < 0 and dY == 0:
            azimuth = math.pi
        elif dX != 0 and dY != 0:
            fi = math.atan(abs(dY / dX))
            if dX > 0 and dY > 0:
                azimuth = fi
            elif dX < 0 < dY:
                azimuth = math.pi - fi
            elif dX < 0 and dY < 0:
                azimuth = math.pi + fi
            elif dX > 0 > dY:
                azimuth = 2 * math.pi - fi

        return (azimuth * 180 / math.pi)

    def sygnature_rotation_count(self):

        box = self.polygon.minimum_rotated_rectangle
        x, y = box.exterior.coords.xy

        xk = ((x[1] - x[0]) / 2) + x[0]
        yk = ((y[1] - y[0]) / 2) + y[0]

        centroid_of_box = box.centroid
        xp = centroid_of_box.x
        yp = centroid_of_box.y

        angle = - self.azimuth_count(xp, yp, xk, yk)

        self.signatureRotation = angle

    def is_connected(self, building):
        return self.bufferForTypification.intersects(building.bufferForTypification)

    def is_touching(self, building):
        return self.bufferForUnion.intersects(building.bufferForUnion)

