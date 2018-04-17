import xlrd
from DecisionTree import DecisionTree as Dt

forest = Dt(5, 0, 19, "data_set.xls")
tree_arr = forest.get_forest()

data = xlrd.open_workbook("data_set.xls")
sheet = data.sheets()

hit = 0
miss = 0
for row in range(1, sheet[0].nrows):
    print("time " + str(row))
    test_case = []
    for col in range(0, sheet[0].ncols):
        att = []
        att.append(sheet[0].cell(0, col).value)
        att.append(sheet[0].cell(row, col).value)
        test_case.append(att)
    result = forest.prediction(test_case, tree_arr[0])
    print(result)
    print(test_case[12][1])
    if result == test_case[12][1]:
        hit += 1
    else:
        miss += 1
    print("hit " + str(hit))
    print("miss " + str(miss))
    print("\n")
