
def resolveobject(instance, defination):
    if 'accessor' in defination:
        return defination['accessor'](instance)
    for prop in defination['properties']:
        