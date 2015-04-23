#e.py
# from __future__ import print_function
from time import localtime, strftime
import json

# print 
foo = {'a':23,'b':23}

log =  open("test.log",'a+')



try:
	foo['c']
except KeyError as e:
	report = strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
	report += 'KeyError: ['
	report += str(e)
	report += ']\n'
	log.write(report)

json.dump(foo,log)

log.close
