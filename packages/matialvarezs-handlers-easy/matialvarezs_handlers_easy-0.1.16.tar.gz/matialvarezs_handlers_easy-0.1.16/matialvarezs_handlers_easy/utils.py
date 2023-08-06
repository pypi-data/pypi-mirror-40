from json_response import JsonResponse
from math import e


def delete_db_object(db_object, **options):
    # method_delete => return object if exists or none
    message_ok_delete = options.get('message_ok_delete', 'delete ok')
    message_error_on_delete = options.get('message_error_on_delete', 'error on delete')
    if db_object:
        db_object.delete()
        return JsonResponse({"results": message_ok_delete, "error": None})
    return JsonResponse({"results": None, "error": message_error_on_delete})


def electrical_conductivity_to_25C_method_ratio_model(ce_value, temperature_value, **options):
    contant_value = options.get('contant_value', 0.02)
    return ce_value / (1 + contant_value * (temperature_value - 25))


def electrical_conductivity_to_25C_method_exponencial_model(ce_value, temperature_value):
    return ce_value * (0.4470 + 1.4034 * pow(e, (-1 * temperature_value / 26.815)))
