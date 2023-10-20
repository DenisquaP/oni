# Should be dict of dict
# Key: {'table_name': 'Table',
#       'variables': ['some_variable'],
#       'desc': ['int/varchar and other']}
# variables and description should be in pairs

tables = {
    'just key': {
        'table_name': 'Some_table',
        'variables': ['int'],
        'desc': ['serial']
    }
}


# Do not touch
def create(orm):
    for key in tables.keys():
        orm.create_tables(tables[key])
