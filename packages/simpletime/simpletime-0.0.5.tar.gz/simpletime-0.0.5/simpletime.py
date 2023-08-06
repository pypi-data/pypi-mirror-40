#!/usr/bin/env python
# coding: utf-8
# 
# file    : simpletime.py
# version : 0.0.1
# date    : 2019-01-12
# author  : area0
# 
# descript: 
# { "datetime"  : "datetime.datetime",
#   "date"      : "datetime.date"，
#   "time"      : "datetime.time"，
#   "timestamp" : "float",
#   "timetuple" : "time.struct_time",
#   "string"    : "string"
# } 
#
# datetime.datetime(2019, 1, 12, 20, 02, 52, 903347)
# datetime.date(2019, 1, 12)
# datetime.time(20, 02, 52, 903347)
# 1547294572.0
# time.struct_time(tm_year=2019, tm_mon=1, tm_mday=12, tm_hour=20, tm_min=2, tm_sec=52, tm_wday=5, tm_yday=12, tm_isdst=-1)
# 2019-1-12 20:02:52
#
# if date argument is lost, use the current date instead
# if time argument is lost, use 00:00:00 instead
# if date and time are lost, use now instead
#
# issue: 对timestamp和string没有做验证
#        string的验证(date or time), 正则匹配没有字母
#
import time
import datetime

strFormat  = "%Y-%m-%d %H:%M:%S"
dateFormat = "%Y-%m-%d"
timeFormat = "%H:%M:%S"

# if argument is none, return current datetime
def toDatetime(data=[]):
	if isinstance(data, datetime.datetime):
		return data
	# if argument is a date object, return the beginning time of the date
	elif isinstance(data, datetime.date):
		# date -> datetime
		res = datetime.datetime.combine(data, datetime.time())
		return res
	# if argument is a time object, return now date and argument time
	elif isinstance(data, datetime.time):
		# time -> date -> datetime
		tmpDate = datetime.datetime.now().date()
		res = datetime.datetime.combine(tmpDate,data)
		return res
	elif isinstance(data, float) or isinstance(data, int):
		# timestamp -> datetime
		res = datetime.datetime.fromtimestamp(data)
		return res
	elif isinstance(data, time.struct_time):
		# timetuple -> timestamp -> datetime
		tmpStamp = time.mktime(data)
		res = datetime.datetime.fromtimestamp(tmpStamp)
		return res
	elif isinstance(data, str):
		# str -> datetime
		res = datetime.datetime.strptime(data, strFormat)
		return res
	else:
		res = datetime.datetime.now()
		return res

# if argument is none, return current date
def toDate(data=[]):
	if isinstance(data, datetime.date):
		return data
	elif isinstance(data, datetime.datetime):
		# datetime -> date
		res = data.date()
		return res
	# if argument is a  time object, return current date
	elif isinstance(data, datetime.time):
		# datetime -> date
		tmpDatetime = datetime.datetime.now()
		res = tmpDatetime.date()
		return res
	elif isinstance(data, float) or isinstance(data, int):
		# timestamp -> datetime -> date
		tmpDatetime = datetime.datetime.fromtimestamp(data)
		res = tmpDatetime.date()
		return res
	elif isinstance(data, time.struct_time):
		# timetuple -> timestamp -> datetime -> date
		tmpStamp = time.mktime(data)
		tmpDatetime = datetime.datetime.fromtimestamp(tmpStamp)
		res = tmpDatetime.date()
		return res
	elif isinstance(data, str):
		# str -> datetime -> date
		tmpDatetime = datetime.datetime.strptime(data, strFormat)
		res = tmpDatetime.date()
		return res
	else:
		res = datetime.datetime.now().date()
		return res

# if argument is none, return current time
def toTime(data=[]):
	if isinstance(data, datetime.time):
		return data
	elif isinstance(data, datetime.datetime):
		# datetime -> time
		res = data.time()
		return res
	# if argument is a date object, return current time
	elif isinstance(data, datetime.date):
		# datetime -> time
		res = datetime.datetime.now().time()
		return res
	elif isinstance(data, float) or isinstance(data, int):
		# timestamp -> datetime -> time
		res = datetime.datetime.fromtimestamp(data).time()
		return res
	elif isinstance(data, time.struct_time):
		# timetuple -> timestamp -> datetime -> time
		tmpStamp = time.mktime(data)
		res = datetime.datetime.fromtimestamp(tmpStamp).time()
		return res
	elif isinstance(data, str):
		# str -> datetime -> time
		res = datetime.datetime.strptime(data, strFormat).time()
		return res
	else:
		res = datetime.datetime.now().time()
		return res 

