import pandas as pd
import csv
import os
import pytz
import datetime
import random


from datetime import date
import time


from itertools import groupby


usual_new_headers = ["sales_order_date","sales_order_number","delivery_order_number","retailer_brand_code","service_level","origin_address","origin_city","origin_state","origin_postal_code","ship_to_street1","ship_to_city","ship_to_state","ship_to_postal_code"]
#Sales order date * |Sales order number * |Delivery order number * |Shipping origin street address * |Shipping origin city * |Shipping origin state * |Shipping origin ZIP * |Ship to street address 1 * |Ship to city * |Ship to state * |Ship to ZIP * 

def xl_to_csv(xl_file,outfile):
	# coverts xl to csv, doesn't always work.
	# returns path to file created
	filename = xl_file.split(".")[0]
	read_file = pd.read_excel(xl_file)
	read_file.to_csv(outfile,index = None,header=True)
	return os.path.join(os.getcwd(),outfile)


def make_2d_list(file,col_sep = ","):
	# reads in csv file and creates a 2d list
	# returns 2d list
	data = open(file,"r").read()
	lines = data.split("\n")
	for i in range(len(lines)):
		lines[i] = lines[i].split(col_sep)
	return lines


def remove_bad_rows(data):
	# removes rows with incorrect number of values from 2d list
	# returns fixed data as 2d list
	new_data = []
	headers = data[0]
	for row in data[1:]:
		if len(row) == len(headers) or row:
			new_data.append(row)

	return [headers] + new_data


def read_file(csv_file,col_sep = ","):
	# reads csv file in to list of dicts
	# returns list of dicts
	data = remove_bad_rows(make_2d_list(csv_file,col_sep))
	headers = data[0]
	data = data[1:]
	ld = []
	for row in data:
		try:
			dr = {}
			for i in range(len(row)):
				dr[headers[i]] = row[i]
			if len(dr.keys()) == len(headers):
				ld.append(dr)
		except:
			print(row)
	remove_extra_spaces(ld)
	return ld



def read_files(csv_files,col_sep = ","):
	# reads csv files in to list of dicts
	# assumes all files have same headers
	# returns list of dicts
	all_data = []
	headers = None
	for csv_file in csv_files:
		data = remove_bad_rows(make_2d_list(csv_file,col_sep))
		if headers is None:
			headers = [data[0]]
		data = data[1:]
		all_data += data
	all_data = headers + all_data
	data = all_data
	headers = data[0]
	data = data[1:]
	ld = []
	for row in data:
		try:
			dr = {}
			for i in range(len(row)):
				dr[headers[i]] = row[i]
			ld.append(dr)
		except:
			print(row)
	remove_extra_spaces(ld)
	return ld

	
	


def remove_missing_required(data,required = ["sales_order_number","delivery_order_number"]):
	# removes rows from data that are missing the given required fields
	# no return value, edits mutable dict
	remove_these = []
	for i in range(len(data)):
		for item in required:
			if data[i][item] == "":
				remove_these.append(i)
				break
	for i in remove_these:
		del data[i]



def to_2d_list(dicts):
	# conversts list of dicts to 2d list
	# returns 2d list
	headers = list(dicts[0].keys())
	l = []
	l.append(headers)
	for row in dicts:
		r = []
		for k in headers:
			r.append(row[k])
		l.append(r)
	return l


def to_list_of_dicts(lst):
	# reads csv file in to list of dicts
	# returns list of dicts
	data = remove_extra_spaces(remove_bad_rows(lst))
	headers = data[0]
	data = data[1:]
	ld = []
	for row in data:
		try:
			dr = {}
			for i in range(len(row)):
				dr[headers[i]] = row[i]
			ld.append(dr)
		except:
			print(row)
	return ld






def rename_all(data,new_headers):
	# renames all the column names for the list of dicts
	# no return value, edits mutable dict
	keys = list(data[0].keys())

	for row in data:
		for i in range(len(keys)):
			if new_headers[i] not in row.keys():
				row[new_headers[i]] = row[keys[i]]
				del row[keys[i]]
			else:
				row[new_headers[i]] = row[keys[i]]




