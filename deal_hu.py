
# 对每一户数据进行处理相关函数

# 将A表中的数据按户进行划分
def spliteFamily(TableA):

    # 按照sid区分每一户
    # 先取sid，去掉重复值
    sid_array = TableA["SID"].drop_duplicates()
    i = 0
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = TableA[TableA["SID"] == sid_index]
        # zy_data = TableD[TableD["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='A100')
        yield hu_data