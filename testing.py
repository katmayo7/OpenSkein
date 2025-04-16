import yarn_tables

def setup():
    yt = yarn_tables.YarnTables()
    yt.load_data()

    return yt

# test that yarn table behaves as desired
def test_yarn_table(yts, print_info=True):
    
    # expected: add yarn to table
    print('*** Adding Lion Brand black ***')
    new_yarn = {'Brand Name': 'Lion Brand', 'Color': 'black', 'Material': 'polyester', 'Yarn Weight': 3, 'Length/Skein (yds)': 300, 'Length/Skein (ms)': 250, 'Weight/Skein (g)': 100, 'Machine Washable': False, 'Notes': 'very dark'}
    yts.add_to_yarn(new_yarn)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()

    # expected: update the information
    print('*** Updating info for Lion Brand black ***')
    new_yarn = {'Brand Name': 'Lion brand', 'Color': 'black', 'Material': 'polyester', 'Yarn Weight': 3, 'Length/Skein (yds)': 400, 'Length/Skein (ms)': 350, 'Weight/Skein (g)': 100, 'Machine Washable': False, 'Notes': 'nice to work with'}
    yts.add_to_yarn(new_yarn)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()

    # expected: add yarn to table
    print('*** Adding Caron Heart red **')
    new_yarn = {'Brand Name': 'Caron Heart', 'Color': 'red', 'Material': '50% acyrlic, 50% cotton', 'Yarn Weight': 5, 'Length/Skein (yds)': 300, 'Length/Skein (ms)': 250, 'Weight/Skein (g)': 150, 'Machine Washable': True, 'Notes': ''}
    yts.add_to_yarn(new_yarn)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()
    
    # always print the final table at the end
    if not print_info:
        yts.print_table(yts.yarns_table)
        print()

    print('---------- Testing Completed ----------')

# test that stash table behaves as desired -- requires yarn table to be popualted to work
def test_stash_table(yts):

    test_yarn_table(yts, print_info=False)

    # expected: add to stash and fill in total weight (also total length in ms, but that won't be shown)
    print('*** Add lion brand black to stash -- should calculate the total weight')
    new_stash = {'Brand Name': 'lion brand', 'Color': 'black', '# Skeins': 2, 'Total Length (yds)': 100, 'Total Length (ms)': None, 'Total Weight (g)': None, 'Dye Lots': 'xyz' }
    yts.add_to_stash(new_stash)

    yts.print_table(yts.stash_table)
    print()

    # expected: update stash to increase # of skeins by adding duplicate (total length and number of skeins should increase)
    print('*** Increase amount of lion brand black in stash -- # skeins and length should increase as result')
    new_stash = {'Brand Name': 'lion brand', 'Color': 'black', '# Skeins': None, 'Total Length (yds)': None, 'Total Length (ms)': None, 'Total Weight (g)': 300, 'Dye Lots': 'xyz, abc'}
    yts.add_to_stash(new_stash)

    yts.print_table(yts.stash_table)
    print()

    # expected: add to stash something not in yarns, producing an error
    print('*** Add to stash something not in yarns ***')
    new_stash = {'Brand Name': 'Malabrigo Rios', 'Color': 'gray', '# Skeins': 1, 'Total Length (yds)': None, 'Total Length (ms)': None, 'Total Weight (g)': None, 'Dye Lots': '' }
    yts.add_to_stash(new_stash)

    yts.print_table(yts.stash_table)
    print()

    # expected: update stash to decrease the # skeins by adding duplicate
    print('*** Decrease amount stashed of lion brand black ***')
    new_stash = {'Brand Name': 'lion brand', 'Color': 'black', '# Skeins': None, 'Total Length (yds)': 350, 'Total Length (ms)': None, 'Total Weight (g)': None, 'Dye Lots': ''}
    yts.add_to_stash(new_stash)

    yts.print_table(yts.stash_table)
    print()

    # expected: remove from stash by adding duplicate with no skeins, length, or weight
    print('*** Remove from stash ***')
    new_stash = {'Brand Name': 'lion brand', 'Color': 'black', '# Skeins': 0, 'Total Length (yds)': 0, 'Total Length (ms)': 0, 'Total Weight (g)': 0, 'Dye Lots': ''}
    yts.add_to_stash(new_stash)

    yts.print_table(yts.stash_table)
    print()

    print('----- Testing Completed -----')

if __name__ == '__main__':
    
    yt = setup()

    #test_yarn_table(yt)

    test_stash_table(yt)
