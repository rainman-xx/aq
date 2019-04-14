from tabulate import tabulate
import io
import json
import csv
import yaml

class TableFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		return tabulate(rows, headers=columns, tablefmt='psql', missingval='NULL')


# Returns an array of hashes with the columns as the keys
def mixinColumns(columns, rows):
	rowsArr = []
	cLen = len(columns)

	for row in rows:
		r = {}

		for i in range(0, cLen):
			r[columns[i]] = row[i]

		rowsArr.append(r)

	return rowsArr

class JsonFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		rowsArr = mixinColumns(columns, rows)
		return json.dumps(rowsArr)


class YamlFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		rowsArr = mixinColumns(columns, rows)
		return yaml.safe_dump(rowsArr, default_flow_style=False)


class CsvFormatter(object):
	def __init__(self, options=None):
		self.options = options if options else {}

	@staticmethod
	def format(columns, rows):
		rowsData = io.BytesIO()
		writer = csv.DictWriter(rowsData, fieldnames=columns)
		writer.writeheader()

		rowsArr = mixinColumns(columns, rows)
		for row in rowsArr:
			writer.writerow(row)

		# Force string.
		#   Python2.7 getvalue() returns string
		#   Python 3.x returns bytes
		return str(rowsData.getvalue())
