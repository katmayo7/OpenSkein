import pandas as pd
import os
import datetime as dt

class YarnTables:

    def __init__(self, metric=False):
        self.yarns_file = 'data/yarns_table.pkl'
        self.stash_file = 'data/stash_table.pkl'

        self.metric = metric

        self.yarns_table = None
        self.stash_table = None

    def load_data(self):
        if os.path.exists(self.yarns_file):
            print('Reading in old tables.')
            self.yarns_table = pd.read_pickle(self.yarns_file)
            self.stash_table = pd.read_pickle(self.stash_file)
        else:
            self.yarns_table = pd.DataFrame(columns=['DATE ADDED', 'LAST UPDATED', 'BRAND NAME', 'COLOR', 'MATERIAL', 'YARN WEIGHT', 'LENGTH/SKEIN (YDS)', 'LENGTH/SKEIN (MS)', 'WEIGHT/SKEIN (G)', 'MACHINE WASHABLE', 'NOTES'])
            yarn_types = {'BRAND NAME': 'str', 'COLOR': 'str', 'MATERIAL': 'str', 'YARN WEIGHT': 'int', 'LENGTH/SKEIN (YDS)': 'float', 'LENGTH/SKEIN (MS)': 'float', 'WEIGHT/SKEIN (G)': 'float', 'MACHINE WASHABLE': 'bool', 'NOTES': 'str'}
            self.yarns_table = self.yarns_table.astype(yarn_types)
            self.yarns_table['DATE ADDED'] = pd.to_datetime(self.yarns_table['DATE ADDED'])
            self.yarns_table['LAST UPDATED'] = pd.to_datetime(self.yarns_table['LAST UPDATED'])
            
            self.stash_table = pd.DataFrame(columns=['DATE ADDED', 'LAST UPDATED', 'BRAND NAME', 'COLOR', '# SKEINS', 'TOTAL LENGTH (YDS)', 'TOTAL LENGTH (MS)', 'TOTAL WEIGHT (G)', 'DYE LOTS'])
            stash_types = {'BRAND NAME': 'str', 'COLOR': 'str', '# SKEINS': 'float', 'TOTAL LENGTH (YDS)': 'float', 'TOTAL LENGTH (MS)': 'float', 'TOTAL WEIGHT (G)': 'float', 'DYE LOTS': 'str'}
            self.stash_table = self.stash_table.astype(stash_types)
            self.stash_table['DATE ADDED'] = pd.to_datetime(self.stash_table['DATE ADDED'])
            self.stash_table['LAST UPDATED'] = pd.to_datetime(self.stash_table['LAST UPDATED'])
        
    def save_data(self):
        if not os.path.exists(self.yarns_file):
            os.mkdir('data/')
        
        self.yarns_table.to_pickle(self.yarns_file)
        self.stash_table.to_pickle(self.stash_file)
    
    def print_table(self, table):
        print('**************************************************************************************************************************************************')

        print_cols = []
        if self.metric:
            print_cols = [c for c in table.columns if '(YDS)' not in c]
        else:
            print_cols = [c for c in table.columns if '(MS)' not in c]
        
        print(table[print_cols])  
        print('**************************************************************************************************************************************************')
    
    def get_yarn(self):

        return self.yarns_table
    
    def get_stash(self):

        return self.stash_table
    
    # check if a yarn with this brand and color has previously been logged
    def check_exists(self, table, brand, color):
        tmp_i = table[(table['BRAND NAME'] == brand.lower()) & (table['COLOR'] == color.lower())].index.tolist()
        
        if len(tmp_i) > 1:
            print('!! Error: More than one entry matches this brand name and color??')
        
        if len(tmp_i) > 0:
            return tmp_i[0]
        
        return -1
    
    # allows for extending a text field with more information (ex: dye lots, notes), but ignroing duplicates
    def format_long_form(self, one, two):
        set1 = set(one.split(','))
        set2 = set(two.split(','))

        union = list(set1.union(set2))
        union = [s + ',' for s in union]

        return ''.join(union)
    
    # see if duplicate entry and overwrite old one if desired
    def add_helper(self, table, new_data, testing):
        # enforce lower case for string entries
        text_fields = list(table.select_dtypes(include='object').columns)
        for t in text_fields:
            new_data[t] = new_data[t].lower()
        
        tmp_i = self.check_exists(table, new_data['BRAND NAME'], new_data['COLOR'])

        if tmp_i > -1:
            print('!! It looks like you are trying to add a duplicate. This yarn is already logged as:')
            print(table.loc[tmp_i])
            print()
            
            info_diff = {}
            print('You are updating the following information for the entry:')
            for col in table.columns:
                # don't want to consider if the new entry doesn't have info for something as being "different" and requiring an update
                if col not in ['DATE ADDED', 'LAST UPDATED'] and new_data[col] != table.loc[tmp_i][col] and new_data[col] != None:
                    info_diff[col] = new_data[col]
                    print(col, ': ', info_diff[col] )
                    
                    # allow for case-by-case handling of text field data (might want to totally overwrite it or might just want to add more thoughts/dye lots)
                    if (col == 'NOTES' or col == 'DYE LOTS') and not testing:
                        result = None
                        while result != 'overwrite' and result != 'extend':
                            result = input('For this text field, would you like to overwrite or extend the previously logged notes (overwrite/extend): ').lower()
                    
                        if result == 'extend' and col == 'NOTES':
                            info_diff[col] = self.format_long_form(table.loc[tmp_i]['NOTES'], new_data['NOTES'])
                        elif result == 'extend' and col == 'DYE LOTS':
                            info_diff[col] = self.format_long_form(table.loc[tmp_i]['DYE LOTS'], new_data['DYE LOTS'])
                    elif col == 'NOTES' and testing:
                        info_diff[col] = self.format_long_form(table.loc[tmp_i]['NOTES'], new_data['NOTES'])
                    elif col == 'DYE LOTS' and testing:
                        info_diff[col] = self.format_long_form(table.loc[tmp_i]['DYE LOTS'], new_data['DYE LOTS'])

            if len(info_diff) == 0:
                print('There is no information to update.')
                return None,tmp_i
            
            return info_diff,tmp_i

        return new_data,-1

    def add_to_yarn(self, new_data, testing=False):
        # format, check for duplicates
        new_data,i = self.add_helper(self.yarns_table, new_data, testing)
        if new_data == None:
            return

        print(new_data)
        
        # calculate meters from yards or vice versa if only one is provided
        yds_per_m = 1.09361
        ms_per_yd = 0.9144

        if 'LENGTH/SKEIN (YDS)' in new_data and new_data['LENGTH/SKEIN (YDS)'] == None:
            new_data['LENGTH/SKEIN (YDS)'] = new_data['LENGTH/SKEIN (MS)'] * yds_per_m
        elif 'LENGTH/SKEIN (MS)' in new_data and new_data['LENGTH/SKEIN (MS)'] == None:
            new_data['LENGTH/SKEIN (MS)'] = new_data['LENGTH/SKEIN (YDS)'] * ms_per_yd
        
        # update or new data entry
        new_data['LAST UPDATED'] = dt.date.today()
        new_data['LAST UPDATED'] = pd.to_datetime(new_data['LAST UPDATED'])

        if i > -1:
            for nd in new_data:
                self.yarns_table.loc[i, nd] = new_data[nd]
        else:
            new_data['DATE ADDED'] = dt.date.today()
            new_data['DATE ADDED'] = pd.to_datetime(new_data['DATE ADDED'])
            self.yarns_table.loc[len(self.yarns_table)] = new_data
    
    def add_to_stash(self, new_data, testing=False):
        # make sure yarn exists in Yarn database
        yarn_i = self.check_exists(self.yarns_table, new_data['BRAND NAME'], new_data['COLOR'])

        if yarn_i == -1:
            print('** Error, must add to yarn database before yarn can be stashed! **')
            return
        
        # format, check for duplicates
        new_data,i = self.add_helper(self.stash_table, new_data, testing)

        # if nothing to update
        if new_data == None:
            return
        
        # removal of something already in stash
        if new_data['# SKEINS'] == 0 and new_data['TOTAL LENGTH (YDS)'] == 0 and new_data['TOTAL LENGTH (MS)'] == 0 and new_data['TOTAL WEIGHT (G)'] == 0:
            print('Updating all measures to 0. Removing from stash.')
            self.remove_table_entry(self.stash_table, remove_i = i)
            return
        
        # if updating ensure all methods of measurements included
        measurements = ['# SKEINS', 'TOTAL LENGTH (YDS)', 'TOTAL LENGTH (MS)', 'TOTAL WEIGHT (G)']
        for m in measurements:
            if m not in new_data:
                new_data[m] = None
            elif new_data[m] != None:
                new_data[m] = float(new_data[m])
        
        # if only given subset of # skeins, total length, total weight, use given info to calculate remaining using yarn info
        yds_per_skein = self.yarns_table.loc[yarn_i]['LENGTH/SKEIN (YDS)']
        ms_per_skein = self.yarns_table.loc[yarn_i]['LENGTH/SKEIN (MS)']
        gs_per_skein = self.yarns_table.loc[yarn_i]['WEIGHT/SKEIN (G)']

        # calculate # skeins
        if new_data['# SKEINS'] == None:
            if new_data['TOTAL LENGTH (YDS)'] != None:
                new_data['# SKEINS'] = float(new_data['TOTAL LENGTH (YDS)'] / yds_per_skein)
            elif new_data['TOTAL LENGTH (MS)'] != None:
                new_data['# SKEINS'] = float(new_data['TOTAL LENGTH (MS)'] / ms_per_skein)
            else:
                new_data['# SKEINS'] = float(new_data['TOTAL WEIGHT (G)'] / gs_per_skein)
        
        # use # skeins to calculate remaineder
        if new_data['TOTAL LENGTH (YDS)'] == None:
            new_data['TOTAL LENGTH (YDS)'] = float(new_data['# SKEINS'] * yds_per_skein)
        if new_data['TOTAL LENGTH (MS)'] == None:
            new_data['TOTAL LENGTH (MS)'] = float(new_data['# SKEINS'] * ms_per_skein)
        if new_data['TOTAL WEIGHT (G)'] == None:
            new_data['TOTAL WEIGHT (G)'] = float(new_data['# SKEINS'] * gs_per_skein)

        # update existing or add new entry
        new_data['LAST UPDATED'] = dt.date.today()
        new_data['LAST UPDATED'] = pd.to_datetime(new_data['LAST UPDATED'])

        if i > -1:
            for nd in new_data:
                self.stash_table.loc[i, nd] = new_data[nd]
        else:
            new_data['DATE ADDED'] = dt.date.today()
            new_data['DATE ADDED'] = pd.to_datetime(new_data['DATE ADDED'])
            self.stash_table.loc[len(self.stash_table)] = new_data
        
    def remove_table_entry(self, table, remove_i=None, remove_brand=None, remove_color=None):
        if remove_brand != None:
            remove_i = self.check_exists(table, remove_brand, remove_color)
        
        table.drop(remove_i, inplace=True)
