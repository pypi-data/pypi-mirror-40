"""
python 練習
"""
def print_lol(this_list,level):
	for each_item in this_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)