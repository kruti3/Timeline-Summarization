import os
import extract_featurevector
import extract_goldlabels
from sklearn import linear_model
from sklearn import metrics 
import pickle


class DateExtraction:

    def __init__(self):
            
            self.DATA_PATH = '..\..\DataSet\Timeline17\Data'
            self.METADATA_PATH = '..\..\DataSet\Timeline17\MetaData'
            self.CURR_PATH = (os.path.dirname(__file__)).replace('/', '\\')

            self.topic_list = ['bpoil_bbc', 'bpoil_foxnews', 'bpoil_guardian', 'bpoil_reuters', 'bpoil_washingtonpost',
                               'EgyptianProtest_cnn', 'Finan_washingtonpost', 'H1N1_bbc', 'H1N1_guardian',
                               'H1N1_reuters', 'haiti_bbc', 'IraqWar_guardian', 'LibyaWar_cnn', 'LibyaWar_reuters',
                               'MJ_bbc', 'SyrianCrisis_bbc', 'SyrianCrisis_reuters']
            '''
            Finan_washingtonpost:1235.txt:ThirdLine:The technology-heavy Nasdaq composite index slid 9.14 percent ,
            or 199.61 , to 1983.73 , and the broader Standard & Poor 's 500-stock index lost 8.79 percent , or 106.62 ,
            to close at 1106.39 .
            Egyptian protest cnn: Output.txt
            removed 2011-02-12
            '''
            self.date_list = []
            self.gold_label = []
            self.feature_vector_list = []

            self.clf = linear_model.LogisticRegression()

    def create_metadata(self):

        metadata_path = os.path.join(self.CURR_PATH, self.METADATA_PATH)
        feat = extract_featurevector.Features()
        output_var = extract_goldlabels.GoldLabel()

        for directory in self.topic_list:

                if  not (os.path.isfile(metadata_path + '\\' + directory + 'date_list.txt') & os.path.isfile(metadata_path + '\\' + directory + 'feature_vector.txt')):
                    print "Getting feature vector for ", directory
                    date_list, feature_vector_list = feat.create_feature_vector(directory)
                    output = open(metadata_path + '\\' + directory + 'date_list.txt', 'wb')
                    pickle.dump(date_list, output)
                    output.close()

                    output = open(metadata_path + '\\' + directory + 'feature_vector.txt', 'wb')
                    pickle.dump(feature_vector_list, output)
                    output.close()

                if not os.path.isfile(metadata_path + '\\' + directory + 'gold_label.txt'):
                    print "Getting gold labels for ", directory
                    input1 = open('{0}\\{1}date_list.txt'.format(metadata_path, directory), 'rb')
                    date_list = pickle.load(input1)
                    input1.close()

                    gold_label = output_var.get_goldlabel(directory, date_list)

                    output = open(metadata_path + '\\' + directory + 'gold_label.txt', 'wb')
                    pickle.dump(gold_label, output)
                    output.close()

        pass

    def get_data(self, test_data):

        root_path = os.path.join(self.CURR_PATH, self.METADATA_PATH)

        for directory in self.topic_list:

            input1 = open('{0}\\{1}date_list.txt'.format(root_path, directory), 'rb')
            date_list = pickle.load(input1)
            input1.close()

            input1 = open('{0}\\{1}feature_vector.txt'.format(root_path, directory), 'rb')
            feature_vector_list = pickle.load(input1)
            input1.close()

            input1 = open('{0}\\{1}gold_label.txt'.format(root_path, directory), 'rb')
            gold_label = pickle.load(input1)
            input1.close()

            if directory != test_data:
                    print "Training on ", directory
                    self.train_classifier(feature_vector_list, gold_label)
            else:
                    self.feature_vector_list = feature_vector_list
                    self.date_list = date_list
                    self.gold_label = gold_label

    def train_classifier(self, feature_vector_list, gold_label):

        self.clf.fit(feature_vector_list, gold_label)

        pass

    def test_classifier(self):

        predict_vector = self.clf.predict(self.feature_vector_list)
        acc = metrics.accuracy_score(self.gold_label, predict_vector)
        print "Accuracy Score", acc

        return acc
        pass

if __name__ == '__main__':
    test = DateExtraction()
    test.create_metadata()

    acc = 0
    for test_data in test.topic_list:
        test.get_data(test_data)
        print "Predicting for", test_data
        acc += test.test_classifier()

    acc = acc*1.0/len(test.topic_list)
    print "Average Accuracy Score", acc
