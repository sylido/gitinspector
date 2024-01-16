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

class CommentFirst():
	none = 0
	block = 1
	all = 2

class Language():
	def __init__(self, name, extensions, line_comment="//", start_comment_block="/*", end_comment_block="*/", 
			     comment_must_first=CommentFirst.none, nested_comments=False):
		self.name = name
		self.extensions = extensions
		self.line_comment = line_comment
		self.start_comment_block = start_comment_block
		self.end_comment_block = end_comment_block
		self.comment_must_first = comment_must_first
		self.nested_comments = nested_comments

_lang_list = [
	Language("Ada", ['ada', 'ads', 'adb'], "--", None, None),
	Language("C", ['c', 'h']),
	Language("C++", ['cc', 'cpp', 'hh', 'hpp']),
	Language("C#", ['cs']),
	Language("GNU Gettext", ['po', 'pot'], '#', None, None),
	Language("Go", ['go']),
	Language("Haskell", ['hs'], '--', '{-', '-}'),
	Language("HTML", ['html', 'xhtml'], None, '<!--', '-->'),
	Language("Java", ['java']),
	Language("JavaScript", ['js']),
	Language("Kotlin", ['kt'], nested_comments=True),
	Language("LaTeX", ['tex'], '%', r'\begin{comment}', r'\end{comment}', comment_must_first=CommentFirst.block),
	Language("ML", ['ml', 'mli'], None, '(*', '*)'),
	Language("OpenGL Shading Language", ['glsl', 'frag', 'vert', 'tese', 'tesc']),
	Language("Perl", ['pl'], '#', '=', '=cut'),
	Language("PHP", ['php']),
	Language("Python", ['py'], '#', "\"\"\"", "\"\"\"", comment_must_first=CommentFirst.block),
	Language("Ruby", ['rb'], "//", "=begin", "=end"),
	Language("Scala", ['scala']),
	Language("SQL", ['sql'], '--'),
	Language("XML", ['xml', 'jspx'], None, "<!--", "-->"),
]

class LangMapper():
	def __init__(self):
		self.map = {}
		# Populate the map with all the available extensions
		for lang in _lang_list:
			for ext in lang.extensions:
				self.map[ext] = lang

	def get_lang(self, ext):
		return self.map[ext]

def is_comment(extension, string):
	# TODO HERE
	return False

def handle_comment_block(is_inside_comment, extension, content):
	# TODO rework interface here
	return (0, False)
