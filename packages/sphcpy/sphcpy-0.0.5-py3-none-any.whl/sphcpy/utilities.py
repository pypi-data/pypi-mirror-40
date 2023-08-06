
def is_number(s):
    ''' Tests the string for conversion to float.'''
    try:
        float(s)
        return True
    except ValueError:
        return False
