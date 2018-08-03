import math

from StructureBuilder import structure_builder
import csv


class model_builder:
    def __init__(self):
        self.struct = structure_builder()
        self.probability_attribute_to_yes = {}
        self.probability_attribute_to_no = {}
        self.testData = []

    # Pre Processing Functions

    def pre_processing(self, data):
        """Goes through all the dataBase and fills empty entry's"""
        for col in range(len(self.struct.attributes) - 1):
            self.fill_blanks(col, data)

    def fill_blanks(self, col, data):
        """ Fill the blanks in "lines" using get_avg & get_most_common functions"""
        if self.struct.structure[data[0][col]] == 'NUMERIC':
            avg = self.get_avg(col, data)
            for row in range(1, len(data)):
                if data[row][col] == '':
                    data[row][col] = avg
                else:
                    # changes the value to avg value if the value is incorrect type using exception thrown by convert
                    try:
                        int(data[row][col])
                    except ValueError:
                        data[row][col] = avg
        else:
            most_common = self.get_most_common(col, data)
            for row in range(1, len(data)):
                if data[row][col] == '':
                    data[row][col] = most_common
                # check if value is correct value to attribute else puts the most common
                if data[row][col] not in self.struct.structure[data[0][col]]:
                    data[row][col] = most_common

    def get_avg(self, col, data):
        """ Return avg of column that contains Numbers as NUMERIC """
        if self.struct.structure[data[0][col]] == 'NUMERIC':
            sum = 0
            avg = 0
            for row in range(1, len(data)):
                if data[row][col] != '':
                    try:
                        # Ignores convert failure
                        sum = sum + float(data[row][col])
                    except ValueError:
                        pass
            avg = float(sum) / len(data)
            return avg

    def get_most_common(self, col, data):
        """ Returns Most Common Value in column """
        val = data[0][col]
        most_common_counter = 0
        temp_common_counter = 0
        most_common_val = self.struct.structure[val][0]
        for name in self.struct.structure[val]:
            for row in range(1, len(data)):
                if data[row][col] != '':
                    if data[row][col] == name:
                        temp_common_counter = temp_common_counter + 1
            print 'Check: ', name, 'Times: ', temp_common_counter
            if temp_common_counter > most_common_counter:
                most_common_val = name
                most_common_counter = temp_common_counter
            temp_common_counter = 0
        print 'Most Common Val in **', val, '** is:', most_common_val
        return most_common_val

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def get_min(self, col):
        """If col is numeric returns the min value"""
        if self.struct.structure[self.struct.lines[0][col]] == 'NUMERIC':
            if self.struct.lines[1][col] != '':
                min_value = float(self.struct.lines[1][col])
            else:
                min_value = 0
            for row in range(1, len(self.struct.lines)):
                if self.struct.lines[row][col] != '':
                    if float(self.struct.lines[row][col]) < min_value:
                        min_value = float(self.struct.lines[row][col])
            return min_value
        else:
            return None

    def get_max(self, col):
        """If col is numeric returns the max value"""
        if self.struct.structure[self.struct.lines[0][col]] == 'NUMERIC':
            if self.struct.lines[1][col] != '':
                max_value = float(self.struct.lines[1][col])
            else:
                max_value = 0
            for row in range(1, len(self.struct.lines)):
                if self.struct.lines[row][col] != '':
                    if float(self.struct.lines[row][col]) > max_value:
                        max_value = float(self.struct.lines[row][col])
            return max_value
        else:
            return None

    def user_interval(self, col, userCols):
        """ Calculates the interval needed for scaling defined by number of bins user entered """
        interval = (self.get_max(col) - self.get_min(col)) / userCols
        interval = int(math.ceil(interval))
        return interval

    def build_scale(self, col, userCols):
        """ Build Scale after discretization """
        if self.struct.structure[self.struct.lines[0][col]] == 'NUMERIC':
            scale = [self.get_min(col)]
            index = 0
            interval = self.user_interval(col, userCols)
            for i in range(userCols):
                scale.append(scale[index] + interval)
                index += 1
            return scale

    def yesno_counter_to_numeric(self, attr, sign, userCols):
        """ Using the scale to count how many object in each bin """
        current_scale = self.build_scale(self.struct.attributes.index(attr), userCols)
        scale_counter = []
        for i in range(len(current_scale) - 1):
            # scale_counter.append(0)
            scale_counter.append(1)  # Laplacian Correction
        for row in range(1, len(self.struct.lines)):
            for runner in range(len(current_scale) - 1):
                if current_scale[runner] <= float(self.struct.lines[row][self.struct.attributes.index(attr)]) < \
                        current_scale[runner + 1]:
                    if self.struct.lines[row][self.struct.attributes.index('class')] == sign:
                        scale_counter[runner] += 1
        return scale_counter

    def num_of_occurrence(self, col, attribute):
        """ Counts number of occurences of attribute """
        temp_common_counter = 0
        for row in range(1, len(self.struct.lines)):
            if self.struct.lines[row][col] != '':
                if self.struct.lines[row][col] == attribute:
                    temp_common_counter = temp_common_counter + 1
        return int(temp_common_counter)

    def probability_attribute_train_numeric(self, scale, index, sign):
        """ Returns probability for train model """
        return scale[index] / float(self.num_of_occurrence(self.struct.attributes.index('class'), sign))

    def classifier_numeric(self, attr, sign, userCols):
        """ Returns all the probabilities that calculated in list type """
        yes = self.yesno_counter_to_numeric(attr, sign, userCols)
        classifier_engine_probability = []
        for i in range(len(yes)):
            classifier_engine_probability.append(
                self.probability_attribute_train_numeric(yes, i, sign))
            print '{0} / {1}'.format(i, len(yes) - 1)
        print classifier_engine_probability
        return classifier_engine_probability

    def change_to_scale(self, attr, userCols):
        """ Changes the value of each numeric value to the number bin its needed to be for faster calculations """
        current_scale = self.build_scale(self.struct.attributes.index(attr), userCols)
        for row in range(1, len(self.struct.lines)):
            for runner in range(len(current_scale) - 1):  # type: int
                if current_scale[runner] <= float(self.struct.lines[row][self.struct.attributes.index(attr)]) < \
                        current_scale[runner + 1]:
                    self.struct.lines[row][self.struct.attributes.index(attr)] = runner

    def yesno_counter_to_attribute(self, attribute, val_attribute, sign):
        """ Counts occurrences of attribute checks if sign is yes or no """
        # counter = 0
        counter = 1  # Laplacian Correction - adds 1 to each attribute counter
        for row in range(1, len(self.struct.lines)):
            if self.struct.lines[row][self.struct.attributes.index(attribute)] == val_attribute and \
                    self.struct.lines[row][self.struct.attributes.index('class')] == sign:
                counter += 1
        return counter

    def classifier_non_numeric(self, attr, attr_val, sign):
        """ Returns probability for non numeric attributes """
        # len(self.struct.structure[attr]) returns number of variables theat needed to be added for the laplace correction
        return self.yesno_counter_to_attribute(attr, attr_val, sign) / float(
            self.num_of_occurrence(self.struct.attributes.index('class'), sign) + len(self.struct.structure[attr]))

    def build_model(self, userCols):
        """ Main function for building the Model, creates "dataBase" of probabilitys """
        # self.pre_processing()
        self.pre_processing(self.struct.lines)
        for i in range(len(self.struct.attributes) - 1):
            if self.struct.structure[self.struct.lines[0][i]] == 'NUMERIC':
                print("Numeric !!")
                self.probability_attribute_to_yes[self.struct.lines[0][i]] = (
                    self.classifier_numeric(self.struct.lines[0][i], 'yes', userCols))
                self.probability_attribute_to_no[self.struct.lines[0][i]] = (
                    self.classifier_numeric(self.struct.lines[0][i], 'no', userCols))
                self.change_to_scale(self.struct.lines[0][i], userCols)
            else:
                self.probability_attribute_to_yes[self.struct.lines[0][i]] = []
                self.probability_attribute_to_no[self.struct.lines[0][i]] = []
                for attr in self.struct.structure[self.struct.lines[0][i]]:
                    print attr
                    self.probability_attribute_to_yes[self.struct.lines[0][i]].append(
                        (attr, self.classifier_non_numeric(self.struct.lines[0][i], attr, 'yes')))
                    self.probability_attribute_to_no[self.struct.lines[0][i]].append(
                        (attr, self.classifier_non_numeric(self.struct.lines[0][i], attr, 'no')))

    def return_probability(self, attr, val, yes_no, userCols):
        """ Returns probability from the model depends of the request """
        yes = self.probability_attribute_to_yes[attr]
        no = self.probability_attribute_to_no[attr]
        if yes_no == 1:
            if self.struct.structure[attr] == 'NUMERIC':
                return yes[val]
            for i in range(len(yes)):
                if yes[i][0] == val:
                    return yes[i][1]
        else:
            if self.struct.structure[attr] == 'NUMERIC':
                return no[val]
            for i in range(len(yes)):
                if yes[i][0] == val:
                    return no[i][1]

    def get_min_test(self, col):
        """If col is numeric returns the min value"""
        if self.struct.structure[self.testData[0][col]] == 'NUMERIC':
            if self.testData[1][col] != '':
                min_value = float(self.testData[1][col])
            else:
                min_value = 0
            for row in range(1, len(self.testData)):
                if self.testData[row][col] != '':
                    if float(self.testData[row][col]) < min_value:
                        min_value = float(self.testData[row][col])
            return min_value
        else:
            return None

    def get_max_test(self, col):
        """If col is numeric returns the max value"""
        if self.struct.structure[self.testData[0][col]] == 'NUMERIC':
            if self.testData[1][col] != '':
                max_value = float(self.testData[1][col])
            else:
                max_value = 0
            for row in range(1, len(self.testData)):
                if self.testData[row][col] != '':
                    if float(self.testData[row][col]) > max_value:
                        max_value = float(self.testData[row][col])
            return max_value
        else:
            return None

    def user_interval_test(self, col, userCols):
        """ Returns interval needed for scaling depends on User Cols, this function using testData """
        interval = (self.get_max_test(col) - self.get_min_test(col)) / userCols
        interval = int(math.ceil(interval))
        return interval

    def build_scale_test(self, col, userCols):
        # Build Scale after discretion
        if self.struct.structure[self.struct.lines[0][col]] == 'NUMERIC':
            scale = [self.get_min_test(col)]
            index = 0
            interval = self.user_interval_test(col, userCols)
            for i in range(userCols):
                scale.append(scale[index] + interval)
                index += 1
            return scale

    def change_to_scale_testData(self, attr, userCols):
        current_scale = self.build_scale_test(self.struct.attributes.index(attr), userCols)
        checkmax = current_scale[len(current_scale) - 1]
        for row in range(1, len(self.testData)):
            for runner in range(len(current_scale) - 1):  # type: int
                if (current_scale[runner] <= float(self.testData[row][self.struct.attributes.index(attr)]) <
                    current_scale[runner + 1]) or float(self.testData[row][self.struct.attributes.index(attr)]) == \
                        current_scale[len(current_scale) - 1]:
                    self.testData[row][self.struct.attributes.index(attr)] = runner

    def change_scale(self, userCols):
        for i in range(len(self.struct.attributes) - 1):
            if self.struct.structure[self.testData[0][i]] == 'NUMERIC':
                self.change_to_scale_testData(self.testData[0][i], userCols)

    def activate_model(self, index, userCols, yes_dict, no_dict):
        print("///////////// Process No: {0} \\\\\\\\\\\\\\\\".format(index))
        yes_prob = 1
        for i in range(len(self.struct.attributes) - 1):
            if self.testData[index][i] in yes_dict:
                yes_prob = float(yes_prob) * yes_dict[self.testData[index][i]]
            else:
                if self.struct.structure[self.testData[0][i]] != 'NUMERIC':
                    prob = self.return_probability(self.testData[0][i], self.testData[index][i], 1, userCols)
                    if prob != 0:
                        yes_dict[self.testData[index][i]] = prob
                    else:
                        yes_dict[self.testData[index][i]] = 1
                    print("Value: {0} | Probability YES: {1} ".format(self.testData[index][i],
                                                                      yes_dict[self.testData[index][i]],
                                                                      self.testData[index][i],
                                                                      1,
                                                                      userCols))
                    yes_prob = float(yes_prob) * yes_dict[self.testData[index][i]]
                else:
                    prob = self.return_probability(self.testData[0][i], self.testData[index][i], 1, userCols)
                    if prob != 0:
                        yes_prob = float(yes_prob) * prob
                    else:
                        yes_prob = float(yes_prob) * 1

                print("{0} : {1}".format(i, yes_prob))  # print calculation
        prob_yes_to_class = float(self.yesno_counter_to_attribute("class", "yes", "yes")) / (len(self.struct.lines) - 1)
        print("Yes _ prob: {0}".format(yes_prob))
        print("Prob: Yes/Class : {0}".format(prob_yes_to_class))
        print("###############################")
        no_prob = 1
        for i in range(len(self.struct.attributes) - 1):
            if self.testData[index][i] in no_dict:
                no_prob = float(no_prob) * no_dict[self.testData[index][i]]
            else:
                if self.struct.structure[self.testData[0][i]] != 'NUMERIC':
                    prob = self.return_probability(self.testData[0][i], self.testData[index][i], -1, userCols)
                    if prob != 0:
                        no_dict[self.testData[index][i]] = prob
                    else:
                        no_dict[self.testData[index][i]] = 1
                    # no_dict[testData[index][i]] = return_probability(testData[0][i], testData[index][i], -1, userCols)
                    print("Value: {0} | Probability NO: {1} ".format(self.testData[index][i],
                                                                     no_dict[self.testData[index][i]]))
                    no_prob = float(no_prob) * no_dict[self.testData[index][i]]
                else:
                    prob = self.return_probability(self.testData[0][i], self.testData[index][i], -1, userCols)
                    if prob != 0:
                        no_prob = float(no_prob) * prob
                    else:
                        no_prob = float(no_prob) * 1
                print("{0} : {1}".format(i, no_prob))  # print calculation

        print("Yes _ prob: {0}".format(no_prob))
        prob_no_to_class = float(self.yesno_counter_to_attribute("class", "no", "no")) / (len(self.struct.lines) - 1)
        yes_prob = yes_prob * prob_yes_to_class
        no_prob = no_prob * prob_no_to_class
        print("Prob: No/Class : {0}".format(prob_no_to_class))
        print("###############################")
        print("YES prob: {0} ".format(yes_prob))
        print("NO prob: {0}".format(no_prob))
        if yes_prob > no_prob:
            print("The lines is : Class YES")
            print("////////////////////////////////////////////////////////")
            return 1
        else:
            print("The lines is : Class NO")
            print("////////////////////////////////////////////////////////")
            return -1

    def set_data(self, rootPath):

        read2 = csv.reader(open(rootPath + '/test.csv'))
        self.testData = list(read2)
        self.pre_processing(self.testData)
