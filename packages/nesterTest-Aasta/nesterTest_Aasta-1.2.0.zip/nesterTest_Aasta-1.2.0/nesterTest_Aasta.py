"""
python 練習
"""
def print_lol(thislist,level):
	for each_item in thislist:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item)