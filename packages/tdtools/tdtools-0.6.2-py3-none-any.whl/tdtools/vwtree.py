#! /usr/bin/env python
"List Teradata view dependecies"

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

import tdtypes as td
from . import util

logger = util.getLogger(__name__)

class Err(Exception):
	"Script error"

class ViewFinder(td.table.DBObjFinder):
	"Find all views that matching name patterns and optionally created between given period"
	def __init__(self, names, since, before):
		super().__init__(names, objtypes='V')
		self.since, self.before = since, before

	def make_sql(self):
		sql = super().make_sql()
		if self.since:
			sql += "\n   AND CreateTimestamp >= CAST('{}' AS TIMESTAMP(0))".format(self.since.isoformat())
		if self.before:
			sql += "\n   AND CreateTimestamp <  CAST('{}' AS TIMESTAMP(0))".format(self.before.isoformat())
		return sql

def main():
	"script entrypoint"
	global csr

	try:
		args = user_args()

		with td.cursor(args) as csr:
			if csr.version < "14.10":
				raise Err('This script only works with Teradata versions 14.10 or later')

			vwlist = ViewFinder(args.names, args.since, args.before).findall(csr=csr)

			if args.store:
				persist(vwlist, args.store, recurse=not (args.since or args.before))
			else:
				display(vwlist)

	except Err as msg:
		logger.error(msg)

	return 8

def user_args():
	"run-time parameters"

	import argparse
	import textwrap
	from datetime import datetime

	def parse_date(d):
		"Parse text to a Date object"
		return datetime.strptime(d, '%Y-%m-%d')

	p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__, epilog=textwrap.dedent("""\
	Note: --store argument requires the table to have all columns shown in the example below.
	   CREATE TABLE ViewRefs
	   ( ViewDB    varchar(128) character set unicode not null
	   , ViewName  varchar(128) character set unicode not null
	   , RefDB     varchar(128) character set unicode not null
	   , RefName   varchar(128) character set unicode not null
	   ) PRIMARY INDEX(ViewDB,ViewName);"""))

	# pylint: disable=locally-disabled, bad-whitespace
	p.add_argument("names", metavar='VIEW', type=td.DBObjPat, nargs='+', help="View name or pattern (eg dbc.qry%% dbc.tablesv)")
	p.add_argument(      '--since',    metavar='YYYY-MM-DD', type=parse_date, help="only views created since the given date")
	p.add_argument(      '--before',   metavar='YYYY-MM-DD', type=parse_date, help="only views created before the given date")
	p.add_argument('-u', '--store',    metavar='TBL',        help="Insert/Update references info in a table")

	util.dbconn_args(p)

	return p.parse_args()

def execsql(sql, parms=None):
	"log and execute SQL"
	logger.debug('Submitting SQL:\n%s;\n', sql)
	return csr.executemany(sql, parms) if parms and isinstance(parms, list) else csr.execute(sql, parms)

def display(vwlist):
	"display view and dependencies as a tree"
	from yappt import treeiter

	for vw in vwlist:
		for pfx, node in treeiter(vw, getch=lambda v: v.refs if isinstance(v, td.View) else []):
			print(str(pfx) + str(node))

def persist(vwlist, table, recurse=True):
	"save view list to given table"
	from util.sqlcsr import Error

	def view_iterator(vw):
		"generate view dependecies, each as a tuple"
		try:
			for ob in vw.refs:
				yield vw.sch, vw.name, ob.sch, ob.name
				if recurse and isinstance(ob, td.View):
					yield from view_iterator(ob)
		except td.NotFoundError:
			logger.error('Error getting %s references -- view probably refers to a non-existent object.', vw)

	refs = [ref for vw in vwlist for ref in view_iterator(vw)]

	if refs:
		dedup = lambda l: list(set(l))   # remove duplicates from a list
		try:
			execsql("DELETE FROM {} WHERE ViewDB = ? AND ViewName = ?".format(table), dedup([(vdb, vw) for vdb, vw, rdb, ref in refs]))
			execsql("INSERT INTO {}(ViewDB,ViewName,RefDB,RefName) VALUES(?,?,?,?)".format(table), dedup(refs))
		except util.Error as msg:
			raise Err("Error updating [{}]: {}".format(table, msg))

	else:
		logger.info("No view references to update")

if __name__ == '__main__':
	import sys
	sys.exit(main() or 0)
