
import xlrd
import xlwt
from xlutils.copy import copy
import os.path
import re
import json
import requests
loc = ("4-9.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0) 

writing_wb = copy(wb)
writing_sheet = writing_wb.get_sheet(0)
#print(sheet.cell_value(0,4))

writing_sheet.write(0,23, "home zip code")
writing_sheet.write(0,24, "work zip code")
writing_sheet.write(0,25, "distance")

for i in range(1, sheet.nrows):
    #home address
    home_address = str(sheet.cell_value(i,3))
    search_zip = re.search('\d{5}', home_address)
    if search_zip is not None:
        zip_code1 = search_zip.group(0)
    else:
        zip_code1 = "NONE"
    writing_sheet.write(i, 23, zip_code1)

    work_address = str(sheet.cell_value(i,4))
    #work address
    search_zip = re.search('\d{5}', work_address)
    if search_zip is not None:
        zip_code2 = search_zip.group(0)
    else:
        zip_code2 = "NONE"
    writing_sheet.write(i, 24, zip_code2)
    
    #distance
    if (zip_code1!="NONE") and (zip_code2!="NONE"):
        print(i)
        api_key = "gXTMe761UEknkYBpIgAKOX00rBZVwMLWF4YtS1sCoLjOlv85TmL1YBLKzSRqtuYj"
        n = [api_key, "csv", zip_code1, zip_code2, "mile"]
        api = "http://www.zipcodeapi.com/rest/{}/distance.{}/{}/{}/{}".format(*n)
        response = requests.get(api)
        distance = response.text.split("\n")[1]
        writing_sheet.write(i, 25, distance)
    
writing_wb.save('my_workbook.xls')   