def de_spacify(string):
	# removes extra spaces from string
	# returns corrected string
	new_string = ""
	last_char = ""
	i = 0
	length = len(string)
	if length < 2:
		return string
	for c in string:
		if c == " ":
			if last_char != " ":
				new_string += c
		else:
			new_string += c
		last_char = c
		i += 1
	if new_string[-1] == " ":
		new_string = new_string[:-1]
	return new_string


def remove_extra_spaces(data):
	# removes all extra spaces from list of dicts
	# no return value, edits mutable dicts
	for row in data:
		for key in row.keys():
			row[key] = de_spacify(row[key])


def full_zip(z):
	# adds leading zeros to zip
	# returns zip with leading zeros added if needed
	nz = str(z)
	if len(z) < 5:
		while True:
			nz = "0" + nz
			if len(nz) == 5:
				break
		return nz
	else:
		return str(z)


def numbers_only(z):
	# conerts a string to only numbers
	# returns converted string
	new_z = ""
	for c in z:
		if c.isnumeric():
			new_z+=c
	return new_z


def correct_zip(z):
	# converts zips to 5 digit with leading zeros included
	# returns converted zip
	z2 = numbers_only(z)
	if len(z2) > 5:
		new_z = full_zip(str(z2)[:5])
		return new_z
	else:
		return full_zip(str(z2))


def add_col(data,header,default_val):
	# adds a new column to data with given header and assigns it a default_val
	# no return value, edits mutable dict
	# if col already exists, it is simply replaced with new value
	for row in data:
		row[header] = default_val


def replace_col(data,header,default_val):
	# replaces value of all data in given column with given header
	# no return value, edits mutable dict
	add_col(data,header,default_val)


def map_col(data,header,funct):
	# maps a function to all values in column with a given header
	# no return value, edits mutable dict
	for row in data:
		row[header] = funct(row[header])


def rename_col(data,old_header,new_header):
	# renames given old_header with new_header
	# no return value, edits mutable dict
	for row in data:
		row[new_header] = row[old_header]
		del row[old_header]

	

def remove_col(data,header):
	# removes a column with given header and all data associated with it
	# no return value, edits mutable dict
	for row in data:
		del row[header]


def write_to_csv(data,filename,col_sep = ","):
	# writes list of dicts to csv file with filename
	# returns path to file created
	file = open(filename, mode='w', encoding='utf-8')
	csv_format = ""
	lines = []
	for row in data:
		line = []
		for key in row.keys():
			line.append(str(row[key]))
		lines.append(col_sep.join(line))
	headers = list(data[0].keys())
	lines = [col_sep.join(headers)]+lines
	csv_format = "\n".join(lines)
	file.write(csv_format)
	return os.path.join(os.getcwd(),filename)





def all_match(dict1,dict2,keys):
	# given 2 dicts and a list of strings keys, returns true if all keys in both dicts have the same associated values. 
	for k in keys:
		if dict1[k]!=dict2[k]:
			return False
	return True






def write_2d_list_to_csv(listdata,filename,col_sep = ","):
	# writes 2d listdata to a given filename
	# returns path to that filename
	file = open(filename, mode='w', encoding='utf-8')
	csv_format = ""
	lines = []
	for row in listdata:
		line = col_sep.join(row)
		lines.append(line)
	csv_format = "\n".join(lines)
	file.write(csv_format)
	return os.path.join(os.getcwd(),filename)


def combine_csv(lst_of_csv,outfile,col_sep = ","):
	# combines any number of csv files given list like this...[csv1,csv2,csv3]
	# returns path to outfile created
	headers = None
	new_data = []
	for file in lst_of_csv:
		try:
			data = make_2d_list(file,col_sep)
			if headers is None:
				headers = data[0]
				new_data.append(headers)
			for row in data[1:]:
				new_data.append(row)
		except:
			print("missing " + str(file))
	return write_2d_list_to_csv(new_data,outfile,col_sep)




def distinct(data,header):
	# returns list of distinct values in a given column with header	# finds all distinct values for a column given the column header
	# returns list of distinct valuesunique = []
	unique = []
	for row in data:
		if row[header] not in unique:
			unique.append(row[header])
	return unique





