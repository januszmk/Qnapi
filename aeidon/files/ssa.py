# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Sub Station Alpha file."""

import aeidon
import re

__all__ = ("SubStationAlpha",)


class SubStationAlpha(aeidon.SubtitleFile):

    """
    Sub Station Alpha file.

    :ivar event_fields: Tuple of field names for the ``[Events]`` section
    """

    _re_file_time = re.compile(r"^(-?)(.+)$")
    _re_separator = re.compile(r",\s*")
    _re_subtitle_time = re.compile(r"(-?)\d(.{10})\d")
    format = aeidon.formats.SSA
    mode = aeidon.modes.TIME

    def __init__(self, path, encoding, newline=None):
        """Initialize a :class:`SubStationAlpha` object."""
        aeidon.SubtitleFile.__init__(self, path, encoding, newline)
        self.event_fields = ("Marked",
                             "Start",
                             "End",
                             "Style",
                             "Name",
                             "MarginL",
                             "MarginR",
                             "MarginV",
                             "Effect",
                             "Text",)

    def _decode_field(self, field_name, value, subtitle):
        """Save string `value` from file as a subtitle attribute."""
        if field_name == "Marked":
            value = value.split("=")[-1]
            return setattr(subtitle.ssa, "marked", int(value))
        if field_name == "Start":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "start_time", value)
        if field_name == "End":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "end_time", value)
        if field_name == "Text":
            value = value.replace("\\n", "\n")
            value = value.replace("\\N", "\n")
            return setattr(subtitle, "main_text", value)
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = aeidon.util.title_to_lower_case(field_name)
            return setattr(subtitle.ssa, name, int(value))
        # Set plain string container attribute value.
        name = aeidon.util.title_to_lower_case(field_name)
        setattr(subtitle.ssa, name, value)

    def _encode_field(self, field_name, subtitle, doc):
        """Return value of field as string to be written to file."""
        if field_name == "Marked":
            return "Marked={:d}".format(subtitle.ssa.marked)
        if field_name == "Start":
            value = subtitle.calc.round(subtitle.start_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "End":
            value = subtitle.calc.round(subtitle.end_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "Text":
            value = subtitle.get_text(doc)
            return value.replace("\n", "\\N")
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = aeidon.util.title_to_lower_case(field_name)
            return "{:04d}".format(getattr(subtitle.ssa, name))
        # Return plain string container attribute value.
        name = aeidon.util.title_to_lower_case(field_name)
        return getattr(subtitle.ssa, name)

    def _read_header(self, lines):
        """Read header and remove its lines."""
        self.header = ""
        while not lines[0].startswith("[Events]"):
            self.header += "\n"
            self.header += lines.pop(0)
        self.header = self.header.strip()

    def copy_from(self, other):
        """Copy generic properties from `other` file."""
        aeidon.SubtitleFile.copy_from(self, other)
        if self.format == other.format:
            self.event_fields = tuple(other.event_fields)

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        lines = self._read_lines()
        self._read_header(lines)
        for line in (x for x in lines if x.startswith("Format:")):
            line = line.replace("Format:", "").strip()
            fields = self._re_separator.split(line)
            indices = dict((x, fields.index(x)) for x in fields)
            max_split = len(fields) - 1
        for line in (x for x in lines if x.startswith("Dialogue:")):
            subtitle = self._get_subtitle()
            line = line.replace("Dialogue:", "").lstrip()
            values = self._re_separator.split(line, max_split)
            for name, index in indices.items():
                self._decode_field(name, values[index], subtitle)
            subtitles.append(subtitle)
        self.event_fields = tuple(fields)
        return subtitles

    def write_to_file(self, subtitles, doc, fobj):
        """
        Write `subtitles` from `doc` to `fobj`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        n = self.newline.value
        header = self.header.replace("\n", n)
        fobj.write("{}{}{}".format(header, n, n))
        fobj.write("[Events]{}".format(n))
        fobj.write("Format: {}{}".format(", ".join(self.event_fields), n))
        for subtitle in subtitles:
            values = [self._encode_field(x, subtitle, doc)
                      for x in self.event_fields]

            fobj.write("Dialogue: {}{}".format(",".join(values), n))
