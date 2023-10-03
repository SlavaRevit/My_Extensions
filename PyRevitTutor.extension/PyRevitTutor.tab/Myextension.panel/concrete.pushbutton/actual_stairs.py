from Autodesk.Revit.DB import *
import clr

clr.AddReference("RevitAPI")
clr.AddReference("System")
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document

stairs_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Stairs). \
    WhereElementIsNotElementType(). \
    ToElements()

floors_collector_forsteirs = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType(). \
    ToElements()


Stairs = {}
def getiing_parameters_slab_edge(stairs_collector, floors_collector_forsteirs):
    for el in stairs_collector:
        stair_type_id = el.GetTypeId()
        stair_type_elem = doc.GetElement(stair_type_id)
        parameter_Duplication = stair_type_elem.LookupParameter("Duplication Type Mark").AsString()
        if stair_type_elem:
            if parameter_Duplication == "Home" or parameter_Duplication == "Stairway" or parameter_Duplication == "Stairs":
                parameter_vol = el.LookupParameter("Volume")
                key = "Stairs/משטחי מדרגות ישרים (פודסטי ביניים ) ומדרגות מבטון"
                if key not in Stairs:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Stairs[key] = {"Volume": parameter_value_vol}
                elif key in Stairs:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Stairs[key]["Volume"] += parameter_value_vol
            else:
                pass

    for el in floors_collector_forsteirs:
        floor_type_id = el.GetTypeId()
        floor_type_elem = doc.GetElement(floor_type_id)
        parameter_Duplication = floor_type_elem.LookupParameter("Duplication Type Mark").AsString()
        if floor_type_elem:
            if parameter_Duplication == "Landing-H" or parameter_Duplication == "Landing-S":
                parameter_vol = el.LookupParameter("Volume")
                key = "Stairs/משטחי מדרגות ישרים (פודסטי ביניים ) ומדרגות מבטון"
                if key not in Stairs:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Stairs[key] = {"Volume": parameter_value_vol}
                elif key in Stairs:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Stairs[key]["Volume"] += parameter_value_vol


getiing_parameters_slab_edge(stairs_collector, floors_collector_forsteirs)