def get_tnt_from_service_level(data):
	# inserts the appropriate tnt based on the service_level of that each row.
	# no return value, edits mutable dict
	swap = {
		'GND':'None',
		'1DP':'1',
		'2DA':'2',
		'3DS':'3',
		'1DM':'1',
		'1DA':'1',
		'2DM':'2'
		}
	for row in data:
		try:
			row["tnt"] = swap[row["service_level"]]
		except:
			row["tnt"] = "None"


def current_date(tz = "UTC"):
	tz_in = pytz.timezone(tz)
	return datetime.datetime.now(tz_in).strftime('%Y-%m-%d %H:%M:%S.%f')








def group_by(data,headers,sorter = None):
	# given list of dicts data and keys headers
	# returns list of list of dicts with sub lists grouped by shared header values
	if sorter is None:
		sorter = headers[0]
	sorted_data = sorted(data, key=lambda d: d[sorter]) 
	groups = []
	def f(x):
		give_back = []
		for k in headers:
			give_back.append(x[k])
		return tuple(give_back)
	for key, group in groupby(sorted_data, f):
		groups.append(list(group))
	return groups



def generate_sales_order_numbers(data,retailer_code,sales_order_date,headers):
	# efficiently generates sales order numbers based on delivery orders having shared values associated with the given list of headers being considered as part of the same sales order
	# returns copy of the data with the sales orders generated
	groups = group_by(data,headers)
	flat_data = []
	i = 0
	for g in groups:
		for row in g:
			if row["sales_order_number"] == "":
				row["sales_order_number"] = retailer_code + "-" + sales_order_date + "-" + str(i)
			flat_data.append(row) 
		i += 1
	return flat_data



def generate_delivery_order_numbers(data,retailer_code,sales_order_date):
	i = 0
	for row in data:
		row["delivery_order_number"] = "-".join([retailer_code,sales_order_date,"DO",str(i)])
		i += 1


	

def remove_duplicates(data,headers = ["sales_order_number","delivery_order_number"]):
	# efficiently removes duplicates defined as having the same values associated with all of the given headers
	# returns copy of the data with duplicates removed.
	groups = group_by(data,headers)
	flat_data = []
	for g in groups:
		flat_data.append(g[0])
	return flat_data



def remove_multi_address_sales_orders(data):
	count = 0
	sos = group_by(data,["sales_order_number"]) # list of list of row dicts
	new_data = []
	for so in sos:
		unique_addr = []
		for do in so:
			if do["ship_to_street1"] not in unique_addr:
				unique_addr.append(do["ship_to_street1"])
		if len(unique_addr) == 1:
			for do in so:
				new_data.append(do)
		else:
			count += len(so)
	print(str(count) + " deleted due to multi-ship_to_address")
	return new_data


def remove_multi_service_level_sales_orders(data):
	count = 0
	sos = group_by(data,["sales_order_number"]) # list of list of row dicts
	new_data = []
	for so in sos:
		unique_serv_lev = []
		unique_warehouse = []
		for do in so:
			if do["service_level"] not in unique_serv_lev:
				unique_serv_lev.append(do["service_level"])
			if do["warehouse_code"] not in unique_warehouse:
				unique_warehouse.append(do["warehouse_code"])
		if len(unique_serv_lev) == 1 or len(unique_warehouse) > 1:
			for do in so:
				new_data.append(do)
		else:
			count += len(so)
	print(str(count) + " deleted due to multi-service_level")
	return new_data






def split_in_groups_of(l,groups):
	output=[l[i:i + groups] for i in range(0, len(l), groups)]
	return output



def remove_rows_missing(data,header):
	new_data = []
	for row in data:
		if header in row:
			if row[header] not in ["",None,"None","null","NULL"]:
				new_data.append(row)
	return new_data












def today(tz = 'America/New_York'):
	tz_in = pytz.timezone(tz)
	return datetime.datetime.now(tz_in).strftime('%Y-%m-%d')




