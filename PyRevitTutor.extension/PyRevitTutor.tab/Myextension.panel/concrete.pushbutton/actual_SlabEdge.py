from Autodesk.Revit.DB import *
import clr

clr.AddReference("RevitAPI")
clr.AddReference("System")
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document

slab_edge_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_EdgeSlab). \
    WhereElementIsNotElementType(). \
    ToElements()

Slabedge = {}

def getiing_parameters_slab_edge(slab_edge_collector):
    for el in slab_edge_collector:
        edge_type_id = el.GetTypeId()
        edge_type_elem = doc.GetElement(edge_type_id)
        parameter_Duplication = edge_type_elem.LookupParameter("Duplication Type Mark").AsString()
        if edge_type_elem:
            if not parameter_Duplication:
                parameter_vol = el.LookupParameter("Volume")
                parameter_length = el.LookupParameter("Length")
                key_slab_edge = "no DTM Slab edge"
                if key_slab_edge not in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[key_slab_edge] = {"Volume": parameter_value_vol, "Length": parameter_length}
                elif key_slab_edge in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[key_slab_edge]["Volume"] += parameter_value_vol
                    Slabedge[key_slab_edge]["Length"] += parameter_length
            elif parameter_Duplication == "Wuta":
                parameter_vol = el.LookupParameter("Volume")
                parameter_length = el.LookupParameter("Length")
                if parameter_Duplication not in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[parameter_Duplication] = {"Volume": parameter_value_vol, "Length": parameter_length}
                elif parameter_Duplication in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[parameter_Duplication]["Volume"] += parameter_value_vol
                    Slabedge[parameter_Duplication]["Length"] += parameter_length
            else:
                parameter_vol = el.LookupParameter("Volume")
                parameter_length = el.LookupParameter("Length")
                if parameter_Duplication not in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[parameter_Duplication] = {"Volume": parameter_value_vol, "Length": parameter_length}
                elif parameter_Duplication in Slabedge:
                    parameter_length = parameter_length.AsDouble() * 0.3048
                    parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                    Slabedge[parameter_Duplication]["Volume"] += parameter_value_vol
                    Slabedge[parameter_Duplication]["Length"] += parameter_length


getiing_parameters_slab_edge(slab_edge_collector)