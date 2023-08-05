"tdtools utility functions"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2017, Paresh Adhia"
__license__ = "GPL"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yappt
from tdtypes.sqlcsr import *

def load_json(resource):
	import json
	from pkg_resources import resource_filename

	with open(resource_filename(__name__, resource), 'r') as jsonf:
		return json.load(jsonf)

def getLogger(name):
	import tdtypes as td

	td.getLogger('tdtools')
	return td.getLogger(name)

def pprint_csr(csr, limit=0, sizefmt='.1h', pctfmt='.1%'):
	"""
	Return cursor resultset in formatted tabular form.abs
	Column header and values are formatted based on their type and name.
	As a convention, column names ending with
	- _ (underscore) are formatted as human-readable sizes
	- % are formatted as percentage
	- Column names are turned into headers, after removing trailing _ if any
	"""
	def col(n, t):
		"""return format string based on name and type of the column"""
		if n.endswith('_'):
			return yappt.PPCol(n[:-1], ctype=t, fmtval=lambda v: format(yappt.HumanInt(v), sizefmt))
		if n.endswith('%'):
			return yappt.PPCol(n, ctype=t, fmtval=lambda v: format(v, pctfmt))
		return yappt.PPCol(n, t)

	if limit:
		def data():
			"generate rows up to limit specified"
			def rows():
				"return row at a time until exhausted"
				r = csr.fetchone()
				while r is not None:
					yield r
					r = csr.fetchone()
			yield from (r for e, r in enumerate(rows()) if e < limit)
	else:
		data = csr.fetchall

	return yappt.pprint(data(), columns=[col(d[0], d[1]) for d in csr.description], sep='  ')

try:
	dbconn_args # test if a custom function is defined
except NameError:
	def dbconn_args(parser):
		"""
		Placeholder function, when overriden allows database connection information to be supplied via command-line.
		database connection information via command line option.
		- tdconn_site.py must include dbconn_args() function that accepts
		argparse.ArgumentParser object and adds required argument(s).
		- And, dbconnect() function that will be passed output of ArgumentParser.parse_args()
		"""
