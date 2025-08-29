import yarn_tables
import pattern_and_proj_tables as ppt
import pandas as pd
from tabulate import tabulate

# allows for viewing both metric and imperial measurements despite the general table settings (useful depending on pattern listing, etc.)
def view(tables, table_name, use_metric=False, filter_table={}):
    if table_name == 'yarn':
        all_cols = tables.yarns_table.columns.tolist()
    elif table_name == 'stash':
        all_cols = tables.stash_table.columns.tolist()
    elif table_name == 'pattern':
        all_cols = tables.pattern_table.columns.tolist()
    elif table_name == 'project':
        all_cols = tables.project_table.columns.tolist()
    elif len(filter_table) > 0:
        all_cols = filter_table.columns.tolist()
    
    # color and brand name are always displayed in stash and yarn
    if table_name == 'yarn' or table_name == 'stash':
        all_cols.remove('BRAND NAME')
        all_cols.remove('COLOR')
    # project or patter name are always displayed
    elif table_name == 'project':
        all_cols.remove('PROJECT NAME')
    elif table_name == 'pattern':
        all_cols.remove('PATTERN NAME')

    print('You may view a subset of the columns by inputting a comma separated list of column names, or typing "all" to see the data for all columns.')
    print('Columns available for viewing: ', all_cols)
    to_view = input('Which columns of data would you like to view: ').upper()

    # allow for people to include or not include spaces in their comma separated list
    if ', ' in to_view:
        to_view = to_view.split(', ')
    else:
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
    
    # add back in columns that are always displayed
    if table_name == 'yarn' or table_name == 'stash':
        validated_to_view.insert(0, 'BRAND NAME')
        validated_to_view.insert(1, 'COLOR')
    elif table_name == 'project':
        validated_to_view.insert(0, 'PROJECT NAME')
    elif table_name == 'pattern':
        validated_to_view.insert(0, 'PATTERN NAME')
    
    if table_name == 'yarn':
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(tables.yarns_table[validated_to_view])
    elif table_name == 'stash':
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(tables.stash_table[validated_to_view])
    elif table_name == 'project':
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(tables.project_table[validated_to_view])
    elif table_name == 'pattern':
        with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(tables.pattern_table[validated_to_view])
    elif len(filter_table) > 0:
        return filter_table[validated_to_view]
    
def add_yarn(tables, brand=None, color=None, use_metric=False):
    correct = 'no'
    to_add = {}

    while correct == 'no':
        if brand == None:
            to_add['BRAND NAME'] = input('Brand Name: ').lower()
        else:
            to_add['BRAND NAME'] = brand
        if color == None:
            to_add['COLOR'] = input('Color: ').lower()
        else:
            to_add['COLOR'] = color

        to_add['MATERIAL'] = input('Material: ')
        to_add['YARN WEIGHT'] = int(input('Yarn Weight: '))

        if use_metric:
            to_add['LENGTH/SKEIN (MS)'] = float(input('Length/Skein (ms): '))
            to_add['LENGTH/SKEIN (YDS)'] = None
        else:
            to_add['LENGTH/SKEIN (YDS)'] = float(input('Length/Skein (yds): '))
            to_add['LENGTH/SKEIN (MS)'] = None

        to_add['WEIGHT/SKEIN (G)'] = float(input('Weight/Skein (g): '))
        wash = input('Machine washable (yes or no): ').lower()
        if wash == 'yes':
            to_add['MACHINE WASHABLE'] = True
        else:
            to_add['MACHINE WASHABLE'] = False

        to_add['NOTES'] = input('Additional notes: ').lower()

        print('We have gathered the following information:')
        print('----Brand Name: ', to_add['BRAND NAME'])
        print('----Color: ', to_add['COLOR'])
        print('----Material: ', to_add['MATERIAL'])
        print('----Yarn Weight: ', to_add['YARN WEIGHT'])
        if use_metric:
            print('----Length/Skein: ', to_add['LENGTH/SKEIN (MS)'])
        else:
            print('----Length/Skein: ', to_add['LENGTH/SKEIN (YDS)'])
        print('----Weight/Skein (g): ', to_add['WEIGHT/SKEIN (G)'])
        print('----Machine Washable: ', to_add['MACHINE WASHABLE'])
        print('----Notes: ', to_add['NOTES'])
        print()
        correct = input('Is this correct? (yes/no): ').lower()

    tables.add_to_yarn(to_add)

