# coding: utf-8
#
# Copyright © 2012 Ejwa Software. All rights reserved.
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

from __future__ import print_function
import format

class Outputable(object):
	def output_html(self):
		print("HTML output not yet supported in \"" + self.__class__.__name__ + "\".")

	def output_text(self):
		print("Text output not yet supported in \"" + self.__class__.__name__ + "\".")

	def output_xml(self):
		print("XML output not yet supported in \"" + self.__class__.__name__ + "\".")

def output(outputable):
	if format.get_selected() == "html":
		outputable.output_html()
	elif format.get_selected() == "text":
		outputable.output_text()
	else:
		outputable.output_xml()