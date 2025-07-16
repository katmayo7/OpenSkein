import yarn_tables
import pattern_and_proj_tables

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

def setup_patt_and_proj():
    pt = pattern_and_proj_tables.PatternProjTables()
    pt.load_data()

    return pt
    
def test_pattern_table(pts):
        
    # expected: add to pattern table, filling in the meters appropriately
    print('*** Add to pattern table ***')
    new_item = {'PATTERN NAME': 'winter hat', 'SUGGESTED YARN WEIGHT': 4, 'SUGGESTED HOOK SIZE': 5.0, 'TOTAL AMOUNT OF YARN (YDS)': 100.0, 'TOTAL AMOUNT OF YARN (MS)': None, 'CATEGORY': 'wearables', 'NOTES': 'comfortable and looks good', 'SOURCE': 'https://test.com'}
    pts.add_to_pattern(new_item, True)

    pts.print_table(pts.pattern_table)
    print()

    # expected: add to pattern table, filling yards appropriately
    print('*** Add to pattern table ***')
    new_item = {'PATTERN NAME': 'summer top', 'SUGGESTED YARN WEIGHT': 2, 'SUGGESTED HOOK SIZE': 3.5, 'TOTAL AMOUNT OF YARN (YDS)': None, 'TOTAL AMOUNT OF YARN (MS)': 400.0, 'CATEGORY': 'top', 'NOTES': '', 'SOURCE': 'Fun Summer Tops Book'}
    pts.add_to_pattern(new_item, True)

    pts.print_table(pts.pattern_table)
    print()

    # expected: update pattern entry information
    print('*** Update summer top pattern hook size and category***')
    new_item = {'PATTERN NAME': 'summer top', 'SUGGESTED YARN WEIGHT': 2, 'SUGGESTED HOOK SIZE': 4.0, 'TOTAL AMOUNT OF YARN (YDS)': None, 'TOTAL AMOUNT OF YARN (MS)': 400.0, 'CATEGORY': 'wearables', 'NOTES': '', 'SOURCE': 'Fun Summer Tops Book'}
    pts.add_to_pattern(new_item, True)

    pts.print_table(pts.pattern_table)
    print()

    # expected: add duplicate pattern, which should not change the table
    print('*** Add duplicate of the winter hat pattern ***')
    new_item = {'PATTERN NAME': 'winter hat', 'SUGGESTED YARN WEIGHT': 4, 'SUGGESTED HOOK SIZE': 5, 'TOTAL AMOUNT OF YARN (YDS)': 100, 'TOTAL AMOUNT OF YARN (MS)': None, 'CATEGORY': 'wearables', 'NOTES': 'comfortable and looks good', 'SOURCE': 'https://test.com'}
    pts.add_to_pattern(new_item, True)

    pts.print_table(pts.pattern_table)
    print()

    # expected: remove winter hat from pattern table
    print('*** Remove winter hat pattern ***')
    pts.remove_table_entry(pts.pattern_table, remove_name='winter hat')

    pts.print_table(pts.pattern_table)
    print()

    print('----- Testing Pattern Table Completed -----')
    print()

def test_project_table(pts):
    # expected: add a new project calculate the total amount of yarn ms
    print('*** Add to project table ***')
    new_item = {'PROJECT NAME': 'winter hat', 'PATTERN NAME': 'cozy winter hats', 'YARN(S) USED (BRAND+COLOR)': 'lion brand wool ease blue; lion brand wood ease yellow', 'YARN WEIGHT': 3, 'AMOUNT OF YARN (PER YARN)': '100; 100', 'TOTAL AMOUNT OF YARN (YDS)': 200.0, 'TOTAL AMOUNT OF YARN (MS)': None, 'DYE LOTS (PER YARN)': 'abc; afj', 'HOOK SIZE USED': 5.0, 'NOTES': 'a little big'}
    pts.add_to_project(new_item, True)

    pts.print_table(pts.project_table)
    print()

    # expected: add a new project calculate the total amount of yarn yds
    print('*** Add new project ***')
    new_item = {'PROJECT NAME': 'mom placemat gift', 'PATTERN NAME': 'easy placemats', 'YARN(S) USED (BRAND+COLOR)': 'lily sugar and cream blue; lily sugar and cream yellow', 'YARN WEIGHT': 4, 'AMOUNT OF YARN (PER YARN)': '500; 500', 'TOTAL AMOUNT OF YARN (YDS)': None, 'TOTAL AMOUNT OF YARN (MS)': 1000.0, 'DYE LOTS (PER YARN)': '', 'HOOK SIZE USED': 4.0, 'NOTES': ''}
    pts.add_to_project(new_item, True)

    pts.print_table(pts.project_table)
    print()

    # expected: add a duplicate doesn't change things
    print('*** Add duplicate ***')
    new_item = {'PROJECT NAME': 'winter hat', 'PATTERN NAME': 'cozy winter hats', 'YARN(S) USED (BRAND+COLOR)': 'lion brand wool ease blue; lion brand wood ease yellow', 'YARN WEIGHT': 3, 'AMOUNT OF YARN (PER YARN)': '100; 100', 'TOTAL AMOUNT OF YARN (YDS)': 200.0, 'TOTAL AMOUNT OF YARN (MS)': None, 'DYE LOTS (PER YARN)': 'abc; afj', 'HOOK SIZE USED': 5.0, 'NOTES': 'a little big'}
    pts.add_to_project(new_item, True)

    pts.print_table(pts.project_table)
    print()

    # expected: update the hook size and yarn weight of an existing entry
    print('*** Update total amount of yarn for winter hat ***')
    new_item = {'PROJECT NAME': 'winter hat', 'PATTERN NAME': 'cozy winter hats', 'YARN(S) USED (BRAND+COLOR)': 'lion brand wool ease blue; lion brand wood ease yellow', 'YARN WEIGHT': 3, 'AMOUNT OF YARN (PER YARN)': '100; 100', 'TOTAL AMOUNT OF YARN (YDS)': 225.0, 'TOTAL AMOUNT OF YARN (MS)': None, 'DYE LOTS (PER YARN)': 'abc; afj', 'HOOK SIZE USED': 5.0, 'NOTES': 'a little big'}
    pts.add_to_project(new_item, True)

    pts.print_table(pts.project_table)
    print()

    # expected: remove 
    print('*** Remove placemats ***')
    pts.remove_table_entry(pts.project_table, remove_name='winter hat', pattern_search=False)

    pts.print_table(pts.project_table)
    print()

    print('----- Testing Pattern Table Completed -----')
    print()

if __name__ == '__main__':
    
    #yt = setup()

    #test_yarn_table(yt)

    #test_stash_table(yt)

    pt = setup_patt_and_proj()

    #test_pattern_table(pt)

    test_project_table(pt)