# if argument is none, return current timestamp as int
def toStamp(data=[]):
	if isinstance(data, float) or isinstance(data, int):
		res = int(data)
		return res
	elif isinstance(data, datetime.datetime):
		# datetime -> timetuple -> timestamp
		tmpTuple = data.timetuple()
		res = int(time.mktime(tmpTuple))
		return res
	# if argument is a date object, return the beginning time of the date
	elif isinstance(data, datetime.date):
		# date -> timetuple -> timestamp
		tmpTuple = data.timetuple()
		res = int(time.mktime(tmpTuple))
		return res
	# if argument is a time object,
	elif isinstance(data, datetime.time):
		# time -> datetime -> timetuple -> timestamp
		# 'datetime.time' object has no attribute 'timetuple'
		tmpDate = datetime.datetime.now().date()
		tmpDatetime = datetime.datetime.combine(tmpDate,data)
		tmpTuple = tmpDatetime.timetuple()
		res = int(time.mktime(tmpTuple))
		return res
	elif isinstance(data, time.struct_time):
		# timetuple -> timestamp
		res = int(time.mktime(data))
		return res
	elif isinstance(data, str):
		# str -> datetime -> timetuple -> timestamp
		# if string lost date or time!!!
		tmpDatetime = datetime.datetime.strptime(data, strFormat)
		tmpTuple = tmpDatetime.timetuple()
		res = int(time.mktime(tmpTuple))
		return res
	else:
		res = int(time.time())
		return res

# if argument is none, return current timestuple
def toTuple(data=[]):
	if isinstance(data, time.struct_time):
		return data
	elif isinstance(data, datetime.datetime):
		# datetime -> timetuple
		res = data.timetuple()
		return res
	# if argument is a date object, return the beginning time of the date
	elif isinstance(data, datetime.date):
		# date -> timetuple
		res = data.timetuple()
		return res
	# if argument is a time object,
	elif isinstance(data, datetime.time):
		# time -> datetime -> timetuple
		# 'datetime.time' object has no attribute 'timetuple'
		tmpDate = datetime.datetime.now().date()
		tmpDatetime = datetime.datetime.combine(tmpDate,data)
		res = tmpDatetime.timetuple()
		return res
	elif isinstance(data, float) or isinstance(data, int):
		# timestamp -> datetime -> timetuple
		tmpDatetime = datetime.datetime.fromtimestamp(data)
		res = tmpDatetime.timetuple()
		return res
	elif isinstance(data, str):
		# str -> datetime -> timetuple
		tmpDatetime = datetime.datetime.strptime(data, strFormat)
		res = tmpDatetime.timetuple()
		return res
	else:
		res = datetime.datetime.now().timetuple()
		return res
	
# if argument is none, return current string
def toString(data=[]):
	if isinstance(data, str):
		return data
	elif isinstance(data, datetime.datetime):
		# datetime -> str
		res = data.strftime(strFormat)
		return res
	# if argument is a date object, return the beginning time of the date
	elif isinstance(data, datetime.date):
		# date -> str
		res = data.strftime(dateFormat)
		return res
	# if argument is a time object,return only the string of time 
	elif isinstance(data, datetime.time):
		# time -> str
		# 'datetime.time' object has no attribute 'timetuple'
		res = data.strftime(timeFormat)
		return res
	elif isinstance(data, float) or isinstance(data, int):
		# timestamp -> datetime -> str
		tmpDatetime = datetime.datetime.fromtimestamp(data)
		res = tmpDatetime.strftime(strFormat)
		return res
	elif isinstance(data, time.struct_time):
		# timetuple -> timestamp -> datetime -> str
		tmpStamp = time.mktime(data)
		tmpDatetime = datetime.datetime.fromtimestamp(tmpStamp)
		res = tmpDatetime.strftime(strFormat)
		return res
	else:
		res = datetime.datetime.now().strftime(strFormat)
		return res


if __name__ == "__main__":
	print("this is a module for date and time conver")
