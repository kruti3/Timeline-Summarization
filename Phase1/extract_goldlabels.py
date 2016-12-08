import os
import re


class GoldLabel:
    def __init__(self):

        self.DATA_PATH = '..\..\DataSet\Timeline17\Data'
        self.OUTPUT_PATH = 'timelines'
        self.CURR_PATH = (os.path.dirname(__file__)).replace('/', '\\')
        self.INPUT_PATH = 'InputDocs'
        self.OUTPUT_VECTOR = []

    def get_goldlabel(self, topic_name, date_list=[]):

        root_path = os.path.join(self.CURR_PATH, self.DATA_PATH, topic_name, self.OUTPUT_PATH)

        if len(date_list) == 0:
            self.create_date_list(topic_name, date_list)

        self.OUTPUT_VECTOR = [0] * len(date_list)

        for root, directories, files in os.walk(root_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                self.update_from_file(file_path, date_list)

        return self.OUTPUT_VECTOR

    def create_date_list(self, topic_name, date_list):

        root_path = os.path.join(self.CURR_PATH, self.DATA_PATH, topic_name, self.INPUT_PATH)

        for root, directories, files in os.walk(root_path):
            for directory in directories:
                date_list.append(directory)

    def update_from_file(self, file_path, date_list):

        file_obj = open(file_path, 'r')

        for line in file_obj:
            str1 = re.findall('\d{4}-\d{2}-\d{2}', line)
            for one in str1:
                if one in date_list:
                    self.OUTPUT_VECTOR[date_list.index(one)] = 1

# if __name__ == '__main__':
#    test = GoldLabel()
#    print test.get_goldlabel('bpoil_bbc')
