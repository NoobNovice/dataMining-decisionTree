import xlrd
import math
import copy
from TreeNode import TreeNode as Node

class DecisionTree:
    __level = 0
    __threshold = 0
    __table = []
    __label_table = []
    __label = []
    __tree = []

    def __init__(self, level, threshold, num_label, file):
        self.__level = level
        self.__threshold = threshold
        data = xlrd.open_workbook(file)
        sheet = data.sheets()

        # read file in to input table
        for col in range(0, sheet[0].ncols - num_label):
            att = []
            for row in range(0, sheet[0].nrows):
                att.append(sheet[0].cell(row, col).value)
            self.__table.append(att)

        # read file in to label table
        for col in range(len(self.__table) - num_label, len(self.__table)):
            att = []
            for row in range(0, sheet[0].nrows):
                att.append(sheet[0].cell(row, col).value)
            self.__label_table.append(att)

        for att in range(0, num_label):
            self.__label.clear()
            t = copy.copy(self.__table)
            t.append(self.__label_table[att])
            self.__label = self.__classifiedAtt__(len(t) - 1, t)
            root = Node(None, None, None)
            self.__generateTree__(0, root, t)
            self.__tree.append(root)
            print("tree is create " + str(att))
        return

    @staticmethod
    def __classifiedAtt__(att, table):
        temp = copy.copy(table[att])
        temp.pop(0)
        send_att = []
        send_att.append(temp[0])
        while True:
            if len(temp) == 0:
                break
            count = 0
            while True:
                if send_att[count] == temp[0]:
                    temp.pop(0)
                    break
                if count == len(send_att) - 1:
                    send_att.append(temp[0])
                    temp.pop(0)
                    break
                count += 1
        return send_att

    @staticmethod
    def __info__(att_arr):
        arr = copy.copy(att_arr)
        result = 0
        sum = 0

        for temp in range(len(arr)):
            arr[temp] += 1
            sum += arr[temp]

        for value in arr:
            result += (-value / sum * math.log(value / sum, 2))
        return result

    def __attCount__(self, col, x, table, word):
        temp = copy.copy(table)
        if word == "nl":
            count = 0
            for row in range(1, len(temp[col])):
                if x == temp[col][row]:
                    count += 1
            return count

        if word == "l":
            count_list = []
            for time in range(len(self.__label)):
                count_list.append(0)

            for row in range(0, len(temp[col])):
                if x == temp[col][row]:
                    for index in range(0, len(self.__label)):
                        if self.__label[index] == temp[len(temp) - 1][row]:
                            count_list[index] += 1
                            break
            return count_list

    def __infoAtt__(self, att, table):
        result = 0
        attlist = self.__classifiedAtt__(att, table)
        for value in attlist:
            prob = self.__attCount__(att, value, table, "nl") / (len(table[0]) - 1)
            info = self.__info__(self.__attCount__(att, value, table, "l"))
            result += prob * info
        return result

    def __gainAtt__(self, col_label, att, table):
        label_arr = []
        for index in self.__label:
            label_arr.append(self.__attCount__(col_label, index, table, "nl"))
        return self.__info__(label_arr) - self.__infoAtt__(att, table)

    @staticmethod
    def __cropTable__(att, value, table):
        send_table = []
        for time in range(len(table)):
            arr = []
            send_table.append(arr)
            send_table[time].append(table[time][0])

        for row in range(len(table[att])):
            if table[att][row] == value:
                for col in range(len(table)):
                    send_table[col].append(table[col][row])
        send_table.pop(att)
        return send_table

    def __generateTree__(self, cur_level, cur_node, table):
        # root case
        if cur_node.parent == None:
            gain_max = self.__threshold
            att_max = -1
            for i in range(0, len(table) - 1):
                gain = self.__gainAtt__(len(table) - 1, i, table)
                if gain_max < gain:
                    gainmax = gain
                    att_max = i
            cur_node.parent = cur_node
            cur_node.att_split = table[att_max][0]
            path_list = self.__classifiedAtt__(att_max, table)
            for path in path_list:
                child_node = Node(cur_node, None, path)
                t = self.__cropTable__(att_max, path, table)
                cur_node.child.append(child_node)
                self.__generateTree__(cur_level + 1, child_node, t)
            return
        # general case
        elif cur_level <= self.__level and len(table) > 1:
            gain_max = self.__threshold
            att_max = -1
            for att in range(0, len(table) - 1):
                gain = self.__gainAtt__(len(table) - 1, att, table)  # chain error
                if gain_max < gain:
                    gain_max = gain
                    att_max = att
            cur_node.att_split = table[att_max][0]
            if gain_max == self.__threshold:  # label case
                max_count = 0
                label = None
                for value in self.__label:
                    temp = self.__attCount__(len(table) - 1, value, table, "nl")
                    if max_count < temp:
                        max_count = temp
                        label = value
                cur_node.label = label
                return
            else:
                path_list = self.__classifiedAtt__(att_max, table)
                for path in path_list:
                    child_node = Node(cur_node, None, path)
                    t = self.__cropTable__(att_max, path, table)
                    cur_node.child.append(child_node)
                    self.__generateTree__(cur_level + 1, child_node, t)
                return
        # break case
        else:
            max_count = 0
            label = None
            for value in self.__label:
                temp = self.__attCount__(len(table) - 1, value, table, "nl")
                if max_count < temp:
                    max_count = temp
                    label = value
            cur_node.label = label
            return

    def get_forest(self):
        return self.__tree



tree = DecisionTree(5, 0, 19, "data_set.xls")
print("end")
