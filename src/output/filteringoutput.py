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

import textwrap
from ..localization import N_
from ..filtering import filters, has_filtered
from .. import terminal
from .outputable import Outputable

FILTERING_INFO_TEXT = N_("The following files were excluded from the statistics due to the specified exclusion patterns")
FILTERING_AUTHOR_INFO_TEXT = N_("The following authors were excluded from the statistics due to the specified exclusion patterns")
FILTERING_EMAIL_INFO_TEXT = N_("The authors with the following emails were excluded from the statistics due to the specified " \
                               "exclusion patterns")
FILTERING_COMMIT_INFO_TEXT = N_("The following commit revisions were excluded from the statistics due to the specified " \
                                "exclusion patterns")

class FilteringOutput(Outputable):
	@staticmethod
	def _output_html_section(info_string, filtered):
		filtering_xml = ""

		if filtered:
			filtering_xml += "<p>" + info_string + "."+ "</p>"

			for i in filtered:
				filtering_xml += "<p>" + i + "</p>"

		return filtering_xml

	def output_html(self):
		if has_filtered():
			filtering_xml = "<div><div class=\"box\">"
			FilteringOutput._output_html_section(_(FILTERING_INFO_TEXT), filters["file"][1])
			FilteringOutput._output_html_section(_(FILTERING_AUTHOR_INFO_TEXT), filters["author"][1])
			FilteringOutput._output_html_section(_(FILTERING_EMAIL_INFO_TEXT), filters["email"][1])
			FilteringOutput._output_html_section(_(FILTERING_COMMIT_INFO_TEXT), filters["revision"][1])
			filtering_xml += "</div></div>"

			print(filtering_xml)

	@staticmethod
	def _output_json_section(info_string, filtered, container_tagname):
		if filtered:
			message_json = "\t\t\t\t\"message\": \"" + info_string + "\",\n"
			filtering_json = ""

			for i in filtered:
				filtering_json += "\t\t\t\t\t\"" + i + "\",\n"
			else:
				filtering_json = filtering_json[:-3]

			return "\n\t\t\t\"{0}\": {{\n".format(container_tagname) + message_json + \
			"\t\t\t\t\"entries\": [\n" + filtering_json + "\"\n\t\t\t\t]\n\t\t\t},"

		return ""

	def output_json(self):
		if has_filtered():
			output = ",\n\t\t\"filtering\": {"
			output += FilteringOutput._output_json_section(_(FILTERING_INFO_TEXT), filters["file"][1], "files")
			output += FilteringOutput._output_json_section(_(FILTERING_AUTHOR_INFO_TEXT), filters["author"][1], "authors")
			output += FilteringOutput._output_json_section(_(FILTERING_EMAIL_INFO_TEXT), filters["email"][1], "emails")
			output += FilteringOutput._output_json_section(_(FILTERING_COMMIT_INFO_TEXT), filters["revision"][1], "revision")
			output = output[:-1]
			output += "\n\t\t}"
			print(output, end="")

	@staticmethod
	def _output_text_section(info_string, filtered):
		if filtered:
			print("\n" + textwrap.fill(info_string + ":", width=terminal.get_size()[0]))

			for i in filtered:
				(width, _unused) = terminal.get_size()
				print("...%s" % i[-width+3:] if len(i) > width else i)

	def output_text(self):
		FilteringOutput._output_text_section(_(FILTERING_INFO_TEXT), filters["file"][1])
		FilteringOutput._output_text_section(_(FILTERING_AUTHOR_INFO_TEXT), filters["author"][1])
		FilteringOutput._output_text_section(_(FILTERING_EMAIL_INFO_TEXT), filters["email"][1])
		FilteringOutput._output_text_section(_(FILTERING_COMMIT_INFO_TEXT), filters["revision"][1])

	@staticmethod
	def _output_xml_section(info_string, filtered, container_tagname):
		if filtered:
			message_xml = "\t\t\t<message>" + info_string + "</message>\n"
			filtering_xml = ""

			for i in filtered:
				filtering_xml += "\t\t\t\t<entry>" + i + "</entry>\n"

			print("\t\t<{0}>".format(container_tagname))
			print(message_xml + "\t\t\t<entries>\n" + filtering_xml + "\t\t\t</entries>\n")
			print("\t\t</{0}>".format(container_tagname))

	def output_xml(self):
		if has_filtered():
			print("\t<filtering>")
			FilteringOutput._output_xml_section(_(FILTERING_INFO_TEXT), filters["file"][1], "files")
			FilteringOutput._output_xml_section(_(FILTERING_AUTHOR_INFO_TEXT), filters["author"][1], "authors")
			FilteringOutput._output_xml_section(_(FILTERING_EMAIL_INFO_TEXT), filters["email"][1], "emails")
			FilteringOutput._output_xml_section(_(FILTERING_COMMIT_INFO_TEXT), filters["revision"][1], "revision")
			print("\t</filtering>")
