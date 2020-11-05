from partial_date import PartialDate as pd
import unittest
from datetime import datetime as dt

class TestCreation(unittest.TestCase):
	def test_year(self):
		# check year partial date formats and output
		for y in range(1,2200): 
			self.assertEqual(pd(str(y)).pretty_string(),dt(y,1,1).strftime('%Y'))
			self.assertEqual(pd(str(y)+'y').pretty_string(),dt(y,1,1).strftime('%Y'))
			self.assertEqual(pd(str(y)+'y').pretty_string(),pd(t=dt(y,1,1)).pretty_string())

		#check whether the pretty string format generates the same partial date
		self.assertEqual(pd('1999'),pd(pd('1999').pretty_string()))
		self.assertEqual(pd('1999'),pd(pd('1999y').pretty_string()))
		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('1999'),pd(t = pd('1999y').dt))

	def test_year_month(self):
		# check year-month partial date formats and output
		self.assertEqual(pd('1981-03').pretty_string(),dt(1981,3,1).strftime('%B %Y'))
		self.assertEqual(pd('181-11').pretty_string(),dt(181,11,1).strftime('%B %Y'))
		self.assertEqual(pd('march 1981').pretty_string(),dt(1981,3,1).strftime('%B %Y'))
		self.assertEqual(pd('March 1981').pretty_string(),dt(1981,3,1).strftime('%B %Y'))
		for y in 1,100,1000,1500,1900,1818,1951,1960,2000,2004: 
			for m in range(1,13):
				s = str(y) + '-' + str(m)
				sl = dt(1999,m,1).strftime('%B') + ' ' + str(y)
				self.assertEqual(pd(s).pretty_string(),dt(y,m,1).strftime('%B %Y'))
				self.assertEqual(pd(sl).pretty_string(),dt(y,m,1).strftime('%B %Y'))

		#check whether the pretty string format generates the same partial date
		self.assertEqual(pd('1981-03'),pd(pd('1981-03').pretty_string()))
		self.assertEqual(pd('1981-03'),pd(pd('march 1981').pretty_string()))
		self.assertEqual(pd('1981-03'),pd(pd('March 1981').pretty_string()))
		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('1981-03'),pd(t = pd('March 1981').dt))

	def test_year_month_day(self):
		# check year-month-day partial date formats and output
		self.assertEqual(pd('1981-03-15').pretty_string(),dt(1981,3,15).strftime('%B %d, %Y'))
		self.assertEqual(pd('181-11-1').pretty_string(),dt(181,11,1).strftime('%B %d, %Y'))
		self.assertEqual(pd('march 2, 1981').pretty_string(),dt(1981,3,2).strftime('%B %d, %Y'))
		self.assertEqual(pd('March 2, 1981').pretty_string(),dt(1981,3,2).strftime('%B %d, %Y'))
		for y in 1,100,1000,1500,1900,1818,1951,1960,2000,2004: 
			for m in range(1,13):
				for d in range(1,29):
					s = str(y) + '-' + str(m) + '-' + str(d)
					sl = dt(1999,m,d).strftime('%B') + ' ' + str(d) +', ' + str(y)
					self.assertEqual(pd(s).pretty_string(),dt(y,m,d).strftime('%B %d, %Y'))
					self.assertEqual(pd(sl).pretty_string(),dt(y,m,d).strftime('%B %d, %Y'))

		#check whether the pretty string format generates the same partial date
		self.assertEqual(pd('1981-03-01'),pd(pd('1981-03-01').pretty_string()))
		self.assertEqual(pd('1981-03-01'),pd(pd('march 1, 1981').pretty_string()))
		self.assertEqual(pd('1981-03-01'),pd(pd('March 1, 1981').pretty_string()))
		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('1981-03-01'),pd(t = pd('March 1, 1981').dt))

	def test_decade(self):
		#check decade partial date format and output
		self.assertEqual(pd('190d').pretty_string(),'190th decade')
		self.assertEqual(pd('2d').pretty_string(),'2nd decade')

		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('19d'),pd(t = pd('19d').dt))

	def test_millenium(self):
		#check century partial date format and output
		self.assertEqual(pd('1c').pretty_string(),'1st century')
		self.assertEqual(pd('3c').pretty_string(),'3rd century')

		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('19c'),pd(t = pd('19c').dt))

	def test_millenium(self):
		#check millenium partial date format and output
		self.assertEqual(pd('1m').pretty_string(),'1st millenium')
		self.assertEqual(pd('2m').pretty_string(),'2nd millenium')

		#check whether datetime input generate the same partial date (compared to string input)
		self.assertEqual(pd('2m'),pd(t = pd('2m').dt))

if __name__ == '__main__':
	unittest.main()

