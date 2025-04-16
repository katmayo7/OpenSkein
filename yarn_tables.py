import pandas as pd
import os

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
            self.yarns_table = pd.DataFrame(columns=['Brand Name', 'Color', 'Material', 'Yarn Weight', 'Length/Skein (yds)', 'Length/Skein (ms)', 'Weight/Skein (g)', 'Machine Washable', 'Notes'])
            yarn_types = {'Brand Name': 'str', 'Color': 'str', 'Material': 'str', 'Yarn Weight': 'int', 'Length/Skein (yds)': 'float', 'Length/Skein (ms)': 'float', 'Weight/Skein (g)': 'float', 'Machine Washable': 'bool', 'Notes': 'str'}
            self.yarns_table = self.yarns_table.astype(yarn_types)
            self.stash_table = pd.DataFrame(columns=['Brand Name', 'Color', '# Skeins', 'Total Length (yds)', 'Total Length (ms)', 'Total Weight (g)', 'Dye Lots'])
            stash_types = {'Brand Name': 'str', 'Color': 'str', '# Skeins': 'float', 'Total Length (yds)': 'float', 'Total Length (ms)': 'float', 'Total Weight (g)': 'float', 'Dye Lots': 'str'}
            self.stash_table = self.stash_table.astype(stash_types)
        
    def save_data(self):
        if not os.path.exists(self.yarns_file):
            os.mkdir('data/')
        
        self.yarns_table.to_pickle(self.yarns_file)
        self.stash_table.to_pickle(self.stash_file)
    
    def print_table(self, table):
        print('**********************************************************************************************************')

        print_cols = []
        if self.metric:
            print_cols = [c for c in table.columns if '(yds)' not in c]
        else:
            print_cols = [c for c in table.columns if '(ms)' not in c]
        
        print(table[print_cols])
            
        print('**********************************************************************************************************')
    
    def get_yarn(self):

        return self.yarns_table
    
    def get_stash(self):

        return self.stash_table
    
    # check if a yarn with this brand and color has previously been logged
    def check_exists(self, table, brand, color):
        tmp_i = table[(table['Brand Name'] == brand.lower()) & (table['Color'] == color.lower())].index.tolist()
        
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
    def add_helper(self, table, new_data):
        # enforce lower case for string entries
        text_fields = list(table.select_dtypes(include='object').columns)
        for t in text_fields:
            new_data[t] = new_data[t].lower()
        
        tmp_i = self.check_exists(table, new_data['Brand Name'], new_data['Color'])

        if tmp_i > -1:
            print('!! It looks like you are trying to add a duplicate. This yarn is already logged as:')
            print(table.loc[tmp_i])
            print()
            
            info_diff = {}
            for col in table.columns:
                if new_data[col] != table.loc[tmp_i][col]:
                    info_diff[col] = new_data[col]
            
            if len(info_diff) == 0:
                print('There is no information to update.')
                return None
            
            # TO DO: make the update optional -- also maybe make on case by case basis for each set of info
            # print('Would you like to update the entry with the following information?')
            print('You are updating the following information:')
            for i in info_diff:
                print('{0}: {1}'.format(i, info_diff[i]))
            
            print('** Note: dye lots and notes will be combined between new and updated versions. **')
            
            # TO DO: offer option to completely overwrite notes, for example if dye lots used up we might actually want to delete some
            if 'Notes' in table.columns and table.iloc[tmp_i]['Notes'] != new_data['Notes']:
                new_data['Notes'] = self.format_long_form(table.loc[tmp_i]['Notes'], new_data['Notes'])
            elif 'Dye Lots' in table.columns and table.loc[tmp_i]['Dye Lots'] != new_data['Dye Lots']:
                new_data['Dye Lots'] = self.format_long_form(table.loc[tmp_i]['Dye Lots'], new_data['Dye Lots'])

            self.remove_table_entry(table, remove_i=tmp_i)

        return new_data

    def add_to_yarn(self, new_data):
        # format, check for duplicates
        new_data = self.add_helper(self.yarns_table, new_data)
        if new_data == None:
            return
        
        self.yarns_table.loc[len(self.yarns_table)] = new_data
    
    def add_to_stash(self, new_data):
        # make sure yarn exists in Yarn database
        yarn_i = self.check_exists(self.yarns_table, new_data['Brand Name'], new_data['Color'])

        if yarn_i == -1:
            print('!! Error, must add to yarn database before yarn can be stashed!')
            # TO DO: collect info to add it to the yarn data base
            return
        
        # format, check for duplicates
        new_data = self.add_helper(self.stash_table, new_data)

        # if nothing ot update or updating with 0 for all amount info (really a removal from stash)
        if new_data == None or (new_data['# Skeins'] == 0 and new_data['Total Length (yds)'] == 0 and new_data['Total Length (ms)'] == 0 and new_data['Total Weight (g)'] == 0):
            return
        
        # if only given subset of # skeins, total length, total weight, use given info to calculate remaining using yarn info

        yds_per_skein = self.yarns_table.loc[yarn_i]['Length/Skein (yds)']
        ms_per_skein = self.yarns_table.loc[yarn_i]['Length/Skein (ms)']
        gs_per_skein = self.yarns_table.loc[yarn_i]['Weight/Skein (g)']

        # calculate # skeins
        if new_data['# Skeins'] == None:
            if new_data['Total Length (yds)'] != None:
                new_data['# Skeins'] = new_data['Total Length (yds)'] / yds_per_skein
            elif new_data['Total Length (ms)'] != None:
                new_data['# Skeins'] = new_data['Total Length (ms)'] / ms_per_skein
            else:
                new_data['# Skeins'] = new_data['Total Weight (g)'] / gs_per_skein
        
        # use # skeins to calculate remaineder
        if new_data['Total Length (yds)'] == None:
            new_data['Total Length (yds)'] = new_data['# Skeins'] * yds_per_skein
        if new_data['Total Length (ms)'] == None:
            new_data['Total Length (ms)'] = new_data['# Skeins'] * ms_per_skein
        if new_data['Total Weight (g)'] == None:
            new_data['Total Weight (g)'] = new_data['# Skeins'] * gs_per_skein
       
        self.stash_table.loc[len(self.stash_table)] = new_data

    def remove_table_entry(self, table, remove_i=None, remove_brand=None, remove_color=None):
        if remove_brand != None:
            remove_i = self.check_exists(table, remove_brand, remove_color)
        
        table.drop(remove_i, inplace=True)
