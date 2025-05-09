import yarn_tables

# allows for viewing both meters and imperial measurements despite the general table settings (useful depending on pattern listing, etc.)
def view(tables, table_name, use_metric=False):
    if table_name == 'yarn':
        all_cols = tables.yarns_table.columns.tolist()
    elif table_name == 'stash':
        all_cols = tables.stash_table.columns.tolist()
    
    # color and brand name are always displayed
    all_cols.remove('BRAND NAME')
    all_cols.remove('COLOR')

    print('You may view a subset of the columns by inputting a comma separated list (no spaces after comma) of column names, or typing "all" to see the data for all columns.')
    print('Columns available for viewing: ', all_cols)
    to_view = input('Which columns of data would you like to view: ').upper()
    to_view = to_view.split(',')
    validated_to_view = []

    if to_view[0] == 'ALL':
        validated_to_view = all_cols
    else:
    # check everything in to_view is valid input (ie actual columns)
        for tv in to_view:
            if tv not in all_cols:
                print('Input of {0} does not match available column names. Please re-enter this desired column name or type "skip" to skip.'.format(tv))

                while tv not in all_cols and tv != 'SKIP':
                    tv = input('Column name: ').upper()
        
                if tv == 'SKIP':
                    continue

            validated_to_view.append(tv)
    
    if table_name == 'yarn':
        print(tables.yarns_table[validated_to_view])
    elif table_name == 'stash':
        print(tables.stash_table[[validated_to_view]])
    
def add_yarn(tables, brand=None, color=None, use_metric=False):
    correct = 'no'

    while correct == 'no':
        if brand == None:
            brand = input('Brand Name: ').lower()
        if color == None:
            color = input('Color: ').lower()
        mat = input('Material: ')
        yweight = input('Yarn Weight: ')
        if use_metric:
            length = input('Length/Skein (ms): ')
        else:
            length = input('Length/Skein (yds): ')
        gweight = input('Weight/Skein (g): ')
        wash = input('Machine washable (yes or no): ')
        notes = input('Additional notes: ').lower()

        print('We have gathered the following information:')
        print('----Brand Name: ', brand)
        print('----Color: ', color)
        print('----Material: ', mat)
        print('----Yarn Weight: ', yweight)
        print('----Length/Skein: ', length)
        print('----Weight/Skein (g): ', gweight)
        print('----Machine Washable: ', wash == 'yes')
        print('----Notes: ', notes)
        print()
        correct = input('Is this correct? (yes/no): ').lower()
    
    to_add = {'BRAND NAME': brand, 'COLOR': color, 'MATERIAL': mat, 'YARN WEIGHT': int(yweight), 'WEIGHT/SKEIN (G)': float(gweight), 'MACHINE WASHABLE': wash == 'yes', 'NOTES': notes}
    if use_metric:
        to_add['LENGTH/SKEIN (MS)'] = float(length)
        to_add['LENGTH/SKEIN (YDS)'] = None
    else:
        to_add['LENGTH/SKEIN (YDS)'] = float(length)
        to_add['LENGTH/SKEIN (MS)'] = None

    tables.add_to_yarn(to_add)

