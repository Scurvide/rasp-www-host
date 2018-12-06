# Eats a dictionary of data and checks each value for
# requirements based on key

def syntax_check( data ):

    checks = 0
    checksRequired = len( data )
    msg = 'Incorrect syntax: '

    for key in data.keys():
        value = data[key]

        if key == 'name':
            if isinstance( value, str ):
                if len( value ) < 31 and len( value ) > 2:
                    checks += 1
                    continue
            return False, msg + 'name (str, 3-30 char)'

        elif key == 'secretId':
            if isinstance( value, str ):
                if len( value ) == 10 or value == 'None':
                    checks += 1
                    continue
            return False, msg + 'secretId (str, 10 char, can be None when registering)'

        elif key == 'command':
            if isinstance( value, str ):
                if len( value ) < 31 and len( value ) > 2:
                    checks += 1
                    continue
            return False, msg + 'command (str, 3-30 char)'

        elif key == 'commands':
            checksRequired += len( value ) - 1
            for com in value:
                if isinstance( com, str ):
                    if len( com ) < 31 and len( com ) > 2:
                        checks += 1
                        continue
                return False, msg + 'command (str, 3-30 char)'
            continue

        elif key == 'point':
            if isinstance( value, int ) or isinstance( value, float ):
                if len( str( value ) ) <= 10:
                    checks += 1
                    continue
            return False, msg + 'point (int or float, <11 char)'

        elif key == 'unit':
            if isinstance( value, str ):
                if len( value ) < 5 and len( value ) >= 0:
                    checks += 1
                    continue
            return False, msg + 'unit (str, 0-5 char)'

        return False, msg + 'unsupported key (' + key + ')'

    if checks == checksRequired:
        return True, 'Pass'
    return False, msg + 'unknown reason'
