# -*- coding: utf-8 -*-

__title__ = ""  # Name of the button displayed in Revit UI
__doc__ = ""  # Description of the button displayed in Revit UI
__autor__ = 'Slava Filimonenko'  # Script's autor

import math
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
import os, sys, datetime
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.DB.Architecture import *
# pyrevit
from pyrevit import forms, revit, script

# .NET Imports
import clr

clr.AddReference('System')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from System.Collections.Generic import List
from pyrevit.forms import WPFWindow

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument  # type: UIDocument
app = __revit__.Application  # type: Application

stairs_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Stairs). \
    WhereElementIsNotElementType(). \
    ToElements()

stair_runs = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StairsRuns). \
    WhereElementIsNotElementType(). \
    ToElements()
runs_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StairsRuns). \
    WhereElementIsNotElementType(). \
    ToElements()

floors_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType(). \
    ToElements()

FloorTypes = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()

floor_to_show = [floor.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() for floor in FloorTypes]
res = forms.SelectFromList.show(floor_to_show, button_name="Select item")

for floor in FloorTypes:
    if floor.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == res:
        floor_type_id = floor.Id


def getting_parameters_for_runs(el):
    # runs element from element id
    runs_element = doc.GetElement(r)
    # getting actual width of  run_width
    runs_width = runs_element.ActualRunWidth
    # params of rises and treads
    runs_actualNumberOfRises = runs_element.LookupParameter("Actual Number of Risers").AsInteger()
    runs_actualNumberOfTreads = runs_element.LookupParameter("Actual Number of Treads").AsInteger()
    run_base_height = runs_element.LookupParameter("Relative Base Height").AsDouble()
    run_top_height = runs_element.LookupParameter("Relative Top Height").AsDouble()
    # getting run params
    r_depth = runs_element.LookupParameter("Actual Tread Depth").AsDouble()
    r_height = runs_element.LookupParameter("Actual Riser Height").AsDouble()
    return runs_element, runs_width, r_depth, r_height, runs_actualNumberOfRises, runs_actualNumberOfTreads, run_base_height, run_top_height


def find_closest_point(point, point_list):
    min_distance = float('inf')
    closest_point = None

    for p in point_list:
        x, y, z = p
        distance = math.sqrt((point[0] - x) ** 2 + (point[1] - y) ** 2 + (point[2] - z) ** 2)

        if distance < min_distance:
            min_distance = distance
            closest_point = p

    return closest_point


t = Transaction(doc, "plaster on runs")
t.Start()

for el in stairs_collector:
    floors_to_enable = []
    coordinates_end = []
    coordinates_start = []
    modified_curves = []
    floor_heights = []
    floor_params = []
    runs = el.GetStairsRuns()
    stairs_level_id = el.LookupParameter("Base Level").AsElementId()
    stairs_base_offset = el.LookupParameter("Base Offset").AsDouble() * 30.48
    count = 0
    run_coordinates_start = []
    for r in runs:

        profile_ceiling = CurveLoop()
        profile = CurveLoop()
        # Create an empty curve loop to build the profile
        runs_element, \
            runs_width, \
            r_depth, \
            r_height, \
            runs_actualNumberOfRises, \
            runs_actualNumberOfTreads, \
            run_base_height, \
            run_top_height = getting_parameters_for_runs(r)

        geometry = runs_element.get_Geometry(Options())
        # getting Footprint Boundaries to get all coordinates of X Y Z
        boundaries_of_run = runs_element.GetFootprintBoundary()
        # for each curve element in the boundaries run we are getting points, and adding it to the list
        biggest_face = None
        area_total = 0
        # param_to_check = runs_element.LookupParameter("Extend Below Riser Base").AsDouble()
        face = None
        for obj in geometry:
            if isinstance(obj, Solid):
                solid = obj
                faces = solid.Faces
                for face in faces:
                    area_of_face = face.Area
                    surface_area = face.Triangulate().ComputeSurfaceArea()
                    if area_of_face > area_total:
                        area_total = face.Area
                        biggest_face = face

        if biggest_face:
            curve_edges_loop = biggest_face.GetEdgesAsCurveLoops()
            normal = biggest_face.FaceNormal
            direction_vector = normal.Normalize()

            for curve_loop in curve_edges_loop:
                curve_iterator = curve_loop.GetCurveLoopIterator()
                modified_loop = CurveLoop()
                for curve_iter in curve_iterator:
                    start = curve_iter.GetEndPoint(0)
                    end = curve_iter.GetEndPoint(1)
                    start = XYZ(start.X, start.Y, start.Z)
                    end = XYZ(end.X, end.Y, end.Z)
                    # Modify the Z-coordinate to be 0
                    modified_start_point = XYZ(start.X, start.Y, 0)
                    modified_end_point = XYZ(end.X, end.Y, 0)

                    coordinates_start.append((start.X, start.Y, start.Z))
                    coordinates_end.append((end.X, end.Y, end.Z))
                    try:
                        modified_curve = Line.CreateBound(modified_start_point, modified_end_point)
                        modified_loop.Append(modified_curve)
                    except Exception as err:
                        print(err)


                modified_curves.append(modified_loop)

    try:
        floor_ceiling = Floor.Create(doc, modified_curves, floor_type_id, stairs_level_id)
        floor_ceiling.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(0)
        floors_to_enable.append(floor_ceiling)
        doc.Regenerate()

    except Exception as ex:
        print(ex)

    # sorted_start = sorted(coordinates_start)
    sorted_start = sorted(coordinates_start, key=lambda vertex: (vertex[0], vertex[1], vertex[2]))

    # sorted_end = sorted(coordinates_end, key=lambda vertex: (vertex[0], vertex[1], vertex[2]))


    def sort_key(vertex):
        return vertex.Position.X, vertex.Position.Y, vertex.Position.Z



    # print("sorted list: ", sorted_start)

    try:
        for floor in floors_to_enable:
            doc.Regenerate()
            slabeditor = floor.SlabShapeEditor
            # Get the slab's vertex array
            # print(len(sorted_start))

            # for i,_ in enumerate(sorted_start):
            #     print("Printing position: {0}".format(i), _)

            slabeditor.Enable()
            doc.Regenerate()
            creasesArray = slabeditor.SlabShapeCreases
            vertexArray = slabeditor.SlabShapeVertices
            sorted_vertex_array = sorted(vertexArray, key=sort_key)
            # print(len(sorted_vertex_array))
            floor_id = floor.LevelId
            elevation = doc.GetElement(floor_id).Elevation
            doc.Regenerate()

            # print(len(sorted_vertex_array))

            for i, vertex in enumerate(sorted_vertex_array):
                x, y, z = vertex.Position.X, vertex.Position.Y, vertex.Position.Z
                x_new, y_new, z_new = sorted_start[i]
                # print("Printing Positions of vertex {0}: ".format(i), x, y, z , z_new)
                pos_check = (x, y, z)
                # if (vertex.Position.X, vertex.Position.Y) == (x_new, y_new):
                #     print("Position is:",i, z_new)
                # else:
                #     print("Doesn't match is", i)
                # print("The position is",i, vertex.Position.X, vertex.Position.Y, vertex.Position.Z, x_new, y_new, z_new)

                # print(closest_point)
                slabeditor.ModifySubElement(vertex, z_new - elevation)
            print("End of floor HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        doc.Regenerate()


    except Exception as ex:
        print(ex)

t.Commit()
