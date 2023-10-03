from Autodesk.Revit.DB import *
import clr

clr.AddReference("RevitAPI")
clr.AddReference("System")
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document

columns_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StructuralColumns). \
    WhereElementIsNotElementType(). \
    ToElements()

columns = {}
precast_elements = {}

def getiing_parameters(columns_collector):
    for el in columns_collector:
        col_type_id = el.GetTypeId()
        col_type_elem = doc.GetElement(col_type_id)
        if col_type_elem:
            parameter_Duplication = col_type_elem.LookupParameter("Duplication Type Mark").AsString()
            if parameter_Duplication == "Steel":
                continue

            if parameter_Duplication in ["Rec", "Round", "Eliptic"]:
                parameter_vol = el.LookupParameter("Volume")
                key = "Columns Regular/עמודי בטון"
                if key not in columns:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    columns[key] = {"Volume": parameter_value_vol}
                elif key in columns:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    columns[key]["Volume"] += parameter_value_vol

            if parameter_Duplication == "Precast":
                key_precast = "עמוד טרומי/Columns Precast"
                parameter_vol = el.LookupParameter("Volume")
                if key_precast not in precast_elements:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    precast_elements[key_precast] = {"Volume": parameter_value_vol, "Count": 1}
                elif key_precast in precast_elements:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    precast_elements[key_precast]["Volume"] += parameter_value_vol
                    precast_elements[key_precast]["Count"] += 1

            if not parameter_Duplication:
                key = "DTM empty Columns"
                parameter_vol = el.LookupParameter("Volume")
                if key not in columns:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    columns[key] = {"Volume": parameter_value_vol}
                else:
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    columns[key]["Volume"] += parameter_value_vol



getiing_parameters(columns_collector)