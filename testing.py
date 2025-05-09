import yarn_tables

def setup():
    yt = yarn_tables.YarnTables()
    yt.load_data()

    return yt

# test that yarn table behaves as desired
def test_yarn_table(yts, print_info=True):
    
    # expected: add yarn to table
    print('*** Adding Lion Brand black ***')
    new_yarn = {'BRAND NAME': 'Lion Brand', 'COLOR': 'black', 'MATERIAL': 'polyester', 'YARN WEIGHT': 3, 'LENGTH/SKEIN (YDS)': 300, 'LENGTH/SKEIN (MS)': None, 'WEIGHT/SKEIN (G)': 100, 'MACHINE WASHABLE': False, 'NOTES': 'very dark'}
    yts.add_to_yarn(new_yarn, testing=True)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()
    
    # expected: update the information
    print('*** Updating info for Lion Brand black ***')
    new_yarn = {'BRAND NAME': 'Lion brand', 'COLOR': 'black', 'MATERIAL': 'polyester', 'YARN WEIGHT': 3, 'LENGTH/SKEIN (YDS)': 400, 'LENGTH/SKEIN (MS)': None, 'WEIGHT/SKEIN (G)': 150, 'MACHINE WASHABLE': False, 'NOTES': 'nice to work with'}
    yts.add_to_yarn(new_yarn, testing=True)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()
    
    # expected: add yarn to table
    print('*** Adding Caron Heart red **')
    new_yarn = {'BRAND NAME': 'Caron Heart', 'COLOR': 'red', 'MATERIAL': '50% acyrlic, 50% cotton', 'YARN WEIGHT': 5, 'LENGTH/SKEIN (YDS)': 300, 'LENGTH/SKEIN (MS)': 250, 'WEIGHT/SKEIN (G)': 150, 'MACHINE WASHABLE': True, 'NOTES': ''}
    yts.add_to_yarn(new_yarn, testing=True)

    if print_info:
        yts.print_table(yts.yarns_table)
        print()
    
    # always print the final table at the end
    if not print_info:
        yts.print_table(yts.yarns_table)
        print()
    
    print('---------- Testing Yarn Table Completed ----------')
    print()

# test that stash table behaves as desired -- requires yarn table to be popualted to work
def test_stash_table(yts):

    test_yarn_table(yts, print_info=False)

    # expected: add to stash and fill in total weight (also total length in ms, but that won't be shown)
    print('*** Add lion brand black to stash -- should calculate the total weight')
    new_stash = {'BRAND NAME': 'lion brand', 'COLOR': 'black', '# SKEINS': 2, 'TOTAL LENGTH (YDS)': 100, 'TOTAL LENGTH (MS)': None, 'TOTAL WEIGHT (G)': None, 'DYE LOTS': 'xyz' }
    yts.add_to_stash(new_stash, testing=True)

    yts.print_table(yts.stash_table)
    print()

    # expected: update stash to increase # of skeins by adding duplicate (total length and number of skeins should increase)
    print('*** Increase amount of lion brand black in stash -- # skeins and length should increase as result')
    new_stash = {'BRAND NAME': 'lion brand', 'COLOR': 'black', '# SKEINS': None, 'TOTAL LENGTH (YDS)': None, 'TOTAL LENGTH (MS)': None, 'TOTAL WEIGHT (G)': 500, 'DYE LOTS': 'xyz, abc'}
    yts.add_to_stash(new_stash, testing=True)

    yts.print_table(yts.stash_table)
    print()

    # expected: add to stash something not in yarns, producing an error
    print('*** Add to stash something not in yarns ***')
    new_stash = {'BRAND NAME': 'Malabrigo Rios', 'COLOR': 'gray', '# SKEINS': 1, 'TOTAL LENGTH (YDS)': None, 'TOTAL LENGTH (MS)': None, 'TOTAL WEIGHT (G)': None, 'DYE LOTS': '' }
    yts.add_to_stash(new_stash, testing=True)

    yts.print_table(yts.stash_table)
    print()

    # expected: update stash to decrease the # skeins by adding duplicate
    print('*** Decrease amount stashed of lion brand black ***')
    new_stash = {'BRAND NAME': 'lion brand', 'COLOR': 'black', '# SKEINS': None, 'TOTAL LENGTH (YDS)': 150, 'TOTAL LENGTH (MS)': None, 'TOTAL WEIGHT (G)': None, 'DYE LOTS': ''}
    yts.add_to_stash(new_stash, testing=True)

    yts.print_table(yts.stash_table)
    print()

    # expected: remove from stash by adding duplicate with no skeins, length, or weight
    print('*** Remove from stash ***')
    new_stash = {'BRAND NAME': 'lion brand', 'COLOR': 'black', '# SKEINS': 0, 'TOTAL LENGTH (YDS)': 0, 'TOTAL LENGTH (MS)': 0, 'TOTAL WEIGHT (G)': 0, 'DYE LOTS': ''}
    yts.add_to_stash(new_stash, testing=True)

    yts.print_table(yts.stash_table)
    print()

    print('----- Testing Stash Table Completed -----')
    print()

if __name__ == '__main__':
    
    yt = setup()

    #test_yarn_table(yt)

    test_stash_table(yt)