# need to check whether something is in the yarn table first
# add it to yarn table if it isn't
def add_stash(tables, use_metric=False):
    correct = 'no'
    to_add = {}

    while correct == 'no':
        to_add['BRAND NAME'] = input('Brand Name: ').lower()
        to_add['COLOR'] = input('Color: ').lower()

        # add to yarns if doesn't already exist
        print('Checking if {0} {1} exists in yarns.'.format(to_add['BRAND NAME'], to_add['COLOR']))

        if tables.check_exists(tables.yarns_table, to_add['BRAND NAME'], to_add['COLOR']) == -1:
            print('This yarn is not yet logged in the Yarn table. We require some additional information to log the yarn.')
            add_yarn(tables, to_add['BRAND NAME'], to_add['COLOR'], use_metric)
        else:
            print('This yarn has previously been logged in the Yarn table. Can proceed logging to Stash table.')

        print('Continue logging to Stash table.')
        to_add['DYE LOTS'] = input('Dye Lots (comma separated): ')

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
        print('----Brand name: ', to_add['BRAND NAME'])
        print('----Color: ', to_add['COLOR'])
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
        print('----Dye Lots: ', to_add['DYE LOTS'])

        correct = input('Is this information correct (yes/no): ').lower()

    # if we're removing from stash
    if weight == 0 or length == 0 or num_skeins == 0:
        to_add['TOTAL WEIGHT (G)'] = 0
        to_add['TOTAL LENGTH (YDS)'] = 0
        to_add['TOTAL LENGTH (MS)'] = 0
        to_add['# SKEINS'] = 0
    
    if weight != '':
        to_add['TOTAL WEIGHT (G)'] = weight
    else:
        to_add['TOTAL WEIGHT (G)'] = None
    if length != '' and not use_metric:
        to_add['TOTAL LENGTH (YDS)'] = length
    else:
        to_add['TOTAL LENGTH (YDS)'] = None
    if length != '' and use_metric:
        to_add['TOTAL LENGTH (MS)'] = length
    else:
        to_add['TOTAL LENGTH (MS)'] = None
    if num_skeins != '':
        to_add['# SKEINS'] = num_skeins
    else:
        to_add['# SKEINS'] = None
    
    tables.add_to_stash(to_add)

def add_pattern(pt_tables, pattern_name=None, use_metric=False):
    correct = 'no'
    to_add = {}

    while correct == 'no':
        if pattern_name == None:
            to_add['PATTERN NAME'] = input('Pattern Name: ').lower()
        else:
            to_add['PATTERN NAME'] = pattern_name

        to_add['SUGGESTED YARN WEIGHT'] = int(input('Suggested Yarn Weight: '))
        to_add['SUGGESTED HOOK SIZE'] = float(input('Suggested Hook Size: '))

        if use_metric:
            to_add['TOTAL AMOUNT OF YARN (MS)'] = float(input('Total amount of yarn in meters: '))
            to_add['TOTAL AMOUNT OF YARN (YDS)'] = None
        else:
            to_add['TOTAL AMOUNT OF YARN (YDS)'] = float(input('Total amount of yarn in yards: '))
            to_add['TOTAL AMOUNT OF YARN (MS)'] = None

        to_add['CATEGORY'] = input('Category name for pattern: ').lower()
        to_add['NOTES'] = input('Notes: ').lower()
        # note for URLs capitalization may matter, so don't force to lowercase
        to_add['SOURCE'] = input('Information reagrding pattern source (e.g., book name, website URL): ')

        print('We have gathered the following information:')
        print('----Pattern Name: ', to_add['PATTERN NAME'])
        print('----Suggested Yarn Weight: ', to_add['SUGGESTED YARN WEIGHT'])
        print('----Suggested Hook Size: ', to_add['SUGGESTED HOOK SIZE'])
        if use_metric:
            print('----Total Amount of Yarn: {0} meters'.format(to_add['TOTAL AMOUNT OF YARN (MS)']))
        else:
            print('----Total Amount of Yarn: {0} yards'.format(to_add['TOTAL AMOUNT OF YARN (YDS)']))
        print('----Category: ', to_add['CATEGORY'])
        print('----Notes: ', to_add['NOTES'])
        print('----Pattern Source: ', to_add['SOURCE'])

        correct = input('Is this information correct (yes/no)?: ').lower()
    
    pt_tables.add_to_pattern(to_add)