# need to check whether something is in the yarn table first
# add it to yarn table if it isn't
def add_stash(tables, use_metric=False):
    correct = 'no'

    while correct == 'no':
        brand = input('Brand Name: ').lower()
        color = input('Color: ').lower()

        # add to yarns if doesn't already exist
        print('Checking if {0} {1} exists in yarns.'.format(brand, color))

        if tables.check_exists(tables.yarns_table, brand, color) == -1:
            print('This yarn is not yet logged in the Yarn table. We require some additional information to log the yarn.')
            add_yarn(tables, brand, color, use_metric)

        dye_lots = input('Dye Lots (comma separated): ')

        weight = ''
        length = ''
        num_skeins = ''

        while num_skeins == '' and weight == '' and length == '':
            print('You must supply either number of skeins, length or weight of yarn. To skip one, simply leave the field blank and press enter.')
            num_skeins = input('Number of Skeins: ')

            if use_metric:
                length = input('Total Length (ms): ')
            else:
                length = input('Total Length (yds): ')

            weight = input('Total Weight (g): ')
        
        print('We have gathered the following information:')
        print('----Brand name: ', brand)
        print('----Color: ', color)
        if num_skeins != '':
            print('----# Skeins: ', num_skeins)
        else:
            print('----# Skeins: not supplied')
        if length != '':
            print('----Total Length: ', length)
        else:
            print('----Total Length: not supplied')
        if weight != '':
            print('----Total Weight (g): ', weight)
        else:
            print('----Total Weight (g): not supplied')
        print('----Dye Lots: ', dye_lots)

        correct = input('Is this information correct (yes/no): ').lower()
    
    to_add = {'BRAND NAME': brand, 'COLOR': color, 'DYE LOTS': dye_lots}
    if weight != '':
        to_add['TOTAL WEIGHT (G)'] = weight
    if length != '' and not use_metric:
        to_add['TOTAL LENGTH (YDS)'] = length
    if length != '' and use_metric:
        to_add['TOTAL LENGTH (MS)'] = length
    if num_skeins != '':
        to_add['# SKEINS'] = num_skeins
    
    tables.add_to_stash(to_add)

def remove_from_stash(tables):
    correct = 'no'

    while correct == 'no':
        brand_name = input('Brand Name: ' ).lower()
        color = input('Color: ').lower()

        print('We will remove the following entry from the stash: ')
        print('----Brand Name: ', brand_name)
        print('----Color: ', color)
        correct = input('You are about to remove this yarn from the stash. Is this information correct (yes/no): ').lower()
    
    if tables.check_exists(tables.stash_table, brand_name, color) > -1:
        tables.remove_table_entry(tables.stash_table, remove_brand=brand_name, remove_color=color)
    else:
        print('** Error: This yarn is not present in the stash **')

def check_validity(input_string, table=False):
    valid_tables = ['yarn', 'stash', 'back']
    valid_inputs = ['exit', 'view', 'add', 'filter', 'remove']

    if table:
        while input_string not in valid_tables:
            input_string = input('Which table (yarn, stash, back to return): ').lower()
    else:
        while input_string not in valid_inputs:
            print('What would you like to do?')
            print('----add: add an entry to a table')
            print('----view: view a table')
            print('----remove: remove an entry from the stash')
            print('----exit: exit the program')
            print()
            input_string = input('Type desired action: ').lower()
    
    return input_string

if __name__ == '__main__':

    """
    TO DO:
    --1) use functions to populate and work with databases [ done ]
    --2) interactive component to read input from command line to work with databases [ongoing]
    --3) develop front end UI to work with tables instead
    """
    set_metric = False

    yt = yarn_tables.YarnTables(metric=set_metric)
    yt.load_data()

    ci_input = None

    while ci_input != 'exit':
        ci_input = check_validity(ci_input, table=False)
        if ci_input == 'exit':
            break
        table = check_validity(None, table=True)
        print()
        
        if ci_input == 'view' and table != 'back':
            view(yt, table, set_metric)
        elif ci_input == 'add' and table != 'back':
            print()
            print('**************************************************')
            
            if table == 'yarn':
                add_yarn(yt)
                print('**************************************************')
                print()
                yt.print_table(yt.yarns_table)
            elif table == 'stash':
                add_stash(yt)
                print('**************************************************')
                print()
                yt.print_table(yt.stash_table)
        elif ci_input == 'remove' and table != 'back':
            # can only remove from stash
            if table == 'stash':
                pass
            elif table == 'yarn':
                print('** Can only remove from stash. **')
        elif ci_input == 'filter' and table != 'back':
            pass

        ci_input = None
        table = None
        
        print()
        


    #yt.save_data()
