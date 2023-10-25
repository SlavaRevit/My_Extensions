# -*- coding: utf-8 -*-

__title__ = ""  # Name of the button displayed in Revit UI
__doc__ = ""  # Description of the button displayed in Revit UI
__autor__ = 'Slava Filimonenko'  # Script's autor

import random
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
import os, sys, datetime,clr
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Architecture import *
# pyrevit
from pyrevit import forms, revit, script

clr.AddReference('System')
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument  # type: UIDocument
app = __revit__.Application  # type: Application


def get_selected_elements():
    selected_elements = []
    for e_id in uidoc.Selection.GetElementIds():
        element = doc.GetElement(e_id)
        selected_elements.append(element)

    return selected_elements


result = get_selected_elements()

# use transactions to modify document
t = Transaction(doc, "Change ElementIds")

t.Start()  # Start transaction
for el in result:
    curve_list = List[Curve]()
    curve_list.Add(el.Location.Curve)
    unc_height = el.LookupParameter("Unconnected Height")
    new_wall_id = ElementId(random.randint(50000, 60000))
    new_wall = Wall.Create(doc,
                           curve_list,
                           new_wall_id,
                           el.LevelId,
                           False,
                           curve_list)
    for param in el.Parameters:
        new_wall.get_Parameter(param.Id).Set(param.AsValueString())
    # print("Changed ElementId to {0} for element with Id {1}".format(new_id, el.Id))

# changes here

t.Commit()  # Commit Transaction

# -------------------------------------------------------------------
print('-' * 50)
print("Script is finished")
