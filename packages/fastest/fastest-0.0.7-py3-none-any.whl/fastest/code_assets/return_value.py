import re


def get_return_values(statements):
    return_values = re.findall(r'return (.*)', statements)
    if len(return_values) > 0:
        return return_values
    else:
        return [None]
