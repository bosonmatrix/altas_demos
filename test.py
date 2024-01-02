nearby_cp_filtered=[[-6021950.43043448, 9164392.527008686, -2.996533, 3.0], 
                    [-6018082.025661625, 9162314.222280363, -2.8341, 2.0], 
                    [-6017907.506884681, 9162220.533409834, -3.043029, 3.0], 
                    [-6017559.056738664, 9162033.489482462, -2.633634, 1.0], 
                    [-6006758.923457784, 9156248.29746024, -2.495993, 3.0], 
                    [-6001222.609989503, 9153291.865469638, -1.237973, 3.0]]

# 1. 遍历二维列表中的每个子列表
lines_list = []
for sublist in nearby_cp_filtered:
    # 2. 检查每个子列表是否为空列表
    if sublist:
        # 3. 转换子列表中的数字为字符串并添加到新列表中    
        numbers_line = ' '.join(str(elem) for elem in sublist)
        lines_list.append(numbers_line)
    else:
        # 如果子列表为空，则添加一个空行
        lines_list.append('')

# 4. 将列表中的元素连接为一个字符串，每个元素占据一行
final_string = '\n'.join(lines_list)

# 5. 将最终的字符串写入文件
with open('nearby_cp_filtered_t.txt', 'w+') as file:
    file.write(final_string)