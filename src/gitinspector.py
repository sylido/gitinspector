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

import atexit
import getopt
import os
import sys
from .blame import Blame
from .changes import Changes
from .config import GitConfig
from .metrics import MetricsLogic
from . import (basedir, clone, extensions, filtering, format, help, interval,
               localization, optval, terminal, version)
from .output import outputable
from .output.blameoutput import BlameOutput
from .output.changesoutput import ChangesOutput
from .output.extensionsoutput import ExtensionsOutput
from .output.filteringoutput import FilteringOutput
from .output.metricsoutput import MetricsOutput
from .output.responsibilitiesoutput import ResponsibilitiesOutput
from .output.timelineoutput import TimelineOutput

localization.init()

class Runner(object):
	def __init__(self):
		self.hard = False
		self.include_metrics = False
		self.list_file_types = False
		self.localize_output = False
		self.responsibilities = False
		self.grading = False
		self.timeline = False
		self.useweeks = False

	def process(self, repos):
		localization.check_compatibility(version.__version__)

		if not self.localize_output:
			localization.disable()

		terminal.skip_escapes(not sys.stdout.isatty())
		terminal.set_stdout_encoding()
		previous_directory = os.getcwd()
		summed_blames = Blame.__new__(Blame)
		summed_changes = Changes.__new__(Changes)
		summed_metrics = MetricsLogic.__new__(MetricsLogic)

		for repo in repos:
			os.chdir(repo.location)
			repo = repo if len(repos) > 1 else None
			changes = Changes(repo, self.hard)
			summed_blames += Blame(repo, self.hard, self.useweeks, changes)
			summed_changes += changes

			if self.include_metrics:
				summed_metrics += MetricsLogic()

			if sys.stdout.isatty() and format.is_interactive_format():
				terminal.clear_row()
		else:
			os.chdir(previous_directory)

		format.output_header(repos)
		outputable.output(ChangesOutput(summed_changes))

		if summed_changes.get_commits():
			outputable.output(BlameOutput(summed_changes, summed_blames))

			if self.timeline:
				outputable.output(TimelineOutput(summed_changes, self.useweeks))

			if self.include_metrics:
				outputable.output(MetricsOutput(summed_metrics))

			if self.responsibilities:
				outputable.output(ResponsibilitiesOutput(summed_changes, summed_blames))

			outputable.output(FilteringOutput())

			if self.list_file_types:
				outputable.output(ExtensionsOutput())

		format.output_footer()
		os.chdir(previous_directory)

def _check_python_version():
	if sys.version_info < (3, 6):
		python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
		sys.exit(_("gitinspector requires at least Python 2.6 to run (version {0} was found).").format(python_version))

def _get_validated_git_repos(repos_relative):
	if not repos_relative:
		repos_relative = "."

	repos = []

	#Try to clone the repos or return the same directory and bail out.
	for repo in repos_relative:
		cloned_repo = clone.create(repo)

		if cloned_repo.name == None:
			cloned_repo.location = basedir.get_basedir_git(cloned_repo.location)
			cloned_repo.name = os.path.basename(cloned_repo.location)

		repos.append(cloned_repo)

	return repos

