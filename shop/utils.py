from rest_framework import status
from rest_framework.response import Response


def handle_error(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


def are_dicts_equal(dict1, dict2):
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key in dict1.keys():
        value1 = dict1[key]
        value2 = dict2[key]

        if isinstance(value1, dict) and isinstance(value2, dict):
            if not are_dicts_equal(value1, value2):
                return False
        elif isinstance(value1, list) and isinstance(value2, list):
            if not are_lists_equal(value1, value2):
                return False
        elif value1 != value2:
            return False

    return True


def are_lists_equal(list1, list2):
    if len(list1) != len(list2):
        return False

    for elem1, elem2 in zip(list1, list2):
        if isinstance(elem1, dict) and isinstance(elem2, dict):
            if not are_dicts_equal(elem1, elem2):
                return False
        elif isinstance(elem1, list) and isinstance(elem2, list):
            if not are_lists_equal(elem1, elem2):
                return False
        elif elem1 != elem2:
            return False

    return True
