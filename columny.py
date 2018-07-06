# Version : 1.3.1
# Code is on git Now !!
import csv
import sys
import argparse
import os.path as _path
import os

class Colonify():
	errorStrings = {"FileNotFoundError":"Error: The file couldn't be found", "InternalError":"Error: An internal error has occured","EmptyError":"The file might be empty"}
	dict_args = None

	def __init__(self):
		parser = argparse.ArgumentParser(description='Columny v1.1')
		parser.add_argument('-p', nargs='?', type=int, help="Padding between columns, default : 5", default=5)
		parser.add_argument('-d', nargs='?', type=str, help="Delimeter between columns, default : ,", default=',')
		parser.add_argument('-f', nargs='?', type=str, help="Input file name", required=True)
		parser.add_argument('-o', nargs='?', type=str, help="Output file name")
		args = parser.parse_args()
		self.dict_args = vars(args)

	def _openWriteStream(self, filePath, default_dir):
		if _path.exists(_path.dirname(filePath)):
			if _path.isdir(filePath):
				return False
			else:
				try:
					return open(filePath,'w')
				except FileNotFoundError:
					print(self.errorStrings["FileNotFoundError"])
					exit(1)
		else:
			return False
			
	def _openWriteStream_(self, filePath):
		try:
			if not _path.isdir(filePath):
				if _path.exists(_path.dirname(filePath)):
					return open(filePath,'w')
				elif len(_path.dirname(filePath)) == 0:
						print("[ File ] : "+os.getcwd()+"\\"+filePath)
						return open(filePath,'w')
				else:
					print("No such directory")
					exit(1)
			else:
				print('Cannot write to a directory')
				print('Please specify a file name')
		except FileNotFoundError:
			print(self.errorStrings["FileNotFoundError"])
			exit(1)			 
		
			
	def toColumn(self):
		try:
			with open(self.dict_args['f'],'r') as f:
				if self.dict_args['d'].startswith("") and self.dict_args['d'].endswith(""):
					self.dict_args['d'] = self.dict_args['d'].replace('"','')
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
				# init output stream
				fout = False
				
				if self.dict_args['o'] not in (None,''):
					fout =  self._openWriteStream_(self.dict_args['o'])
					if not fout:
						dump = "dump_0.txt"
						print("# Creating dump file: "+os.getcwd()+"\\"+dump)
						# To check further
						fout = open(dump,'w')
				else:
					fout = sys.stdout
				for j, row in enumerate(content):
					print((formatStringArray[j]).format(*row),file=fout)	
				
		except FileNotFoundError:
			print(self.errorStrings["FileNotFoundError"])			

def main():
	col = Colonify()
	col.toColumn()
	del col
	
	
if __name__ == "__main__":
    main()
