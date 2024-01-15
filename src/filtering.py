# coding: utf-8
#
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

import re
import subprocess

filters = {"file": [set(), set()], "author": [set(), set()], "email": [set(), set()], "revision": [set(), set()],
               "message" : [set(), None]}

class InvalidRegExpError(ValueError):
	def __init__(self, msg):
		super(InvalidRegExpError, self).__init__(msg)
		self.msg = msg

def get():
	return filters

def _add_one(string):
	for i in filters:
		if (i + ":").lower() == string[0:len(i) + 1].lower():
			filters[i][0].add(string[len(i) + 1:])
			return
	filters["file"][0].add(string)

def add(string):
	rules = string.split(",")
	for rule in rules:
		_add_one(rule)

def clear():
	for i in filters:
		filters[i][0] = set()

def get_filered(filter_type="file"):
	return filters[filter_type][1]

def has_filtered():
	for i in filters:
		if filters[i][1]:
			return True
	return False

def _find_commit_message(sha):
	git_show_r = subprocess.Popen(filter(None, ["git", "show", "-s", "--pretty=%B", "-w", sha]),
	                              stdout=subprocess.PIPE).stdout

	commit_message = git_show_r.read()
	git_show_r.close()

	commit_message = commit_message.strip().decode("unicode_escape", "ignore")
	commit_message = commit_message.encode("latin-1", "replace")
	return commit_message.decode("utf-8", "replace")

def set_filtered(string, filter_type="file"):
	string = string.strip()

	if len(string) > 0:
		for i in filters[filter_type][0]:
			search_for = string

			if filter_type == "message":
				search_for = _find_commit_message(string)
			try:
				if re.search(i, search_for) != None:
					if filter_type == "message":
						_add_one("revision:" + string)
					else:
						filters[filter_type][1].add(string)
					return True
			except:
				raise InvalidRegExpError(_("invalid regular expression specified"))
	return False
