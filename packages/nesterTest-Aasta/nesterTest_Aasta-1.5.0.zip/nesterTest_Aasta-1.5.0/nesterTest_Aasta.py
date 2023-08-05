"""
python 練習
"""
def print_lol(thislist,indent=false,level =0,fn=sys.stdout):
	for each_item in thislist:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fn)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='',file=fn)
			print(each_item,file=fn)