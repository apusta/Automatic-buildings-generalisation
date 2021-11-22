import fiona
from fiona.crs import from_epsg
from shapely.geometry import Polygon, mapping

class Results:
    _SCHEMA = {
        'geometry': 'Polygon',
        'properties': {'ID': 'int', 'TRdBdWgKs': 'str', 'SRdBdWgKs': 'int'}
    }
    _RECTANGLE_SCHEMA = {
        'geometry': 'Polygon',
        'properties': {'ID': 'int', 'TRdBdWgKs': 'str', 'SRdBdWgKs': 'int', 'groupID': 'str'}
    }
    _SIGNATURE_SCHEMA = {
        'geometry': 'Point',
        'properties': {'ID': 'int', 'TRdBdWgKs': 'str', 'SRdBdWgKs': 'int', 'ROTACJA': 'float'}
    }
    _GROUP_SCHEMA = {
        'geometry': 'Polygon',
        'properties': {'GROUPID': 'str', 'BUILDING_ID': 'str', 'AREA': 'float', 'SRdBdWgKs': 'int'}
    }

    def __init__(self,
                 eliminated_buildings=None,
                 rectangelized_buildings=None,
                 for_manual_revision_buildings=None,
                 signatured_buildings=None,
                 unioned_groups=None,
                 typificated_groups=None):
        self.eliminated_buildings = eliminated_buildings
        self.rectangelized_buildings = rectangelized_buildings
        self.for_manual_revision_buildings = for_manual_revision_buildings
        self.signatured_buildings = signatured_buildings
        self.unioned_groups = unioned_groups
        self.typificated_groups = typificated_groups

    def save(self, output_folder):
        if self.eliminated_buildings:
            with fiona.open(output_folder + '/eliminated.shp', 'w', 'ESRI Shapefile', self._SCHEMA, crs=from_epsg(2177)) as file:
                for building in self.eliminated_buildings:
                    file.write({
                        'geometry': mapping(building.polygon),
                        'properties': {'ID': building.properties['ID'], 'TRdBdWgKs': building.properties['TRdBdWgKs'],
                                       'SRdBdWgKs': building.type},
                    })
        if self.rectangelized_buildings:
            with fiona.open(output_folder + '/generalised_to_rectangle.shp', 'w', 'ESRI Shapefile', self._RECTANGLE_SCHEMA,
                            crs=from_epsg(2177)) as file:
                for building in self.rectangelized_buildings:
                    file.write({
                        'geometry': mapping(building.polygon.minimum_rotated_rectangle),
                        'properties': {'ID': building.properties['ID'], 'TRdBdWgKs': building.properties['TRdBdWgKs'],
                                       'SRdBdWgKs': building.type, 'groupID': building.groupId},
                    })
        if self.for_manual_revision_buildings:
            with fiona.open(output_folder + '/notGeneralised.shp', 'w', 'ESRI Shapefile', self._SCHEMA,
                            crs=from_epsg(2177)) as file:
                for building in self.for_manual_revision_buildings:
                    file.write({
                        'geometry': mapping(building.polygon),
                        'properties': {'ID': building.properties['ID'], 'TRdBdWgKs': building.properties['TRdBdWgKs'],
                                       'SRdBdWgKs': building.type},
                    })
        if self.signatured_buildings:
            with fiona.open(output_folder + '/generalised_to_signature.shp', 'w', 'ESRI Shapefile', self._SIGNATURE_SCHEMA,
                            crs=from_epsg(2177)) as file:
                for building in self.signatured_buildings:
                    file.write({
                        'geometry': mapping(building.polygon.centroid),
                        'properties': {'ID': building.properties['ID'], 'TRdBdWgKs': building.properties['TRdBdWgKs'],
                                       'SRdBdWgKs': building.type, 'ROTACJA': building.signatureRotation},
                    })
        if self.unioned_groups:
            with fiona.open(output_folder + '/union.shp', 'w', 'ESRI Shapefile', self._GROUP_SCHEMA, crs=from_epsg(2177)) as file:
                for group in self.unioned_groups:
                    file.write({
                        'geometry': mapping(group.unioned),
                        'properties': {'GROUPID': group.id, 'BUILDING_ID': group.get_building_ids_string(), 'AREA': group.area, 'SRdBdWgKs': group.type},
                    })
        if self.typificated_groups:
            with fiona.open(output_folder + '/typificated.shp', 'w', 'ESRI Shapefile', self._GROUP_SCHEMA, crs=from_epsg(2177)) as file:
                for group in self.typificated_groups:
                    file.write({
                        'geometry': mapping(group.typificated),
                        'properties': {'GROUPID': group.id, 'BUILDING_ID': group.get_building_ids_string(), 'AREA': group.area, 'SRdBdWgKs': group.type},
                    })