# First version (only to remember idea), 
# it should be checked before use in any production.

def listify_dict(d, i=0):
    '''
    Retruns the list of dictionary values.
    '''
    list_of_values = list()
    for key, value in d.items():
        if isinstance(value, dict) and i < 2:
            list_of_values = listify_dict(value, i=+1)
        else:
            list_of_values.append(value)
    return list_of_values