# need to check if pattern and yarn are logged first and if not log them
def add_project(ytables, pt_tables, use_metric=False):
    correct = 'no'
    to_add = {}

    while correct == 'no':
        to_add['PROJECT NAME'] = input('Project Name: ').lower()
        to_add['PATTERN NAME'] = input('Pattern Name: ').lower()

        # check if pattern has been logged
        print('Checking if {0} exists in the pattern table.'.format(to_add['PATTERN NAME']))
        if pt_tables.check_exists(pt_tables.pattern_table, to_add['PATTERN NAME']) == -1:
            print('This pattern is not yet logged in the Pattern table. We require some additional information to log the pattern.')
            add_pattern(pt_tables, to_add['PATTERN NAME'], use_metric)
        else:
            print('This pattern has previously been logged in the Pattern table. Can proceed logging to Project table.')
        
        print('Continue logging to Project table.')

        # get yarn information using yarn table -- force logging if not already logged
        mwashable = True
        all_yarns = ''
        all_amts = ''
        all_dye_lots = ''

        new_yarn = ''

        while new_yarn != 'done':
            yarn_brand = input('Input the brand name (e.g. malabrigo rios) of yarn used or type done if inputted all yarn: ').lower()
            if yarn_brand == 'done':
                break
            
            yarn_color = input('Input the yarn color: ').lower()
            if len(all_yarns) > 0:
                all_yarns += '; '
            all_yarns = all_yarns + yarn_brand + ' ' + yarn_color

            yarn_amt = input('How much yarn did you use in ms or yds: ')
            if len(all_amts) > 0:
                all_amts += '; '
            all_amts += yarn_amt

            yarn_dyes = input('List the dye lots used (separated by commas): ')
            if len(all_dye_lots) > 0:
                all_dye_lots += '; '
            all_dye_lots += yarn_dyes

            # ensure yarn is logged
            print('Checking if {0} {1} exists in yarns.'.format(yarn_brand, yarn_color))
            yarn_i = ytables.check_exists(ytables.yarns_table, yarn_brand, yarn_color)
            print(yarn_i)
            if yarn_i == -1:
                print('This yarn is not yet logged in the Yarn table. We require some additional information to log the yarn.')
                add_yarn(yt, yarn_brand, yarn_color)
                yarn_i = len(yt.yarns_table)-1
            else:
                print('This yarn has previously been logged in the Yarn table. Can proceed logging to Project table.')
            
            print('Continue logging to Project table.')

            # get machine washability
            if not yt.yarns_table.loc[yarn_i, 'MACHINE WASHABLE']:
                mwashable = False
            # get yarn weight -- assume all yarn is same weight and saves final yarn info
            to_add['YARN WEIGHT'] = yt.yarns_table.loc[yarn_i, 'YARN WEIGHT']

        to_add['YARN(S) USED (BRAND+COLOR)'] = all_yarns
        to_add['AMOUNT OF YARN (PER YARN)'] = all_amts
        to_add['DYE LOTS (PER YARN)'] = all_dye_lots
        to_add['MACHINE WASHABLE'] = mwashable

        if use_metric:
            to_add['TOTAL AMOUNT OF YARN (MS)'] = float(input('Total amount of yarn used (over all brands) in meters: '))
            to_add['TOTAL AMOUNT OF YARN (YDS)'] = None
        else:
            to_add['TOTAL AMOUNT OF YARN (YDS)'] = float(input('Total amount of yarn used (over all brands) in yards: '))
            to_add['TOTAL AMOUNT OF YARN (MS)'] = None

        to_add['HOOK SIZE USED'] = float(input('Hook size used: '))
        to_add['NOTES'] = input('Notes: ').lower()
    
        print('We have gathered the following information: ')
        print('----Project Name: ', to_add['PROJECT NAME'])
        print('----Pattern Name: ', to_add['PATTERN NAME'])
        print('----Yarn(s) Used (Brand+Color): ', to_add['YARN(S) USED (BRAND+COLOR)'])
        print('----Total amount of Yarn (per yarn): ', to_add['AMOUNT OF YARN (PER YARN)'])
        if use_metric:
            print('----Total amount of yarn (MS): ', to_add['TOTAL AMOUNT OF YARN (MS)'])
        else:
            print('----Total amount of yarn (YDS): ', to_add['TOTAL AMOUNT OF YARN (YDS)'])
        print('----Dye Lots: ', to_add['DYE LOTS (PER YARN)'])
        print('----Hook Size Used: ', to_add['HOOK SIZE USED'])
        print('----Machine Washable: ', to_add['MACHINE WASHABLE'])
        print('----Notes: ', to_add['NOTES'])

        correct = input('Is this correct (yes/no)?: ').lower()
    
    pt_tables.add_to_project(to_add)
 
