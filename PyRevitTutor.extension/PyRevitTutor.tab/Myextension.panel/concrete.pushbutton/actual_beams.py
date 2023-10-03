from Autodesk.Revit.DB import *
import clr

# from openpyxl import  Workbook, load_workbook
# from openpyxl.utils import  get_column_letter


clr.AddReference("RevitAPI")
clr.AddReference("System")


doc = __revit__.ActiveUIDocument.Document

"""________BEAMS________"""

beams_collector = FilteredElementCollector(doc). \
    OfCategory(BuiltInCategory.OST_StructuralFraming). \
    WhereElementIsNotElementType(). \
    ToElements()

beams = {}

def beams_parameters(beam_list):
    for el in beam_list:
        element_type = doc.GetElement(el.GetTypeId())
        custom_param = element_type.LookupParameter("Duplication Type Mark").AsString()

        if custom_param == "Beam Steel":
            pass
        elif custom_param == "Beam Anchor":
            key = "קורת עוגנים"
            if custom_param not in beams:
                beams[key] = {"Count": 1}
            else:
                beams[key]['Count'] += 1

        elif custom_param == "Anchor Polymer":
            key = "עוגנים פולימרים"
            if custom_param not in beams:
                beams[key] = {"Count": 1}
            else:
                beams[key]['Count'] += 1

        elif custom_param == "Anchor Steel":
            key = "עוגנים"
            if custom_param not in beams:
                beams[key] = {"Count": 1}
            else:
                beams[key]['Count'] += 1

        elif custom_param == "Precast":
            key = "קורה טרומית"
            if custom_param not in beams:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key] = {"Volume": beam_volume, "Count": 1}
            else:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key]['Volume'] += beam_volume
                beams[key]['Count'] += 1

        elif custom_param == "Concrete":
            key = "קורת עוגנים מבטון"
            if custom_param not in beams:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key] = {"Volume": beam_volume, "Count": 1}
            else:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key]['Volume'] += beam_volume
                beams[key]['Count'] += 1

        elif custom_param in ["Regular", "Balcon", "Transformation", "Pergola", "Belts", "Tapered"]:
            combined_key = "קורות בטון"
            if combined_key not in beams:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[combined_key] = {"Volume": beam_volume}
            elif combined_key in beams:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[combined_key]['Volume'] += beam_volume
            # else:
            #     beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
            #     beams[combined_key] = {"Volume": beam_volume}
        elif not custom_param:
            key = "Without Duplication Type Mark"
            if key not in beams:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key] = {"Volume":beam_volume}
            else:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key]["Volume"] += beam_volume

        elif custom_param not in beams:
            key = "קורות"
            beam_volume = el.LookupParameter("Volume").AsDouble()
            if beam_volume:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key] = {"Volume":beam_volume}
        else:
            try:
                beam_volume = el.LookupParameter("Volume").AsDouble() * 0.0283168466
                beams[key]["Volume"] += beam_volume
                # beams[custom_param]["Count"] += 1
            except:
                pass

    return beams

beams_parameters(beams_collector)
