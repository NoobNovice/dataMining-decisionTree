import xlrd
import math
import copy
from TreeNode import TreeNode as Node

class DecisionTree:
    __level = 0
    __threshold = 0
    __num_label = 0
    __table = []
    __label = []
    __tree = []

    def __init__(self):
        dataSet = xlrd.open_workbook("data_set.xls")
        sheet = dataSet.sheets()

        # read file in to table
        for i in range(0, sheet[0].ncols):
            att = []
            for j in range(0, sheet[0].nrows):
                att.append(sheet[0].cell(j, i).value)
            self.__table.append(att)

        self.__label = self.classifiedAtt(sheet[0].ncols - 1, self.__table)
        self.__root = Node(None, None, None)
        return

    def classifiedAtt(self, att, table):
        temp = copy.copy(table[att])
        temp.pop(0)
        sendAtt = []
        sendAtt.append(temp[0])
        while True:
            if len(temp) == 0:
                break
            count = 0
            while True:
                if sendAtt[count] == temp[0]:
                    temp.pop(0)
                    break
                if count == len(sendAtt) - 1:
                    sendAtt.append(temp[0])
                    temp.pop(0)
                    break
                count += 1
        return sendAtt

    def info(self, attArr):
        arr = copy.copy(attArr)
        result = 0
        sum = 0

        for temp in range(len(arr)):
            arr[temp] += 1
            sum += arr[temp]

        for value in arr:
            result += (-value / sum * math.log(value / sum, 2))
        return result

    def attCount(self, att, x, table, word):
        temp = copy.copy(table)
        if word == "nl":
            count = 0
            for i in range(1, len(temp[att])):
                if x == temp[att][i]:
                    count += 1
            return count

        if word == "l":
            countList = []
            for i in range(len(self.__label)):
                countList.append(0)

            for i in range(0, len(temp[att])):
                if x == temp[att][i]:
                    for j in range(0, len(self.__label)):
                        if self.__label[j] == temp[len(temp) - 1][i]:
                            countList[j] += 1
                            break
            return countList

    def infoAtt(self, att, table):
        result = 0
        attlist = self.classifiedAtt(att, table)
        for value in attlist:
            result += (self.attCount(att, value, table, "nl") / (len(table[0]) - 1)) * self.info(
                self.attCount(att, value, table, "l"))
        return result

    def gainAtt(self, attlabel, att, table):
        labelarr = []
        for i in self.__label:
            labelarr.append(tree.attCount(attlabel, i, table, "nl"))
        return self.info(labelarr) - self.infoAtt(att, table)

    def croptable(self, col, row, table):
        sendtable = []
        for time in range(len(table)):
            arr = []
            sendtable.append(arr)
            sendtable[time].append(table[time][0])

        for j in range(len(table[col])):
            if table[col][j] == row:
                for i in range(len(table)):
                    sendtable[i].append(table[i][j])
        sendtable.pop(col)
        return sendtable

    def generateTree(self, curlevel, node, table):
        # root case
        if node.parent == None:
            gainmax = self.__threshold
            attmax = -1
            for i in range(0, len(table) - 1):
                gain = self.gainAtt(len(table) - 1, i, table)
                if gainmax < gain:
                    gainmax = gain
                    attmax = i
            node.parent = node
            node.att_split = table[attmax][0]
            pathlist = self.classifiedAtt(attmax, table)
            for i in pathlist:
                cnode = Node(node, None, i)
                t = self.croptable(attmax, i, table)
                node.child.append(cnode)
                self.generateTree(curlevel + 1, cnode, t)
            return
        # general case
        elif curlevel <= self.__level and len(table) > 1:
            gainmax = self.__threshold
            attmax = -1
            for i in range(0, len(table) - 1):
                gain = self.gainAtt(len(table) - 1, i, table)  # chain error
                if gainmax < gain:
                    gainmax = gain
                    attmax = i
            node.att_split = table[attmax][0]
            if gainmax == self.__threshold or table[attmax][0] == "Iris class":  # label case
                max = 0
                label = None
                for i in self.__label:
                    temp = self.attCount(len(table) - 1, i, table, "nl")
                    if max < temp:
                        max = temp
                        label = i
                node.label = label
                return
            else:
                pathlist = self.classifiedAtt(attmax, table)
                for i in pathlist:
                    cnode = treeNode(node, None, i)
                    t = self.croptable(attmax, i, table)
                    node.child.append(cnode)
                    self.generateTree(curlevel + 1, cnode, t)
                return
        # break case
        else:
            max = 0
            label = None
            for i in self.__label:
                temp = self.attCount(len(table) - 1, i, table, "nl")
                if max <= temp:
                    max = temp
                    label = i
            node.label = label
            return

    def getroot(self):
        return self.__root

    def gettable(self):
        return self.__table


tree = DecisionTree()
tree.generateTree(0, tree.getroot(), tree.gettable())
node = tree.getroot()
print(node.parent)
print(node)
print(node.att_split)
print(node.attr_split_value)
print(node.child)
print("\n")
for i in tree.getroot().child:
    print(i)
    print(i.parent)
    print(i.attr_split_value)
    print(i.att_split)
    print(i.label)
    print("\n")
