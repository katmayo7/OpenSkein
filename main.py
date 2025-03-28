import pandas as pd
import os

def load_data():
    yarns_file = 'data/yarns_table.pkl'
    yarns = None
    stash = None

    if os.path.exists(yarns_file):
        print('Reading in old tables.')
        yarns = pd.read_pickle(yarns_file)
        stash = pd.read_pickle('data/stash_table.pkl')
    else:
        yarns = pd.DataFrame(columns=['Brand Name', 'Color', 'Material', 'Yarn Weight', 'Length/Skein (yds)', 'Weight/Skein (g)', 'Notes'])
        yarn_types = {'Brand Name': 'str', 'Color': 'str', 'Material': 'str', 'Yarn Weight': 'int', 'Length/Skein (yds)': 'float', 'Weight/Skein (g)': 'float', 'Notes': 'str'}
        yarns = yarns.astype(yarn_types)
        stash = pd.DataFrame(columns=['Brand Name', 'Color', '# Skeins', 'Length (yds)', 'Weight (g)', 'Dye Lots'])
        stash_types = {'Brand Name': 'str', 'Color': 'str', '# Skeins': 'float', 'Length (yds)': 'float', 'Weight (g)': 'float', 'Dye Lots': 'str'}
        stash = stash.astype(stash_types)
    
    return yarns,stash

def save_data(yarns_table):
    yarns_file = 'data/yarns_table.pkl'

    if not os.path.exists(yarns_file):
        os.mkdir('data/')
    
    yarns_table.to_pickle(yarns_file)

def print_table(table):
    print('**********************************************************************************************************')
    print(table)
    print('**********************************************************************************************************')

def check_exists(table, brand, color):
    tmp_i = table[(table['Brand Name'] == brand.lower()) & (table['Color'] == color.lower())].index.tolist()
    if len(tmp_i) > 1:
        print('!! Error: More than one entry matches this brand name and color??')
    
    if len(tmp_i) > 0:
        return tmp_i[0]

    return -1

# TO DO: finds the union of dye lot numbers or notes when updating a list in case there are repeats, could also work to make sure not duplicate dye lots in a single entry
# need to eliminate spaces in string after commas for this to work
# HERE
def format_long_form(one, two):
    set1 = set(one.split(','))
    set2 = set(two.split(','))
    union = list(set1.union(set2))
    union = [s + ',' for s in union]

    return ''.join(union)

# enforced lower case for strings, see if duplicate entry and overwrite old one if desired
def add_helper(table, new_data):
    text_fields = list(table.select_dtypes(include='object').columns)
    for t in text_fields:
        new_data[t] = new_data[t].lower()
    
    tmp_i = check_exists(table, new_data['Brand Name'], new_data['Color'])

    # TO DO: instead print what is different and ask if we want to update to those value or not, and if nothing is different don't even give option of updating
    if tmp_i > -1:
        print('!! It looks like you are trying to add a duplicate. This yarn is already logged as: ')
        print(table.loc[tmp_i])
        print('Would you like to update the entry with the following information?')
        
        for col in table.columns:
            if new_data[col] != table.loc[tmp_i][col]:
                print('{0}: {1}'.format(col, new_data[col]))
        print()

        update_entry = True

        if not update_entry:
            return None

        # TO DO: what if the new one they type has old and new ones? might want to do something other than simple addition here -- use format_long_form()
        if 'Notes' in table.columns and table.iloc[tmp_i]['Notes'] != new_data['Notes']:
            new_data['Notes'] = table.loc[tmp_i]['Notes'] + ', ' + new_data['Notes']
        elif 'Dye Lots' in table.columns and table.loc[tmp_i]['Dye Lots'] != new_data['Dye Lots']:
            new_data['Dye Lots'] = table.loc[tmp_i]['Dye Lots'] + ', ' + new_data['Dye Lots']

        remove_table_entry(table, tmp_i)

    return new_data

def add_to_yarn(ytable, new_data):
    # format, check if this entry already exists
    new_data = add_helper(ytable, new_data)

    # already exists and we're not updating anything
    if new_data == None:
        return

    # add the data to the data frame
    ytable.loc[len(ytable)] = new_data

