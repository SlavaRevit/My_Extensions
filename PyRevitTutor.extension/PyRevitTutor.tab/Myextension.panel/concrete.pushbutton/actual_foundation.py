from Autodesk.Revit.DB import *
import clr
import unicodedata

clr.AddReference("RevitAPI")
clr.AddReference("System")
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document

foundation_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StructuralFoundation). \
    WhereElementIsNotElementType(). \
    ToElements()


# def getting_Area(found_list, found_type_check):
#     total_Area = 0.0
#     for el in found_list:
#         foundation_element = doc.GetElement(el)
#         foundation_type = foundation_element.FloorType
#         # floor_type_comments = foundation_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsString()
#         if foundation_type:
#             foundation_duplicationTypeMark = foundation_type.LookupParameter("Duplication Type Mark").AsString()
#             for type_el in found_type_check:
#                 if foundation_duplicationTypeMark == type_el:
#                     if foundation_duplicationTypeMark:
#                         foundation_area = foundation_element.LookupParameter("Area").AsDouble()
#                         total_Area = total_Area + foundation_area * 0.092903
#     return total_Area


Dipuns = {}
Bisus = {}
Basic_Plate = {}
Found_Head = {}
Rafsody = {}
Found_without_DTM = {}

def getting_Length_Volume_Count(found_list):
    for el in found_list:
        if el.Category.Name == "Structural Foundations":
            if isinstance(el, FamilyInstance):
                el_type_id = el.GetTypeId()
                type_elem = doc.GetElement(el_type_id)
                if type_elem:
                    parameter_Duplication = type_elem.LookupParameter("Duplication Type Mark").AsString()
                    if not parameter_Duplication:
                        parameter = el.LookupParameter("Length")
                        parameter_vol = el.LookupParameter("Volume")
                        parameter_Descr = type_elem.LookupParameter("Description").AsValueString()
                        key = "DTM empty Foundation"
                        if key not in Dipuns:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Found_without_DTM[key] = {'Length': parameter_value, 'Volume': parameter_value_vol,
                                                      'Count': 1}
                        else:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Found_without_DTM[key]['Length'] += parameter_value
                            Found_without_DTM[key]['Volume'] += parameter_value_vol
                            Found_without_DTM[key]['Count'] += 1

                    if parameter_Duplication == "Dipun":
                        parameter = el.LookupParameter("Length")
                        parameter_vol = el.LookupParameter("Volume")
                        parameter_Descr = type_elem.LookupParameter("Description").AsValueString()
                        if parameter_Descr not in Dipuns:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Dipuns[parameter_Descr] = {'Length': parameter_value, 'Volume': parameter_value_vol,
                                                       'Count': 1}
                        else:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Dipuns[parameter_Descr]['Length'] += parameter_value
                            Dipuns[parameter_Descr]['Volume'] += parameter_value_vol
                            Dipuns[parameter_Descr]['Count'] += 1


                    elif parameter_Duplication == "Bisus":
                        parameter = el.LookupParameter("Length")
                        parameter_vol = el.LookupParameter("Volume")
                        parameter_Descr = type_elem.LookupParameter("Description").AsValueString()

                        if parameter_Descr not in Bisus:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Bisus[parameter_Descr] = {'Length': parameter_value, 'Volume': parameter_value_vol,
                                                      'Count': 1}
                        else:
                            parameter_value = parameter.AsDouble() * 0.3048
                            parameter_value_vol = parameter_vol.AsDouble() * 0.0283168466
                            Bisus[parameter_Descr]['Length'] += parameter_value
                            Bisus[parameter_Descr]['Volume'] += parameter_value_vol
                            Bisus[parameter_Descr]['Count'] += 1

            # For Floor Types ( Rafsody, Head, BasicPlate )
            elif isinstance(el, Floor):
                el_type_id = el.GetTypeId()
                # foundation_element = doc.GetElement(el)
                foundation_type = el.FloorType
                foundation_duplicationTypeMark = foundation_type.LookupParameter("Duplication Type Mark").AsString()
                if foundation_duplicationTypeMark == "Rafsody":
                    key = "Rafsody/רפסודה"
                    if key not in Rafsody:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Rafsody[key] = {"Area": foundation_area, "Volume": foundation_volume}
                    else:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Rafsody[key]["Area"] += foundation_area
                        Rafsody[key]["Volume"] += foundation_volume

                elif foundation_duplicationTypeMark == "Basic Plate":
                    key = "Basic Plate/פלטות יסוד"
                    if key not in Basic_Plate:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Basic_Plate[key] = {"Area": foundation_area,
                                            "Volume": foundation_volume}
                    else:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Basic_Plate[key]["Area"] += foundation_area
                        Basic_Plate[key]["Volume"] += foundation_volume
                elif foundation_duplicationTypeMark == "Head":
                    key = "Foundation Head/ראשי כלונס"
                    if key not in Found_Head:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Found_Head[key] = {"Area": foundation_area, "Volume": foundation_volume}
                    else:
                        foundation_area = el.LookupParameter("Area").AsDouble() * 0.092903
                        foundation_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                        Found_Head[key]["Area"] += foundation_area
                        Found_Head[key]["Volume"] += foundation_volume

    return Dipuns, Bisus, Rafsody, Basic_Plate, Found_Head, Found_without_DTM


