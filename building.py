from shapely.geometry import Polygon, Point, shape


class Building:

    def __init__(self, properties, polygon, area):

        self.properties = properties
        self.polygon = polygon
        self.area = area
        self.isRectangle = self.rectangle_check()

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
