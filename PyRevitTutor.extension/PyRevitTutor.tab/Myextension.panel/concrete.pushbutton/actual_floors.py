from Autodesk.Revit.DB import *
import clr

clr.AddReference("RevitAPI")
clr.AddReference("System")
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document

floors_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_Floors). \
    WhereElementIsNotElementType(). \
    ToElementIds()

floors_up = {}
floors_down = {}


def getting_floors_parameters(floor_list):
    for el in floor_list:
        floor_element = doc.GetElement(el)
        floor_type = floor_element.FloorType
        floor_type_comments = floor_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS).AsString()
        floor_duplicationTypeMark = floor_type.LookupParameter("Duplication Type Mark").AsString()
        if floor_type_comments == "Up":
            if not floor_duplicationTypeMark:
                key = "DTM empty Up_floors"
                if key not in floors_up:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark in ["Total Floor Area", "Total Floor Area Commercial",
                                               "Total Floor Area LSP",
                                               "Total Floor Area Pergola",
                                               "Air Double Level", "Air Elevator", "Air Pergola Aluminium",
                                               "Air Pergola Steel", "Air Pergola Wood", "Air Regular", "Air Stairs",
                                               "Landing-H", "Landing-S", "Landing Steel", "Polivid", "Backfilling","Aggregate"]:
                continue
            elif floor_duplicationTypeMark in ["Regular", "Balcon", "Regular-T"]:
                combined_key = "Regular_up/תקרת בטון"
                if combined_key not in floors_up:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[combined_key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[combined_key]['Area'] += floor_area
                    floors_up[combined_key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Regular-P":
                key = "תקרה דרוכה/Prestressed slab"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Regular-W Special":
                key = "תקרת צלעות/Ribbed slab"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Koteret":
                key = "כותרת לעיבוי נגד חדירה/Koteret"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Rampa":
                key = "רמפה/Rampa"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Geoplast-D":
                key = "תקרת צלעות במילוי גיאופלסט/Geoplast"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Slab":
                key = 'לוח"ד/Hollow slabs'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה בין לוחדים/Complitions_up'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Topping":
                key = 'יציקת טופינג/Topping'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_up[key]['Area'] += floor_area
                    floors_up[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark not in floors_up and floor_duplicationTypeMark not in combined_key:
                floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                floors_up[floor_duplicationTypeMark] = {"Area": floor_area, "Volume": floor_volume}

            else:
                floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                floors_up[floor_duplicationTypeMark]["Area"] += floor_area
                floors_up[floor_duplicationTypeMark]["Volume"] += floor_volume

        elif floor_type_comments == "Down":
            if not floor_duplicationTypeMark:
                key = "DTM empty DN_floors"
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark in ["Total Floor Area", "Total Floor Area Commercial",
                                               "Total Floor Area LSP",
                                               "Total Floor Area Pergola",
                                               "Air Double Level", "Air Elevator", "Air Pergola Aluminium",
                                               "Air Pergola Steel", "Air Pergola Wood", "Air Regular", "Air Stairs",
                                               "Landing-H", "Landing-S", "Landing Steel", "Polivid", "Backfilling","Aggregate"]:
                continue

            elif floor_duplicationTypeMark in ["Regular", "Balcon", "Regular-T"]:
                combined_key = "Regular_dn/רצפת בטון"
                if combined_key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[combined_key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[combined_key]['Area'] += floor_area
                    floors_down[combined_key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Rampa":
                key = 'רמפה/Rampa_dn'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Slab-Rib Special":
                key = 'רצפת צלעות/Ribbed floor'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Supporting":
                key = 'רגל לקיר תומך/leg for supporting wall'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Lite Beton":
                key = 'מצע בטון רזה מתחת לרצפת בטון/Lite Beton'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume
            elif floor_duplicationTypeMark == "Completion":
                key = 'השלמות יציקה מעל קורות/Dn_Complition'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "Sidewalk":
                key = 'מדרכות/Sidewalks'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark == "CLSM":
                key = 'CLSM'
                if key not in floors_down:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key] = {"Area": floor_area, "Volume": floor_volume}
                else:
                    floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                    floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                    floors_down[key]['Area'] += floor_area
                    floors_down[key]['Volume'] += floor_volume

            elif floor_duplicationTypeMark not in floors_down:
                floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                floors_down[floor_duplicationTypeMark] = {"Area": floor_area, "Volume": floor_volume}

            else:
                floor_area = floor_element.LookupParameter("Area").AsDouble() * 0.092903
                floor_volume = floor_element.LookupParameter("Volume").AsDouble() * 0.0283168466
                floors_down[floor_duplicationTypeMark]["Area"] += floor_area
                floors_down[floor_duplicationTypeMark]["Volume"] += floor_volume

    return floors_up, floors_down


getting_floors_parameters(floors_collector)
"""________FLOORS________"""
