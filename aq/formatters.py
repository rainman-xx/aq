from tabulate import tabulate
import io
import json
import csv

class TableFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		return tabulate(rows, headers=columns, tablefmt='psql', missingval='NULL')


class JsonFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		rowsData = []
		l = len(columns)

		for row in rows:
			r = {}

			for i in range(0, l):
				r[columns[i]] = row[i]

			rowsData.append(r)


		return json.dumps(rowsData)


class CsvFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		l = len(columns)

		# Note:
		rowsData = io.BytesIO()
		writer = csv.DictWriter(rowsData, fieldnames=columns)
		writer.writeheader()

		for row in rows:
			r = {}

			for i in range(0, l):
				r[columns[i]] = row[i]

			writer.writerow(r)

		# Force string.
		#   Python2.7 getvalue() returns string
		#   Python 3.x returns bytes
		return str(rowsData.getvalue())
