import yarn_tables
import pandas as pd

# allows for viewing both metric and imperial measurements despite the general table settings (useful depending on pattern listing, etc.)
def view(tables, table_name, use_metric=False, filter_table={}):
    if table_name == 'yarn':
        all_cols = tables.yarns_table.columns.tolist()
    elif table_name == 'stash':
        all_cols = tables.stash_table.columns.tolist()
    elif len(filter_table) > 0:
        all_cols = filter_table.columns.tolist()
    
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
    
    # add back in brand name and color, which are always displayed
    validated_to_view.insert(0, 'BRAND NAME')
    validated_to_view.insert(1, 'COLOR')
    
    if table_name == 'yarn':
        print(tables.yarns_table[validated_to_view])
    elif table_name == 'stash':
        print(tables.stash_table[validated_to_view])
    elif len(filter_table) > 0:
        return filter_table[validated_to_view]
    
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

# helper function to turn input into appropriate numerical value
def valid_number(col, com='', float_val=True):
    value = None

    while True:
        try:
            if float_val:
                if com != '':
                    value = float(input('Enter the value {0} should be {1} than or equal to: '.format(col, com)))
                else:
                    value = float(input('Enter value: '))
            else:
                # yarn weight case
                value = int(input('Enter the {0} value: '.format(col)))

        except ValueError:
            print('Must input an integer or decimal value.')
    
        return value
    
# see only the entries that match a certain criteria in one or more tables, allows for viewing metric and imperial if desired
def filter(ytables, table_name, metric=False):
    # get additional tables if necessary
    print('Filtering {0} table.'.format(table_name))
    tables = set()
    tables.add(table_name)

    valid_tables = ['yarn', 'stash', 'none']
    ad_table = None

    while ad_table != 'none' and ad_table != '':
        ad_table = input('Enter the name of additional tables for filtering (choices: yarn, stash, none): ').lower()
        if ad_table not in valid_tables:
            print("I'm sorry, that table is not an option. Please select again, or enter none to finish.")
            ad_table = None
        else:
            if ad_table != 'none':
                tables.add(ad_table)
    
    # create new table to filter on, possibly the result of joining multiple tables together on brand+color
    fil_table = None

    if 'yarn' in tables:
        fil_table = ytables.yarns_table
    else:
        fil_table = pd.DataFrame()

    if 'stash' in tables and fil_table.shape[0] == 0:
        fil_table = ytables.stash_table
    elif 'stash' in tables:
        fil_table = pd.merge(fil_table, ytables.stash_table, how='outer', on=['BRAND NAME', 'COLOR'])

    check_equals = ['BRAND NAME', 'COLOR', 'MATERIAL', 'YARN WEIGHT', 'MACHINE WASHABLE']
    check_geq_leq = ['# SKEINS', 'TOTAL LENGTH (YDS)', 'TOTAL LENGTH (MS)', 'TOTAL WEIGHT (G)']
    # possible filtering columns in this table/joined table
    in_table = []

    for c in fil_table.columns.to_list():
        if c in check_equals or c in check_geq_leq:
            in_table.append(c)

    # iterativley filter table by asking what column and values to performing filtering on
    col_name = None
    print('The following columns are available for filtering: {0}'.format(in_table))
    prev_filtered = []

    while col_name != 'NONE' and col_name != '':
        # get column name for filtering
        col_name = input("Enter a column you'd like to filter on or none to terminate: ").upper()

        if col_name not in in_table and col_name != 'NONE' or col_name in prev_filtered:
            print("I'm sorry, that is not a valid column name.")
            print('The following columns are availalbe for filtering: {0}'.format(in_table))
            col_name = None
        elif col_name == 'NONE':
            break
        else:
            prev_filtered.append(col_name)

            # get value to filter on
            filter_val = None
            comp = ''
            
            if col_name in check_equals:
                correct = 'no'
                while correct != 'yes':
                    # requires boolean
                    if col_name == 'MACHINE WASHABLE':
                        filter_val = input('Enter the value of {0} you are looking for (true/false or yes/no valid): ')
                    # requires numerical input
                    elif col_name == 'YARN WEIGHT':
                        filter_val = valid_number(col_name, float_val=False)
                    else:
                        filter_val = input('Enter the value of {0} you are looking for: '.format(col_name))
                    
                    correct = input('Is {0} correct? (yes/no) '.format(filter_val)).lower()
            else:
                correct = 'no'
                while correct != 'yes':
                    # determine if we want to filter so value is >= or <=
                    while comp != '>' and comp != '<':
                        comp = input('Enter > for {0} value is greater than or equal to, and < for less than or equal to: '.format(col_name))
                    
                    # get value for filtering column
                    if comp == '>':
                        filter_val = valid_number(col_name, 'greater')
                        correct = input('Is {0} greater than or equal to {1} correct? (yes/no) '.format(col_name, filter_val)).lower()
                    else:
                        filter_val = valid_number(col_name, 'less')
                        correct = input('Is {0} less than or equal to {1} correct? (yes/no) '.format(col_name, filter_val)).lower()
        
            # filter
            if col_name in check_equals and col_name == 'MACHINE WASHABLE':
                fil_table = fil_table[fil_table[col_name] == (filter_val.lower() == 'yes' or filter_val.lower() == 'true')]
            elif col_name in check_equals:
                fil_table = fil_table[fil_table[col_name] == filter_val]
            elif col_name in check_geq_leq and comp == '>':
                fil_table = fil_table[fil_table[col_name] >= filter_val]
            else:
                fil_table = fil_table[fil_table[col_name] <= filter_val]
            
            print()
            print(fil_table)
            print()
    

    # allow viewing only a subset of available columns from the final table
    subset_view = input('Do you wish to select for viewing a subset of the columns in the final filtered table? (yes/no) ')
    if subset_view.lower() == 'yes':
        fil_table = view(None, None, filter_table=fil_table)
    
    print()
    print('FILTERED TABLE:')
    print('************************************************************************************************************')
    print(fil_table)
    print('************************************************************************************************************')


def check_validity(input_string, table=False, filtering=False):
    valid_tables = ['yarn', 'stash', 'back']
    valid_inputs = ['exit', 'view', 'add', 'filter', 'remove']

    if table:
        while input_string not in valid_tables:
            if filtering:
                input_string = input('Which table first (yarn, stash, back to return): ').lower()
            else:
                input_string = input('Which table (yarn, stash, back to return): ').lower()
    else:
        while input_string not in valid_inputs:
            print('What would you like to do?')
            print('----add: add an entry to a table')
            print('----view: view a table')
            print('----remove: remove an entry from the stash')
            print('----filter: filter tables by column entries')
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
        
        # call modified table input prompt if going to be filtering tables
        if ci_input == 'filter':
            table = check_validity(None, table=True, filtering=True)
        else:
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
            filter(yt, table, set_metric)

        ci_input = None
        table = None
        
        print()
        
    print('****************************************************************************************')
    print('Saving data.')
    yt.save_data()
    print('Exiting program.')
    print('*****************************************************************************************')
