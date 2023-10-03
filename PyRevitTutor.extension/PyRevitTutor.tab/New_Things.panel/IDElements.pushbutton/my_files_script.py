#! python3

import sys
import os
import clr
import sys

from  Autodesk.Revit.UI import TaskDialog, TaskDialogResult


import System
from System import Array
from System.Collections.Generic import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document

"""________FLOORS________"""
floors_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType(). \
    ToElements()


initial_lengths = []
thickness_lengths = []
total_lengths = []
script_run_count = 0

my_script_run = False
if not my_script_run and script_run_count == 0:
    for floor_element in floors_collector:
        floor_type = floor_element.FloorType
        floor_type_comments = floor_type.LookupParameter("Classification.Uniclass.Ss.Number").AsString()
        floor_thickness = floor_element.LookupParameter("Thickness").AsValueString()

        if floor_type_comments and floor_thickness:
            initial_length = len(floor_type_comments)
            thickness_length = len(floor_thickness)
            total_length = initial_length + thickness_length + 1  # +1 for the dot separator

            initial_lengths.append(initial_length)
            thickness_lengths.append(thickness_length)
            total_lengths.append(total_length)


print(initial_lengths)
print(total_lengths)

def getClassificationNumber(floors_collector,script_run):
    global initial_length, thickness_length, total_length, script_run_count

    script_run_count += 1

    unique_floor_types = set()
    for i,floor_element in enumerate(floors_collector):
        # floor_element = doc.GetElement(el)
        floor_type = floor_element.FloorType
        if floor_type.Id not in unique_floor_types: # Check if floor type is unique
            unique_floor_types.add(floor_type.Id) # Add floor type to set

            floor_type_comments = floor_type.LookupParameter("Classification.Uniclass.Ss.Number").AsString()
            floor_thickness = floor_element.LookupParameter("Thickness").AsValueString()

            if floor_type_comments and floor_thickness:
                if script_run_count > 1 and total_lengths[i] > initial_lengths[i]:
                    continue

                new_ID = f'{floor_type_comments}.{floor_thickness}'

                # if floor_type_comments != new_ID:
                t = Transaction(doc, "Set Floor Type Classification ID")
                t.Start()
                floor_type_comments_to_set = floor_type.LookupParameter("Classification.Uniclass.Ss.Number")
                floor_type_comments_to_set.Set(new_ID)
                t.Commit()

                print("Thickness added.")

    return True


has_script_run = getClassificationNumber(floors_collector, my_script_run)
print("Script Run State:", has_script_run)
print(initial_lengths)
print(total_lengths)