class business_day: # assume month/day/year, example: 01/05/2022
	def __init__(self,date_string):
		self.dt = datetime.datetime.strptime(date_string.replace("-",""), "%Y%m%d").date()
		self.possible_days = ("m","t","w","th","f","sa","su")
		self.valid_days = ("m","t","w","th","f")
		self.ups_holidays = ["2022-05-30","2022-07-04","2022-09-05","2022-11-24","2022-12-26","2023-01-02"]
		
	def __str__(self):
		fday = ""
		if self.dt.day < 10:
			fday = "0"+str(self.dt.day)
		else:
			fday = str(self.dt.day)
		fmonth = ""
		if self.dt.month < 10:
			fmonth = "0"+str(self.dt.month)
		else:
			fmonth = str(self.dt.month)
		fyear = str(self.dt.year)

		return "-".join([fyear,fmonth,fday])

	
	def is_weekend(self):
		day = self.possible_days[self.dt.weekday()]
		return day in ("sa","su")
		
	def day(self):
		return self.possible_days[self.dt.weekday()]

	def in_past(self,tz = 'America/New_York'):
		return self.__str__() < today(tz)

	def in_future(self,tz = 'America/New_York'):
		return self.__str__() > today(tz)

	def is_today(self,tz = 'America/New_York'):
		return self.__str__() == today(tz)

	def is_holiday(self):
		return self.__str__() in self.ups_holidays
	
	def is_business_day(self):
		return self.possible_days[self.dt.weekday()] in self.valid_days and self.__str__() not in self.ups_holidays

	def __iadd__(self,other):
		next_day = 0
		while next_day < other:
			time_change = datetime.timedelta(hours=24)
			self.dt = self.dt + time_change
			if self.is_business_day():
				next_day += 1
		return self

	def __add__(self,other):
		if type(other) is int:
			next_day = 0
			copy = eval(self.__repr__())
			while next_day < other:
				time_change = datetime.timedelta(hours=24)
				copy.dt = copy.dt + time_change
				if copy.is_business_day():
					next_day += 1
			return copy
		elif type(other) is business_day or type(other) is str:
			return self.days_until(other)
		else:
			return None



	def __isub__(self,other):
		next_day = 0
		while next_day < other:
			time_change = datetime.timedelta(hours=24)
			self.dt = self.dt - time_change
			if self.is_business_day():
				next_day += 1
		return self


	def __sub__(self,other):
		if type(other) is int:
			next_day = 0
			copy = eval(self.__repr__())
			while next_day < other:
				time_change = datetime.timedelta(hours=24)
				copy.dt = copy.dt - time_change
				if copy.is_business_day():
					next_day += 1
			return copy
		elif type(other) == business_day or type(other) == str:
			return self.days_since(other)
		else:
			return None

	def days_since(self,bus_day):
		if str(bus_day) == str(self):
			return 0
		if type(bus_day) == str:
			bus_day = business_day(bus_day)
		if not bus_day.is_business_day():
			bus_day += 1
		if str(bus_day) > str(self):
			return bus_day.days_since(self) * -1
		count = 0
		thisday = eval(self.__repr__())
		while str(thisday) != str(bus_day):
			thisday -= 1
			count += 1
		return count

	def days_until(self,bus_day):
		if str(bus_day) == str(self):
			return 0
		if type(bus_day) == str:
			bus_day = business_day(bus_day)
		if not bus_day.is_business_day():
			bus_day += 1
		if str(bus_day) < str(self):
			return bus_day.days_until(self) * -1
		count = 0
		thisday = eval(self.__repr__())
		while str(thisday) != str(bus_day):
			thisday += 1
			count += 1
		return count



	def __repr__(self):
		return "business_day(" + self.__str__().__repr__()+")"






def split_sales_orders_into_files(data,group_size,filename,start_date):
	sos = group_by(data,["sales_order_number"])
	groups = split_in_groups_of(sos,group_size)
	i = 1
	d = business_day(start_date)
	d.valid_days = d.possible_days
	for g in groups:
		flat = []
		for so in g:
			for do in so:
				flat.append(do)
		write_to_csv(flat,filename+str(d)+".csv")
		d += 1




def get_subset(data,where):
	subset = []
	for row in data:
		if eval(where):
			subset.append(row)
	return subset







