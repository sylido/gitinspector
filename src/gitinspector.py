# coding: utf-8
#
# Copyright © 2024. All rights reserved.
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
import sys
from .blame import Blame
from .changes import Changes
from .format import available_formats, is_interactive_format, output_header, output_footer
from .metrics import MetricsLogic
from .output import outputable
from .output.blameoutput import BlameOutput
from .output.changesoutput import ChangesOutput
from .output.extensionsoutput import ExtensionsOutput
from .output.filteringoutput import FilteringOutput
from .output.metricsoutput import MetricsOutput
from .output.responsibilitiesoutput import ResponsibilitiesOutput
from .output.timelineoutput import TimelineOutput
from . import terminal


def _config_error(msg):
	print(msg, file=sys.stderr)
	sys.exit(2)

version = "0.5.0dev"
def _version_output():
	_doc = """Copyright © 2024. All rights reserved.
	License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
	This is free software: you are free to change and redistribute it.
	There is NO WARRANTY, to the extent permitted by law."""
	print("gitinspector {0}\n".format(version) + _doc)


import subprocess
def _validate_search_path(path):
	if path != '':
		from pathlib import Path
		p = Path(path)
		if not p.exists():
			_config_error(f"Given search path \"{path}\" does not exist!")
		if not p.isdir():
			_config_error(f"Given search path \"{path}\" is not a directory!")
	else:
		# don't have to check existence if we use cwd
		path = os.getcwd()
	
	# Check for git and find the top level of this repo
	res = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path, stdout=subprocess.PIPE, encoding='utf-8')
	if res.returncode != 0:
		_config_error(f"Given search path\"{path}\" is neither a git repo or in a git repo!")
	
	class Repo():
		def __init__(self, top, search):
			last = top.rindex(os.sep, 2) # 2 is backward index to avoid trailing sep
			end = top[last + 1:]
			if end.endswith(os.sep):
				end = end[:len(end) - 1]
			self.name = end
			self.top = top
			self.search = search

	return Repo(res.stdout.rstrip(), path)


def main():
	terminal.check_terminal_encoding()

	import argparse
	parser = argparse.ArgumentParser(
		prog="gitinspector",
		description="Collects and displays authorship and composition statistics about "
					"the given directory (in a git repo).",
		epilog="gitinspector will filter statistics to only include commits that modify, add, "
			   "or remove one of the specified extensions, see -f or --file-types for more information.\n"
			   "gitinspector requires that the git executable is available in your PATH.")
	parser.add_argument("-f", "--file-types",
		help="a comma separated list of file extensions to include when computing statistics. By default, all "
			 "extensions are considered (*).")
	parser.add_argument("-o", "--output",
		help="define in which format output should be generated. Default is 'text'.",
		choices=available_formats,
		default="text")
	parser.add_argument("-l", "--lines", action='store_true',
		help="analyzes lines of code (for supported languages)")
	parser.add_argument("-r", "--responsibilities", action='store_true',
		help="report which author seems most responsible for each file")
	parser.add_argument("--since", help="only show statistics for commits more recent than a specific date")
	parser.add_argument("-t", "--timeline", action="store_true",
		help="show commit timeline, including author names")
	parser.add_argument("--until", help="only show statistics for commits older than specific date")
	parser.add_argument("-w", "--weeks", action="store_true",
		help="show all statistical information in weeks instead of months")
	parser.add_argument("-x", "--exclude",
		help="specify an exclusion pattern describing the file paths, revisions, revisions with certain commit messages, "
			 "author names, or author emails which should be excluded from statistics; can be specified multiple times")
	parser.add_argument("--version", action="store_true", help="output version information and exit")

	parser.add_argument("search_path", default='', nargs='?',
		help="optional path to a directory to search. If none specified, cwd searched instead.")
	args = parser.parse_args()

	if args.version:
		_version_output()
		return

	if sys.version_info < (3, 6):
		python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
		_config_error("gitinspector requires at least Python 3.6 to run (version {0} was found).".format(python_version))

	# Check that git is defined and that the provided search path exists AND is part of some git repository
	repo = _validate_search_path(args.search_path)

	terminal.skip_escapes(not sys.stdout.isatty())
	terminal.set_stdout_encoding()

	changes = Changes(repo, False)
	summed_blames = Blame(repo, False, args.weeks, changes)
	summed_changes = changes

	metrics = False
	responsibilities = False

	if metrics:
		summed_metrics = MetricsLogic()

	if sys.stdout.isatty() and is_interactive_format():
		terminal.clear_row()

	output_header([repo])
	outputable.output(ChangesOutput(summed_changes))

	if summed_changes.get_commits():
		outputable.output(BlameOutput(summed_changes, summed_blames))

		if args.timeline:
			outputable.output(TimelineOutput(summed_changes, args.weeks))

		if metrics:
			outputable.output(MetricsOutput(summed_metrics))

		if responsibilities:
			outputable.output(ResponsibilitiesOutput(summed_changes, summed_blames))

		outputable.output(FilteringOutput())

	output_footer()


if __name__ == "__main__":
	main()