def remove_from(tables, table_name):
    correct = 'no'

    while correct == 'no':
        if table_name == 'stash':
            brand_name = input('Brand Name: ' ).lower()
            color = input('Color: ').lower()

            print('We will remove the following entry from the stash: ')
            print('----Brand Name: ', brand_name)
            print('----Color: ', color)
            correct = input('You are about to remove this yarn from the stash. Is this information correct (yes/no): ').lower()
        else:
            project_name = input('Project Name: ').lower()
            print('We will remove the following entry from project: ')
            print('----Project Name: ', project_name)
            correct = input('You are about to remove this project from the project table. Is this information correct (yes/no): ').lower()
    
    if table_name == 'stash' and tables.check_exists(tables.stash_table, brand_name, color) > -1:
        tables.remove_table_entry(tables.stash_table, remove_brand=brand_name, remove_color=color)
    elif table_name == 'project' and tables.check_exists(tables.project_table, project_name, pattern=False):
        tables.remove_table_entry(tables, remove_name=project_name, pattern_search=False)
    elif table_name == 'project':
        print('** Error: This project is not present in the project table. **')
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
def filter(tables, table_name, metric=False):
    # get additional tables if necessary
    print('Filtering {0} table.'.format(table_name))
    
    # create new table to filter on, possibly the result of joining yarn and stash tables together on brand+color
    fil_table = None

    if 'yarn' in table_name:
        fil_table = tables.yarns_table
    else:
        fil_table = pd.DataFrame()
    
    # stash table, but not yarn table involved
    if 'stash' in table_name and fil_table.shape[0] == 0:
        fil_table = tables.stash_table
    # stash table is being added to yarn table
    elif 'stash' in table_name:
        fil_table = pd.merge(fil_table, tables.stash_table, how='outer', on=['BRAND NAME', 'COLOR'])
    
    if table_name == 'pattern':
        fil_table = tables.pattern_table
    elif table_name == 'project':
        fil_table = tables.project_table

    # rename some of the columns in yarn+stash case
    fil_table = fil_table.rename(columns={'DATE ADDED_x': 'DATE ADDED YARN', 'LAST UPDATED_x': 'LAST UPDATED YARN', 'DATE ADDED_y': 'DATE ADDED STASH', 'LAST UPDATED_y': 'LAST UPDATED STASH', '# SKEINS': '# SKEINS STASHED', 'TOTAL LENGTH (YDS)': 'TOTAL LENGTH (YDS) STASHED', 'TOTAL LENGTH (MS)': 'TOTAL LENGTH (MS) STASHED', 'TOTAL WEIGHT (G)': 'TOTAL WEIGHT (G) STASHED', 'DYE LOTS': 'DYE LOTS STASHED'})

    # TO DO: do we want to be able to check that a notes or dye lot section includes the following, for example we want notes that include "cuddly"?
    check_equals = ['YARN WEIGHT', 'MACHINE WASHABLE', 'SUGGESTED YARN WEIGHT', 'SUGGESTED HOOK SIZE', 'CATEGORY', 'HOOK SIZE USED']
    check_partial = ['NOTES', 'SOURCE', 'MATERIAL']
    check_eq_or_part = ['BRAND NAME', 'COLOR', 'PROJECT NAME', 'PATTERN NAME']
    check_geq_leq = ['# SKEINS', '# SKEINS STASHED' 'TOTAL LENGTH (YDS)', 'TOTAL LENGTH (YDS) STASHED', 'TOTAL LENGTH (MS)', 'TOTAL LENGTH (MS) STASHED', 'TOTAL WEIGHT (G)', 'TOTAL WEIGHT (G) STASHED', 'TOTAL AMOUNT OF YARN (YDS)', 'TOTAL AMOUNT OF YARN (MS)']
    # possible filtering columns in this table/joined table
    in_table = []

    for c in fil_table.columns.to_list():
        if c in check_equals or c in check_geq_leq or c in check_partial or c in check_eq_or_part:
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
            match = None
            
            if col_name in check_equals or col_name in check_partial:
                correct = 'no'
                while correct != 'yes':
                    # requires boolean
                    if col_name == 'MACHINE WASHABLE':
                        filter_val = input('Enter the value of {0} you are looking for (true/false or yes/no valid): ')
                    # requires numerical input
                    elif col_name == 'YARN WEIGHT' or col_name == 'SUGGESTED YARN WEIGHT':
                        filter_val = valid_number(col_name, float_val=False)
                    # requires float input
                    elif col_name == 'SUGGESTED HOOK SIZE' or col_name == 'HOOK SIZE USED':
                        filter_val = valid_number(col_name, float_val=True)
                    else:
                        filter_val = input('Enter the value of {0} you are looking for: '.format(col_name))
                    
                    correct = input('Is {0} correct? (yes/no) '.format(filter_val)).lower()
            elif col_name in check_eq_or_part:
                correct = 'no'
                while correct != 'yes':
                    match = None
                    # determine if we want exact or partial match
                    while match != 'exact' and match != 'partial':
                        match = input('What kind of match would you like (exact/partial): ').lower()
                    
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
            elif col_name in check_equals or (col_name in check_eq_or_part and match == 'exact'):
                fil_table = fil_table[fil_table[col_name] == filter_val]
            elif col_name in check_partial or (col_name in check_eq_or_part and match == 'partial'):
                fil_table = fil_table[fil_table[col_name].str.contains(filter_val)]
            elif col_name in check_geq_leq and comp == '>':
                fil_table = fil_table[fil_table[col_name] >= filter_val]
            else:
                fil_table = fil_table[fil_table[col_name] <= filter_val]


            print()
            inter_yes = ''
            while inter_yes != 'yes' and inter_yes != 'no':
                inter_yes = input('See intermediate results (yes/no): ').lower()

            if inter_yes == 'yes':
                with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
                    print(fil_table)
    
    # allow viewing only a subset of available columns from the final table
    subset_view = input('Do you wish to select for viewing a subset of the columns in the final filtered table? (yes/no) ')
    if subset_view.lower() == 'yes':
        fil_table = view(None, None, filter_table=fil_table)
    
    print()
    print('FILTERED TABLE:')
    print('************************************************************************************************************')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None,):
            print(fil_table)
    print('************************************************************************************************************')


