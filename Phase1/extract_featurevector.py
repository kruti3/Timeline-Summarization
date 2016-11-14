import os
import re
import datefinder
import datetime

class Features:

        def __init__(self):
            
            self.DATA_PATH = '\DataSet\Timeline17\Data'
            self.INPUT_PATH = 'InputDocs'

            self.date_list = []
            self.featurevector_list = []

        def create_featurevector(self, topic_name):      

            self.create_date_list(topic_name)

            self.featurevector_list = [[0 for x in range(6)] for y in range(len(self.date_list)) ] 

            for one_date in self.date_list:
                root_path = os.path.join(self.DATA_PATH, topic_name, self.INPUT_PATH, one_date)
                
                number_of_files = 0 
                for root, directories, files in os.walk(root_path):
                    number_of_files = len(files)
                    for one_file in files:
                        
                        self.update_featurevector(root_path, one_date, one_file)
                
                self.update_f1_feature(one_date, number_of_files)    
                #self.update_f2_feature(one_date, len(files))    
                #self.update_f3_feature(one_date, len(files))    

            return self.date_list, self.featurevector_list

        def create_date_list(self, topic_name):

            root_path = os.path.join(self.DATA_PATH, topic_name, self.INPUT_PATH)

            for root, directories, files in os.walk(root_path):
                for directory in directories:
                    self.date_list.append(directory)

        def update_featurevector(self, root_path, date, filename):

            root_path = os.path.join(root_path, filename)
            file_obj = open(root_path, 'r')

            date_referred_list = self.extract_datereferred(file_obj, filename)
            
            self.update_f4_feature(date_referred_list, date)
            self.update_f5_feature(date_referred_list, date)
            self.update_f6_feature(date_referred_list, date)

            return date_referred_list

        def update_f1_feature(self, one_date, count):

            #Feature F1 indicates articles published on that date.
            if one_date in self.date_list:
                self.featurevector_list[self.date_list.index(one_date)][0] = count

        def extract_datereferred(self, file_obj, date):

            date_referred_list = []
            
            for line in file_obj:
                str1 = datefinder.find_dates(line)
                
                for one in str1:
                    if self.valid_date(one):
                        one_unaware = one.replace(tzinfo=None)
                        date_referred_list.append(one_unaware)
              
            return date_referred_list

        def valid_date(self, str1):

            
            if str1.year < 2000 or str1.year > 2015:
                return 0

            if str1.month > 12 or str1.month < 1:
                return 0

            if str1.date > 31 or str1.date < 1:
                return 0
            return 1
            '''
            try:
                datetime.datetime.strftime(str1, "%Y-%m-%d")
               
            except ValueError:
                return 0
                pass
            except TypeError:
                return 0
                pass
            return 1'''
            pass
        
        def update_f4_feature(self, date_referred_list, datecurr):
            
            datecurr_fmt = self.str_to_dtfmt(datecurr)
            
            #sentences published on d and refer to d.
            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date,"%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if(datecurr_fmt == one_date) :
                            self.featurevector_list[self.date_list.index(one_date_str)][3] += 1

        def update_f5_feature(self, date_referred_list, datecurr):
            
            datecurr_fmt = self.str_to_dtfmt(datecurr)

            #sentences published after d and refer to d.
            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date,"%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if(datecurr_fmt > one_date) :
                            self.featurevector_list[self.date_list.index(one_date_str)][4] += 1


        def update_f6_feature(self, date_referred_list, datecurr):

            datecurr_fmt = self.str_to_dtfmt(datecurr)

            #sentences published before d and refer to d.
            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date,"%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if(datecurr_fmt < one_date) :
                            self.featurevector_list[self.date_list.index(one_date_str)][5] += 1

        def str_to_dtfmt(self, datecurr):

            year = int(datecurr[0:4])
            month = int(datecurr[5:7])
            date_n = int(datecurr[8:10])
            datecurr_fmt = datetime.datetime(year, month, date_n,0,0,0,0)

            return datecurr_fmt
