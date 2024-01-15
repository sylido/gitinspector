# coding: utf-8
#
# Copyright © 2013-2015 Ejwa Software. All rights reserved.
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

import os
import subprocess
from . import extensions, filtering, format, interval, optval

class GitConfig(object):
	def __init__(self, run, repo, global_only=False):
		self.run = run
		self.repo = repo
		self.global_only = global_only

	def _read_git_config(self, variable):
		previous_directory = os.getcwd()
		os.chdir(self.repo)
		setting = subprocess.Popen(filter(None, ["git", "config", "--global" if self.global_only else "",
		                           "inspector." + variable]), stdout=subprocess.PIPE).stdout
		os.chdir(previous_directory)

		try:
			setting = setting.readlines()[0]
			setting = setting.decode("utf-8", "replace").strip()
		except IndexError:
			setting = ""

		return setting

	def _read_git_config_bool(self, variable):
		try:
			variable = self._read_git_config(variable)
			return optval.get_boolean_argument(False if variable == "" else variable)
		except optval.InvalidOptionArgument:
			return False

	def _read_git_config_string(self, variable):
		string = self._read_git_config(variable)
		return (True, string) if len(string) > 0 else (False, None)

	def read(self):
		var = self._read_git_config_string("file-types")
		if var[0]:
			extensions.define(var[1])

		var = self._read_git_config_string("exclude")
		if var[0]:
			filtering.add(var[1])

		var = self._read_git_config_string("format")
		if var[0] and not format.select(var[1]):
			raise format.InvalidFormatError(_("specified output format not supported."))

		self.run.hard = self._read_git_config_bool("hard")
		self.run.list_file_types = self._read_git_config_bool("list-file-types")
		self.run.localize_output = self._read_git_config_bool("localize-output")
		self.run.metrics = self._read_git_config_bool("metrics")
		self.run.responsibilities = self._read_git_config_bool("responsibilities")
		self.run.useweeks = self._read_git_config_bool("weeks")

		var = self._read_git_config_string("since")
		if var[0]:
			interval.set_since(var[1])

		var = self._read_git_config_string("until")
		if var[0]:
			interval.set_until(var[1])

		self.run.timeline = self._read_git_config_bool("timeline")

		if self._read_git_config_bool("grading"):
			self.run.hard = True
			self.run.list_file_types = True
			self.run.metrics = True
			self.run.responsibilities = True
			self.run.timeline = True
			self.run.useweeks = True
