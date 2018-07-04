# Version : 1.1
# Code is on git Now !!
import csv
import sys
import argparse

class Colonify():
	
	dict_args = None
	def __init__(self):
		parser = argparse.ArgumentParser(description='Colmnify v1.1')
		parser.add_argument('-p', nargs='?', type=int, help="Padding between columns, default : 5", default=5)
		parser.add_argument('-d', nargs='?', type=str, help="Delimeter between columns, default : ,", default=',')
		parser.add_argument('-f', nargs='?', type=str, help="File name", required=True)
		args = parser.parse_args()
		self.dict_args = vars(args)
	
	def parse(self):
		#print(self.dict_args)
		pass
	
	def toColumn(self):
		self.parse()
		with open(self.dict_args['f'],'r') as f:
			content = csv.reader(f, delimiter = self.dict_args['d'])
			header = iter(content)
			nColumns = len(next(header))
			padding = self.dict_args['p']
			formatStringArray = []
			rowLen = [len(ele[0]) for ele in header]
			prevColumnMaxLen = []
			prevColumnMaxLen.append(max(rowLen))
			f.seek(0)
			#-----------
			for i in range(1, nColumns):
				p = 0
				for j, row in enumerate(content):
					currentColumn = len(row[i])
					rowLen.append(currentColumn)
					prevColumnLen = len(row[i - 1])
					p = currentColumn + prevColumnMaxLen[i - 1] - prevColumnLen + padding
					if len(formatStringArray) > j:
						formatStringArray[j] = formatStringArray[j]+'{:>'+str(p)+'}'
					else:
						formatStringArray.append('{:>'+str(p)+'}')
				f.seek(0)
				prevColumnMaxLen.append(max(rowLen))
				rowLen = []

			f.seek(0)

			for j, row in enumerate(content):
				print(('{}'+formatStringArray[j]).format(*row))	
					

def main():
	col = Colonify()
	col.toColumn()
	
	
if __name__ == "__main__":
    main()
