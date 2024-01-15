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

try:
	from shlex import quote
except ImportError:
	from pipes import quote

_since = ""

_until = ""

_ref = "HEAD"

def has_interval():
	return _since + _until != ""

def get_since():
	return _since

def set_since(since):
	global _since
	_since = "--since=" + quote(since)

def get_until():
	return _until

def set_until(until):
	global _until
	_until = "--until=" + quote(until)

def get_ref():
	return _ref

def set_ref(ref):
	global __ref__
	_ref = ref
