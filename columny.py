# Version : 1.1
# Code is on git Now !!
import csv
import sys
import argparse

class Colonify():
	errorStrings = {"FileNotFoundError":"Error: The file couldn't be found", "InternalError":"Error: An internal error has occured","EmptyError":"The file might be empty"}
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
		try:
			with open(self.dict_args['f'],'r') as f:
				content = csv.reader(f, delimiter = self.dict_args['d'])
				padding = self.dict_args['p']
				formatStringArray = []
				prevColumnMaxLen = []
				rowLen = []
				try:
					nColumns = len ( next( iter(content) ) )
				except StopIteration:
					print(self.errorStrings["InternalError"]+'. '+self.errorStrings["EmptyError"])
					exit(1)
				#Rewind cursor
				f.seek(0)
				#----------- Seems correct until here
				for i in range(nColumns): 
					p = 0
					for j, row in enumerate(content):
						currentColumn = len(row[i])
						rowLen.append(currentColumn)
						if i == 0:
							p = 0
						else:
							prevColumnLen = len(row[i - 1])
							p = currentColumn + prevColumnMaxLen[i - 1] - prevColumnLen + padding
						if len(formatStringArray) > j:
							formatStringArray[j] = formatStringArray[j]+'{:>'+str(p)+'}'
						else:
							formatStringArray.append('{}')
					f.seek(0)
					prevColumnMaxLen.append(max(rowLen))
					rowLen = []
				f.seek(0)
				for j, row in enumerate(content):
					print((formatStringArray[j]).format(*row))	
		except FileNotFoundError:
			print(self.errorStrings["FileNotFoundError"])			

def main():
	col = Colonify()
	col.toColumn()
	
	
if __name__ == "__main__":
    main()