def add_to_stash(ytable, stable, new_data):
    # first make sure this exists in the Yarn database, otherwise we need to add it
    # TO DO: actually need to gather the correct information for this.... 
    if check_exists(ytable, new_data['Brand Name'], new_data['Color']) == -1:
        #add_to_yarn(ytable, new_data)
        print('!! Error: must add to yarn database before it can be added to stash')
        print('Cannot add: {0} {1}'.format(new_data['Brand Name'], new_data['Color']))
        return

    # format, check if this entry already exists
    new_data = add_helper(stable, new_data)

    if new_data == None:
        return 
    
    # TO DO: deal with # Skeins, Length (yds), Weight (g)
    """
    assume only one of these is filled in
    --then we can calculate the other information from this using the remaining info
    """

    # TO DO: updating to a value of 0 for # skeins, length, or 0 should really delete the entry from the table
    
    # add the data to the data frame
    stable.loc[len(ytable)] = new_data

def remove_table_entry(table, remove_i=None, remove_brand=None, remove_color=None):
    if remove_brand != None:
        remove_i = check_exists(table, remove_brand, remove_color)
    
    table.drop(remove_i, inplace=True)

if __name__ == '__main__':

    yarns_table,stash_table = load_data()
    
    # TO DO: add interaction component to interact with databases
    """
    Implementation
    --use functions to populate and work with databases
    --interactive component to read input from command line to work with databases
    --develop front end to work with data instead
    """
    # TESTING YARN TABLE
    # 'Brand Name', 'Color', 'Material', 'Yarn Weight', 'Length/Skein (yds)', 'Weight/Skein (g)', 'Notes'
    new_yarn = {'Brand Name': 'Lion Brand', 'Color': 'black', 'Material': 'polyester', 'Yarn Weight': 3, 'Length/Skein (yds)': 300, 'Weight/Skein (g)': 100, 'Notes': 'very dark'}
    add_to_yarn(yarns_table, new_yarn)

    #print('Table now:')
    #print_table(yarns_table)
    #print()

    new_yarn = {'Brand Name': 'Lion brand', 'Color': 'black', 'Material': 'polyester', 'Yarn Weight': 3, 'Length/Skein (yds)': 400, 'Weight/Skein (g)': 100, 'Notes': 'nice to work with'}

    add_to_yarn(yarns_table, new_yarn)
    #print('Table Now:')
    #print_table(yarns_table)
    new_yarn = {'Brand Name': 'Caron Heart', 'Color': 'red', 'Material': '50% acyrlic, 50% cotton', 'Yarn Weight': 5, 'Length/Skein (yds)': 300, 'Weight/Skein (g)': 150, 'Notes': ''}
    add_to_yarn(yarns_table, new_yarn)

    print_table(yarns_table)
    print()

    # TESTING STASH TABLE
    # 'Brand Name', 'Color', '# Skeins', 'Length (yds)', 'Weight (g)', 'Dye Lots'
    """"
    print('Adding first')
    new_stash = {'Brand Name': 'lion brand', 'Color': 'black', '# Skeins': 2, 'Length (yds)': 100, 'Weight (g)': 100, 'Dye Lots': 'XYZ'}
    add_to_stash(yarns_table, stash_table, new_stash)

    # update
    print('Updating')
    new_stash = {'Brand Name': 'Lion Brand', 'Color': 'black', '# Skeins': 3, 'Length (yds)': 150, 'Weight (g)': 150, 'Dye Lots': '123'}
    add_to_stash(yarns_table, stash_table, new_stash)

    # duplicate
    print('Adding duplicate')
    new_stash = {'Brand Name': 'Lion Brand', 'Color': 'black', '# Skeins': 3, 'Length (yds)': 150, 'Weight (g)': 150, 'Dye Lots': '123'}
    add_to_stash(yarns_table, stash_table, new_stash)

    # add one not in yarns
    print('Adding error')
    new_stash = {'Brand Name': 'Malbrigo Rios', 'Color': 'blue', '# Skeins': 1, 'Length (yds)': 100, 'Weight (g)': 100, 'Dye Lots': 'ABC'}
    add_to_stash(yarns_table, stash_table, new_stash)

    print_table(stash_table)
    """

    # when done, save databases to files
    #save_data(yarns_table)