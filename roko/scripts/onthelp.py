import pandas as pd
import xlrd

def main():
#ONTOLOGY
	book = xlrd.open_workbook("temp329.xlsx") #replscr with excel file
	# sheet = book.sheet_by_index(0)
	# for cell in sheet.col(0):
 #   		print("\""+cell.value.lower().rstrip()+"\",")


 #DICTIONARY
	sheet = book.sheet_by_index(0)
	i=0
	for cell in sheet.col(0):
		print("\""+cell.value.lower().rstrip()+"\":"+"\""+ str(sheet.cell_value(i,1)).rstrip()+"\",")
		i=i+1


if __name__ == "__main__":
	main()