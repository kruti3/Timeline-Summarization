import os
import datefinder
import datetime


class Features:

        def __init__(self):
            
            self.DATA_PATH = "..\..\DataSet\Timeline17\Data"
            self.CURR_PATH = (os.path.dirname(__file__)).replace('/', '\\')

            self.INPUT_PATH = 'InputDocs'

            self.date_list = []
            self.feature_vector_list = []
            self.num_features = 6

        def create_feature_vector(self, topic_name):      

            self.create_date_list(topic_name)

            self.feature_vector_list = [[0 for x in range(self.num_features)] for y in range(len(self.date_list))]

            for one_date in self.date_list:
                root_path = os.path.join(self.CURR_PATH, self.DATA_PATH, topic_name, self.INPUT_PATH, one_date)
                
                number_of_files = 0 
                for root, directories, files in os.walk(root_path):
                    number_of_files = len(files)
                    for one_file in files:
                        self.update_featurevector(root_path, one_date, one_file)
                
                self.update_f1_feature(one_date, number_of_files)    
                '''
                self.update_f2_feature(one_date, len(files))
                self.update_f3_feature(one_date, len(files))
                '''
            return self.date_list, self.feature_vector_list

        def create_date_list(self, topic_name):

            root_path = os.path.join(self.CURR_PATH, self.DATA_PATH, topic_name, self.INPUT_PATH)

            for root, directories, files in os.walk(root_path):
                for directory in directories:
                    self.date_list.append(directory)

        def update_featurevector(self, root_path, date, filename):

            root_path = os.path.join(root_path, filename)
            file_obj = open(root_path, 'r')

            date_referred_list = self.extract_datereference(file_obj)
            
            self.update_f4_feature(date_referred_list, date)
            self.update_f5_feature(date_referred_list, date)
            self.update_f6_feature(date_referred_list, date)

            return date_referred_list

        def update_f1_feature(self, one_date, count):

            # Feature F1 indicates articles published on that date.
            if one_date in self.date_list:
                self.feature_vector_list[self.date_list.index(one_date)][0] = count

        def extract_datereference(self, file_obj):

            date_referred_list = []

            for line in file_obj:
                str1 = datefinder.find_dates(line)
                while True:
                        try:
                            one, flag = self.valid_date((str1.__iter__()).next())
                            if flag:
                                one_unaware = one.replace(tzinfo=None)
                                date_referred_list.append(one_unaware)
                        except ValueError:
                            continue
                        except StopIteration:
                            break

            return date_referred_list

        def valid_date(self, str1):

            if str1.year < 2000 or str1.year > 2015:
                return str1, 0

            if str1.month > 12 or str1.month < 1:
                return str1, 0

            if str1.date > 31 or str1.date < 1:
                return str1, 0


            return str1, 1
            pass
        
        def update_f4_feature(self, date_referred_list, datecurr):

            # sentences published on d and refer to d.

            datecurr_fmt = self.str_to_dtfmt(datecurr)
            
            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date, "%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if datecurr_fmt == one_date:
                            self.feature_vector_list[self.date_list.index(one_date_str)][3] += 1

        def update_f5_feature(self, date_referred_list, datecurr):

            # sentences published after d and refer to d.

            datecurr_fmt = self.str_to_dtfmt(datecurr)

            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date, "%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if datecurr_fmt > one_date:
                            self.feature_vector_list[self.date_list.index(one_date_str)][4] += 1

        def update_f6_feature(self, date_referred_list, datecurr):

            # sentences published before d and refer to d.

            datecurr_fmt = self.str_to_dtfmt(datecurr)

            for one_date in date_referred_list:
                if self.valid_date(one_date):
                    one_date_str = datetime.datetime.strftime(one_date, "%Y-%m-%d")
                    if one_date_str in self.date_list:
                        if datecurr_fmt < one_date:
                            self.feature_vector_list[self.date_list.index(one_date_str)][5] += 1

        def str_to_dtfmt(self, datecurr):

            year = int(datecurr[0:4])
            month = int(datecurr[5:7])
            date_n = int(datecurr[8:10])
            datecurr_fmt = datetime.datetime(year, month, date_n, 0, 0, 0, 0)

            return datecurr_fmt
