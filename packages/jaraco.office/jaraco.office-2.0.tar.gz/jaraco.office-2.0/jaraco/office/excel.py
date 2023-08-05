import contextlib

from jaraco.path import tempfile_context


def sheet_as_dict(worksheet):
	"""
	Take an xsrd worksheet and convert it to a dict, using the first
	row as a header (to create keys for the subsequent rows).
	"""
	keys = worksheet.row_values(0)
	value_range = range(1, worksheet.nrows)

	def to_dict(values):
		return dict(zip(keys, values))
	return [
		to_dict(worksheet.row_values(n))
		for n in value_range
	]


# constants from http://msdn.microsoft.com/en-us/library/bb241279.aspx
xlXMLSpreadsheet = 46


def open_workbook(filename):
	from win32com.client import Dispatch
	app = Dispatch('Excel.Application')
	return app.Workbooks.Open(filename)


@contextlib.contextmanager
def suppress_alerts(workbook):
	app = workbook.application
	previous_state = app.DisplayAlerts
	app.DisplayAlerts = False
	try:
		yield
	finally:
		app.DisplayAlerts = previous_state


def get_workbook_as_xml(path):
	"""
	Use Office 2003 or Office 2007 to open up a .xls workbook, save
	it as the Office 2003 Excel XML Spreadsheet format in a temporary
	file, read that XML into memory, then delete the temporary file.
	"""
	workbook = open_workbook(path)
	with tempfile_context(suffix='.xml') as filename:
		with suppress_alerts(workbook):
			workbook.SaveAs(Filename=filename, FileFormat=xlXMLSpreadsheet)
			workbook.Close(SaveChanges=0)
		with open(filename, 'rb') as datafile:
			data = datafile.read()
	return data
