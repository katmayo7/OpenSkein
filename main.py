import pandas as pd
import os

# TO DO: add an item to the table
def add_to_table():
    pass

# TO DO: update information stored in a table
def update_table_entry():
    pass

# TO DO: remove an item from the table (stash and project only?)
def remove_table_entry():
    pass

if __name__ == '__main__':

    yarns_file = 'data/yarns_table.pkl'
    stash_file = 'data/stash_table.pkl'
    # TO DO: work on project table
    #projs_file = 'data/projs_table.pkl'

    yarns_table = None
    stash_table = None 
    #projs_table = None
    
    # load saved database, otherwise create a new one
    if os.path.exists(yarns_file):
        print('Reading in old tables.')
        yarns_table = pd.read_pickle(yarns_file)
        stash_table = pd.read_pickle(stash_file)
        #projs_table = pd.read_pickle(projs_file)
    else:
        yarns_table = pd.DataFrame(columns=['Brand Name', 'Color', 'Material', 'Weight', 'Notes'])
        # TO DO: allow for versatile yards or meters usage
        stash_table = pd.DataFrame(columns=['Brand Name', 'Color', '# Skeins', '# Yards', '# Meters', 'Dye Lots'])

    # TO DO: add interaction to add/see data
    
    print('Yarns:')
    print(yarns_table)
    print()
    print('Stash table:')
    print(stash_table)
    print()

    # when done, save databases to files
    if not os.path.exists(yarns_file):
        os.mkdir('data/')
    yarns_table.to_pickle(yarns_file)
    stash_table.to_pickle(stash_file)
    #projs_table.to_pickle(projs_file)