def check_validity(input_string, table=False, filtering=False):
    valid_tables = ['yarn', 'stash', 'pattern', 'project', 'back']
    valid_filtering = ['yarn', 'stash', 'yarn+stash', 'pattern', 'project', 'back']
    valid_inputs = ['exit', 'view', 'add', 'filter', 'remove']

    if table and filtering:
        while input_string not in valid_filtering:
            #input_string = input('Which table first (yarn, stash, pattern, project, back to return): ').lower()
            input_string = input('Which table(s) (yarn, stash, yarn+stash, pattern, project, back to return): ').lower()
    elif table:
        while input_string not in valid_tables:
            input_string = input('Which table (yarn, stash, pattern, project, back to return): ').lower()
    else:
        while input_string not in valid_inputs:
            print('What would you like to do?')
            print('----add: add an entry to a table')
            print('----view: view a table (subset of columns allowed)')
            print('----remove: remove an entry from the stash')
            print('----filter: filter tables by column entries')
            print('----exit: exit the program')
            print()
            input_string = input('Type desired action: ').lower()
    
    return input_string

if __name__ == '__main__':

    set_metric = False

    yt = yarn_tables.YarnTables(metric=set_metric)
    yt.load_data()
    yt_tables = ['yarn', 'stash', 'yarn+stash']

    pt = ppt.PatternProjTables(metric=set_metric)
    pt.load_data()
    pt_tables = ['pattern', 'project']

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
        
        # view tables
        if ci_input == 'view' and table != 'back' and table in yt_tables:
            view(yt, table, set_metric)
        elif ci_input == 'view' and table != 'back' and table in pt_tables:
            view(pt, table, set_metric)
        # add to tables
        elif ci_input == 'add' and table != 'back' and table == 'yarn':
            print()
            print('**************************************************')
            add_yarn(yt)
            print('**************************************************')
            print()
            yt.print_table(yt.yarns_table)
        elif ci_input == 'add' and table != 'back' and table == 'stash':
            print()
            print('**************************************************')
            add_stash(yt)
            print('**************************************************')
            print()
            yt.print_table(yt.stash_table)
        elif ci_input == 'add' and table != 'back' and table == 'pattern':
            print()
            print('**************************************************')
            add_pattern(pt)
            print('**************************************************')
            print()
            pt.print_table(pt.pattern_table)
        elif ci_input == 'add' and table != 'back' and table =='project':
            print()
            print('**************************************************')
            add_project(yt, pt)
            print('**************************************************')
            print()
            pt.print_table(pt.project_table)
        # remove from tables
        elif ci_input == 'remove' and table != 'back' and table == 'stash':
            remove_from(yt, 'stash')
        elif ci_input == 'remove' and table != 'back' and table == 'project':
            remove_from(pt, 'project')
        elif ci_input == 'remove' and table != 'back':
            print('** Can only remove from stash or project tables. **')
        # filter tables
        elif ci_input == 'filter' and table != 'back' and table in yt_tables:
            filter(yt, table, set_metric)
        elif ci_input == 'filter' and table != 'back' and table in pt_tables:
            filter(pt, table, set_metric)

        ci_input = None
        table = None
        
        print()
        
    print('****************************************************************************************')
    print('Saving data.')
    yt.save_data()
    pt.save_data()
    print('Exiting program.')
    print('*****************************************************************************************')