getting_Length_Volume_Count(foundation_collector)


# def getting_Volume(found_list, found_type_check):
#     total_Volume = 0.0
#     for el in found_list:
#         foundation_element = doc.GetElement(el)
#         foundation_type = foundation_element.FloorType
#         # floor_type_comments = foundation_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsString()
#         foundation_duplicationTypeMark = foundation_type.LookupParameter("Duplication Type Mark").AsString()
#         for type_el in found_type_check:
#             if foundation_duplicationTypeMark == type_el:
#                 foundation_volume = foundation_element.LookupParameter("Volume").AsDouble()
#                 total_Volume = total_Volume + foundation_volume * 0.0283168466
#     return total_Volume


# def check_Area_for_zero(result, found_type_check):
#     if result == 0:
#         pass
#     else:
#         for type in found_type_check:
#             result_of_beams_vol = 0
#             str_check = ", ".join(found_type_check)
#             # res_of_beams = res_of_beams + result
#         if len(found_type_check) > 1:
#             area = 0
#             for p in found_type_check:
#                 total_a = getting_Area(foundation_collector, [p])
#                 area = area + total_a
#             return area
#         elif len(found_type_check) == 1:
#             area = getting_Area(foundation_collector, [type])
#             return area
#
#
# def check_Volume_for_zero(result, found_type_check):
#     if result == 0:
#         pass
#     else:
#         for type in found_type_check:
#             result_of_beams_vol = 0
#             str_check = ", ".join(found_type_check)
#             # res_of_beams = res_of_beams + result
#         if len(found_type_check) > 1:
#             volume = 0
#             for p in found_type_check:
#                 total_v = getting_Volume(foundation_collector, [p])
#                 volume = volume + total_v
#             return volume
#         elif len(found_type_check) == 1:
#             volume = getting_Volume(foundation_collector, [type])
#             return volume


"""________Foundation________"""

# foundation_Area = {
#     "Rafsody" : check_Area_for_zero(getting_Area(foundation_collector, ["Rafsody"]),["Rafsody"]),
#     "Basic Plate" : check_Area_for_zero(getting_Area(foundation_collector, ["Basic Plate"]),["Basic Plate"]),
#     "Foundation Head" : check_Area_for_zero(getting_Area(foundation_collector, ["Head"]),["Head"])
# }
#
# foundation_Volume = {
#     "Rafsody" : check_Volume_for_zero(getting_Volume(foundation_collector, ["Rafsody"]),["Rafsody"]),
#     "Basic Plate" : check_Volume_for_zero(getting_Volume(foundation_collector, ["Basic Plate"]),["Basic Plate"]),
#     "Foundation Head" : check_Volume_for_zero(getting_Volume(foundation_collector, ["Head"]),["Head"])
# }