def main():
	terminal.check_terminal_encoding()
	terminal.set_stdin_encoding()
	argv = terminal.convert_command_line_to_utf8()

	import argparse
	parser = argparse.ArgumentParser(prog="gitinspector",
								     description="Collects and displays authorship and composition statistics about "
									             "the given directory (in a git repo).",
									 epilog="gitinspector will filter statistics to only include commits that modify, add, "
									 "or remove one of the specified extensions, see -f or --file-types for more information.\n"
									 "gitinspector requires that the git executable is available in your PATH.")
	parser.add_argument("-f", "--file-types",
			help="a comma separated list of file extensions to include when computing statistics. By default, all "
			"extensions are considered (*).")
	parser.add_argument("-F", "--format",
			help="define in which format output should be generated. Options include: " + (",".join(__available_formats__)) +
			". Default is 'text'.",
			choices=__available_formats__,
			default="text")
	parser.add_argument("-m", "--metrics", action='store_true',
			help="include checks for certain metrics during the analysis of commits")
	parser.add_argument("-r", "--responsibilities", action='store_true',
			help="show which files the different authors seem most responsible for")
	parser.add_argument("--since", help="only show statistics for commits more recent than a specific date")
	parser.add_argument("-T", "--timeline", action="store_true",
			help="show commit timeline, including author names")
	parser.add_argument("--until", help="only show statistics for commits older than specific date")
	parser.add_argument("-w", "--weeks", action="store_true",
			help="show all statistical information in weeks instead of months")
	parser.add_argument("-x", "--exclude",
			help="specify an exclusion pattern describing the file paths, revisions, revisions with certain commit messages, "
			"author names, or author emails which should be excluded from statistics; can be specified multiple times")
	parser.add_argument("--version", action="store_true", help="output version information and exit")
	args = parser.parse_args()


	exit()

	run = Runner()
	repos = []

	try:
		opts, args = optval.gnu_getopt(argv[1:], "f:F:hHlLmrTwx:", ["exclude=", "file-types=", "format=",
		                                         "hard:true", "help", "list-file-types:true", "localize-output:true",
		                                         "metrics:true", "responsibilities:true", "since=", "grading:true",
		                                         "timeline:true", "until=", "version", "weeks:true"])
		repos = _get_validated_git_repos(set(args))

		#We need the repos above to be set before we read the git config.
		GitConfig(run, repos[-1].location).read()
		clear_x_on_next_pass = True

		for o, a in opts:
			if o in("-h", "--help"):
				help.output()
				sys.exit(0)
			elif o in("-f", "--file-types"):
				extensions.define(a)
			elif o in("-F", "--format"):
				if not format.select(a):
					raise format.InvalidFormatError(_("specified output format not supported."))
			elif o == "-H":
				run.hard = True
			elif o == "--hard":
				run.hard = optval.get_boolean_argument(a)
			elif o == "-l":
				run.list_file_types = True
			elif o == "--list-file-types":
				run.list_file_types = optval.get_boolean_argument(a)
			elif o == "-L":
				run.localize_output = True
			elif o == "--localize-output":
				run.localize_output = optval.get_boolean_argument(a)
			elif o == "-m":
				run.include_metrics = True
			elif o == "--metrics":
				run.include_metrics = optval.get_boolean_argument(a)
			elif o == "-r":
				run.responsibilities = True
			elif o == "--responsibilities":
				run.responsibilities = optval.get_boolean_argument(a)
			elif o == "--since":
				interval.set_since(a)
			elif o == "--version":
				version.output()
				sys.exit(0)
			elif o == "--grading":
				grading = optval.get_boolean_argument(a)
				run.include_metrics = grading
				run.list_file_types = grading
				run.responsibilities = grading
				run.grading = grading
				run.hard = grading
				run.timeline = grading
				run.useweeks = grading
			elif o == "-T":
				run.timeline = True
			elif o == "--timeline":
				run.timeline = optval.get_boolean_argument(a)
			elif o == "--until":
				interval.set_until(a)
			elif o == "-w":
				run.useweeks = True
			elif o == "--weeks":
				run.useweeks = optval.get_boolean_argument(a)
			elif o in("-x", "--exclude"):
				if clear_x_on_next_pass:
					clear_x_on_next_pass = False
					filtering.clear()
				filtering.add(a)

		_check_python_version()
		run.process(repos)

	except (filtering.InvalidRegExpError, format.InvalidFormatError, optval.InvalidOptionArgument, getopt.error) as exception:
		print(sys.argv[0], "\b:", exception.msg, file=sys.stderr)
		print(("Try `{0} --help' for more information.").format(sys.argv[0]), file=sys.stderr)
		sys.exit(2)

@atexit.register
def cleanup():
	clone.delete()

if __name__ == "__main__":
	main()
