from shapely.geometry import Polygon, Point, shape
import math

class Building:

    def __init__(self, properties, polygon, area):

        self.properties = properties
        self.polygon = polygon
        self.buffer = self.polygon.buffer(0.5)
        self.area = area
        self.isRectangle = self.rectangle_check()
        self.signatureRotation = self.sygnature_check()
        self.groupId = None


    def __eq__(self, other):
        return self.properties['OBJECTID'] == other.properties['OBJECTID']

    def __hash__(self):
        return hash(self.properties['OBJECTID'])

    def rectangle_check(self):
        # get minimum bounding box around polygon
        box = self.polygon.minimum_rotated_rectangle

        # get coordinates of polygon vertices
        x, y = box.exterior.coords.xy

        # get length of bounding box edges
        edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))

        # get length of polygon as the longest edge of the bounding box
        length = max(edge_length)

        # get width of polygon as the shortest edge of the bounding box
        width = min(edge_length)

        areaRectangle = length * width

        minArea = 0.95 * self.area
        maxArea = 1.05 * self.area

        if minArea < areaRectangle < maxArea:
            return True
        else:
            return False

    def azimuthCount(self, xpp, ypp, xkk, ykk):
        dX = xkk - xpp
        dY = ykk - ypp
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

        return (azimuth*180/math.pi)


    def sygnature_check(self):
        if self.area > 500:
            return None

        box = self.polygon.minimum_rotated_rectangle
        x, y = box.exterior.coords.xy

        # Point in the middle of the edge
        xkk = ((x[1]-x[0])/2)+x[0]
        ykk = ((y[1]-y[0])/2)+y[0]

        centroidOfBox = box.centroid
        xpp = centroidOfBox.x
        ypp = centroidOfBox.y

        angle = - self.azimuthCount(xpp, ypp, xkk, ykk)

        return angle

    def isConnected(self, building):
        return self.buffer.intersects(building.buffer)








