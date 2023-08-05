'''this is a new module i wrote.
	please take care of if as much as you can.
	thank you.
'''
def print_lol(the_list):
	'''
	this is a little function to deal with a list with cycle item.
	'''
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)



