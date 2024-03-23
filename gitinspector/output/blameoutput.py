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


import json
import sys
import textwrap
from ..localization import N_
from .. import format, gravatar, terminal
from ..blame import Blame
from .outputable import Outputable

BLAME_INFO_TEXT = N_(
  "Below are the number of rows from each author that have survived and are still " "intact in the current revision"
)


class BlameOutput(Outputable):
  def __init__(self, changes, blame):
    if format.is_interactive_format():
      print("")

    self.changes = changes
    self.blame   = blame
    Outputable.__init__(self)

  def output_html(self):
    blame_html   = '<div><div class="box">'
    blame_html   += "<p>" + _(BLAME_INFO_TEXT) + '.</p><div><table id="blame" class="git">'
    blame_html   += "<thead><tr> <th>{0}</th> <th>{1}</th> <th>{2}</th> <th>{3}</th> <th>{4}</th> <th>{5}</th> </tr></thead>".format(
      _("Author"), _("Rows"), _("Stability"), _("Age"), _("% in comments"), _("% of Work")
    )
    blame_html   += "<tbody>"
    chart_data   =   ""
    blames       =  sorted(self.blame.get_summed_blames().items())
    # for bl in blames:
    #   print("bl", bl[1])
    # return ""
    total_blames =  0

    for i in blames:
      total_blames += i[1].rows

    for i, entry in enumerate(blames):
      work_percentage  = str("{0:.2f}".format(100.0 * entry[1].rows / total_blames))
      blame_html      += "<tr " + ('class="odd">' if i % 2 == 1 else ">")

      if format.get_selected() == "html":
        author_email =  self.changes.get_latest_email_by_author(entry[0])
        blame_html   += '<td><img src="{0}"/>{1}</td>'.format(gravatar.get_url(author_email), entry[0])
      else:
        blame_html   += "<td>" + entry[0] + "</td>"

      blame_html += "<td>{:,}</td>".format(entry[1].rows)
      blame_html += "<td>" + ("{0:.1f}".format(Blame.get_stability(entry[0], entry[1].rows, self.changes)) + "</td>")
      blame_html += "<td>" + "{0:.1f}".format(float(entry[1].skew) / entry[1].rows) + "</td>"
      blame_html += "<td>" + "{0:.2f}".format(100.0 * entry[1].comments / entry[1].rows) + "</td>"
      blame_html += "<td>" + work_percentage + "</td>"
      blame_html += "</tr>"
      chart_data += "{{label: {0}, data: {1}}}".format(json.dumps(entry[0]), work_percentage)

      if blames[-1] != entry:
        chart_data += ", "

    blame_html += '<tfoot><tr> <td colspan="6">&nbsp;</td> </tr></tfoot></tbody></table>'
    blame_html += '<div class="chart" id="blame_chart"></div></div>'
    blame_html += '<script type="text/javascript">'
    blame_html += '    blame_plot = $.plot($("#blame_chart"), [{0}], {{'.format(chart_data)
    blame_html += "        series: {"
    blame_html += "            pie: {"
    blame_html += "                innerRadius: 0.4,"
    blame_html += "                show: true,"
    blame_html += "                combine: {"
    blame_html += "                    threshold: 0.03,"
    blame_html += '                    label: "' + _("Minor Authors") + '"'
    blame_html += "                }"
    blame_html += "            }"
    blame_html += "        }, grid: {"
    blame_html += "            hoverable: true"
    blame_html += "        }"
    blame_html += "    });"
    blame_html += "</script></div></div>"

    # print(blame_html)
    return blame_html

  def output_json(self):
    message_json = '\t\t\t"message": "' + _(BLAME_INFO_TEXT) + '",\n'
    blame_json   = ""
    total_blames = 0

    blames = self.blame.get_summed_blames().items()
    for i in blames:
      total_blames += i[1].rows

    for i in sorted(self.blame.get_summed_blames().items()):
      author_email                = self.changes.get_latest_email_by_author(i[0])
      name_json                   = '\t\t\t\t"name": "' + i[0] + '",\n'
      email_json                  = '\t\t\t\t"email": "' + author_email + '",\n'
      gravatar_json               = '\t\t\t\t"gravatar": "' + gravatar.get_url(author_email) + '",\n'
      rows_json                   = '\t\t\t\t"rows": ' + str(i[1].rows) + ",\n"
      stability_json              = '\t\t\t\t"stability": ' + "{0:.1f}".format(Blame.get_stability(i[0], i[1].rows, self.changes)) + ",\n"
      age_json                    = '\t\t\t\t"age": ' + "{0:.1f}".format(float(i[1].skew) / i[1].rows) + ",\n"
      percentage_in_comments_json = (
        '\t\t\t\t"percentage_in_comments": ' + "{0:.2f}".format(100.0 * i[1].comments / i[1].rows) + "\n"
      )
      percentage_work_json = (
        '\t\t\t\t"percentage_work": ' + str("{0:.2f}".format(100.0 * i[1].rows / total_blames)) + "\n"
      )
      blame_json += (
        "{\n"
        + name_json
        + email_json
        + gravatar_json
        + rows_json
        + stability_json
        + age_json
        + percentage_in_comments_json
        + percentage_work_json
        + "\t\t\t},"
      )
    else:
      blame_json = blame_json[:-1]

    # print(',\n\t\t"blame": {\n' + message_json + '\t\t\t"authors": [\n\t\t\t' + blame_json + "]\n\t\t}", end="")
    return ',\n\t\t"blame": {\n' + message_json + '\t\t\t"authors": [\n\t\t\t' + blame_json + "]\n\t\t}" + ""

  def output_text(self):
    if sys.stdout.isatty() and format.is_interactive_format():
      terminal.clear_row()

    print(textwrap.fill(_(BLAME_INFO_TEXT) + ":", width=terminal.get_size()[0]) + "\n")
    terminal.printb(
      terminal.ljust(_("Author"), 21)
      + terminal.rjust(_("Rows"), 10)
      + terminal.rjust(_("Stability"), 15)
      + terminal.rjust(_("Age"), 13)
      + terminal.rjust(_("% in comments"), 20)
    )

    for i in sorted(self.blame.get_summed_blames().items()):
      print(terminal.ljust(i[0], 20)[0 : 20 - terminal.get_excess_column_count(i[0])], end=" ")
      print(str(i[1].rows).rjust(10), end=" ")
      print("{0:.1f}".format(Blame.get_stability(i[0], i[1].rows, self.changes)).rjust(14), end=" ")
      print("{0:.1f}".format(float(i[1].skew) / i[1].rows).rjust(12), end=" ")
      print("{0:.2f}".format(100.0 * i[1].comments / i[1].rows).rjust(19))

  def output_xml(self):
    message_xml = "\t\t<message>" + _(BLAME_INFO_TEXT) + "</message>\n"
    blame_xml   = ""

    for i in sorted(self.blame.get_summed_blames().items()):
      author_email               = self.changes.get_latest_email_by_author(i[0])
      name_xml                   = "\t\t\t\t<name>" + i[0] + "</name>\n"
      email_xml                  = "\t\t\t\t<email>" + author_email + "</email>\n"
      gravatar_xml               = "\t\t\t\t<gravatar>" + gravatar.get_url(author_email) + "</gravatar>\n"
      rows_xml                   = "\t\t\t\t<rows>" + str(i[1].rows) + "</rows>\n"
      stability_xml              = ("\t\t\t\t<stability>" + "{0:.1f}".format(Blame.get_stability(i[0], i[1].rows, self.changes)) + "</stability>\n")
      age_xml                    = "\t\t\t\t<age>" + "{0:.1f}".format(float(i[1].skew) / i[1].rows) + "</age>\n"
      percentage_in_comments_xml = (
        "\t\t\t\t<percentage-in-comments>" + "{0:.2f}".format(100.0 * i[1].comments / i[1].rows) + "</percentage-in-comments>\n"
      )
      blame_xml                  += (
        "\t\t\t<author>\n"
        + name_xml
        + email_xml
        + gravatar_xml
        + rows_xml
        + stability_xml
        + age_xml
        + percentage_in_comments_xml
        + "\t\t\t</author>\n"
      )

    # print("\t<blame>\n" + message_xml + "\t\t<authors>\n" + blame_xml + "\t\t</authors>\n\t</blame>")
    return "\t<blame>\n" + message_xml + "\t\t<authors>\n" + blame_xml + "\t\t</authors>\n\t</blame>"
