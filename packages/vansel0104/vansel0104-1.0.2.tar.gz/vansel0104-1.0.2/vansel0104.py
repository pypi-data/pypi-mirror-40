"""这只是一个测试模块"""
def print_lol(the_list, level):
	"""
	遍历函数
	如果列表里面有列表，调用自己并打印。
	如果不是列表直接打印
	"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			for tab_stop in range(level):
				print("\t", end="")
			print(each_item)
