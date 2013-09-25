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

"""Reading and parsing data from subtitle files."""

import aeidon
import bisect


class OpenAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """Reading and parsing data from subtitle files."""

    def _align_translations_by_number(self, subtitles):
        """Add translation texts by aligning subtitle numbers."""
        indices = list(range(len(self.subtitles), len(subtitles)))
        self.insert_subtitles(indices, register=None)
        for i, subtitle in enumerate(subtitles):
            self.subtitles[i].tran_text = subtitle.main_text

    def _align_translations_by_position(self, subtitles):
        """Add translation texts by aligning subtitle positions."""
        subtitles = [x.copy() for x in subtitles]
        mode = self.main_file.mode
        i = 0
        while subtitles:
            # Examine subtitles to be added one-by-one by comparing
            # their temporal middle positions with the start and end
            # positions of existing subtitles.
            ts = subtitles[0].get_start(mode)
            te = subtitles[0].get_end(mode)
            tm = self.calc.get_middle(ts, te)
            while True:
                # Skip over existing subtitles when
                # no suitable match found among translations.
                if i == len(self.subtitles): break
                ms = self.subtitles[i].get_start(mode)
                me = self.subtitles[i].get_end(mode)
                if not self.calc.is_earlier(me, tm): break
                i += 1
            if i == len(self.subtitles) or self.calc.is_later(ms, tm):
                # Add a new subtitle when no suitable match
                # found among existing subtitles.
                subtitle = self.new_subtitle()
                subtitle.start = subtitles[0].start
                subtitle.end = subtitles[0].end
                self.subtitles.insert(i, subtitle)
            self.subtitles[i].tran_text = subtitles[0].main_text
            subtitles.pop(0)
            i += 1

    def _read_file(self, file):
        """
        Read `file` and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        Raise :exc:`aeidon.ParseError` if parsing fails.
        """
        try:
            return file.read()
        except (IOError, UnicodeError):
            raise
        except Exception:
            if not aeidon.DEBUG:
                raise aeidon.ParseError("Failed to parse file {}"
                                        .format(repr(file.path)))

            raise

    def _sort_subtitles_ensure(self, value, subtitles):
        sorted_subtitles, sort_count = value
        for i in range(len(sorted_subtitles) - 1):
            assert sorted_subtitles[i] <= sorted_subtitles[i + 1]

    def _sort_subtitles(self, subtitles):
        """
        Sort and return `subtitles` and sort count.

        `subtitles` are sorted according to their start positions. Sort count
        is the amount of subtitles that needed to be moved in order to arrange
        them in ascending chronological order.
        """
        sort_count = 0
        sorted_subtitles = []
        while subtitles:
            subtitle = subtitles.pop(0)
            index = bisect.bisect(sorted_subtitles, subtitle)
            if index < len(sorted_subtitles):
                sort_count += 1
            sorted_subtitles.insert(index, subtitle)
        return sorted_subtitles, sort_count

    @aeidon.deco.export
    def open(self, doc, path, encoding=None, *args, **kwargs):
        """
        Read and parse subtitle data for `doc` from `path`.

        `encoding` can be ``None`` to use the system default encoding. Return
        the amount of subtitles that needed to be moved in order to arrange
        them in ascending chronological order.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        Raise :exc:`aeidon.FormatError` if unable to detect format.
        Raise :exc:`aeidon.ParseError` if parsing fails.
        """
        if doc == aeidon.documents.MAIN:
            return self.open_main(path, encoding, *args, **kwargs)
        if doc == aeidon.documents.TRAN:
            return self.open_translation(path, encoding, *args, **kwargs)
        raise ValueError("Invalid document: {}".format(repr(doc)))

    def open_main_require(self, path, encoding):
        assert aeidon.encodings.is_valid_code(encoding)

    def open_main_ensure(self, value, path, encoding):
        assert self.main_file is not None
        assert self.main_changed == 0
        assert self.tran_file is None
        assert self.tran_changed is None

    @aeidon.deco.export
    @aeidon.deco.notify_frozen
    def open_main(self, path, encoding=None):
        """
        Read and parse subtitle data for main file from `path`.

        `encoding` can be ``None`` to use the system default encoding. Return
        the amount of subtitles that needed to be moved in order to arrange
        them in ascending chronological order.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        Raise :exc:`aeidon.FormatError` if unable to detect format.
        Raise :exc:`aeidon.ParseError` if parsing fails.
        """
        encoding = encoding or aeidon.util.get_default_encoding()
        # Check for a Unicode BOM first to avoid getting a FormatError in the
        # case where an unsuitable encoding decodes a file into garbage without
        # raising a UnicodeDecodeError. If a Unicode BOM is found, use the
        # corresponding Unicode encoding to open the file.
        bom_encoding = aeidon.encodings.detect_bom(path)
        if not bom_encoding in (encoding, None):
            return self.open_main(path, bom_encoding)
        format = aeidon.util.detect_format(path, encoding)
        self.main_file = aeidon.files.new(format, path, encoding)
        subtitles = self._read_file(self.main_file)
        self.subtitles, sort_count = self._sort_subtitles(subtitles)
        self.set_framerate(self.framerate, register=None)
        if self.main_file.format == aeidon.formats.MPSUB:
            # Get framerate from MPsub header.
            if self.main_file.framerate is not None:
                self.set_framerate(self.main_file.framerate, register=None)
        self.main_changed = 0
        # Deactivate possible translation file.
        self.tran_file = None
        self.tran_changed = None
        self.emit("main-file-opened", self.main_file)
        return sort_count

    def open_translation_require(self, path, encoding, align_method=None):
        assert self.main_file is not None
        assert aeidon.encodings.is_valid_code(encoding)

    def open_translation_ensure(self, *args, **kwargs):
        assert self.tran_file is not None
        assert self.tran_changed == 0

    @aeidon.deco.export
    @aeidon.deco.notify_frozen
    def open_translation(self, path, encoding=None, align_method=None):
        """
        Read and parse subtitle data for translation file from `path`.

        `encoding` can be ``None`` to use the system default encoding.
        `align_method` specifies how translation texts are attached to existing
        subtitles. :attr:`aeidon.align_methods.NUMBER` is the simple way, which
        adds the translation texts in order, one-by-one to the exising
        subtitles. :attr:`aeidon.align_methods.POSITION` (the default) is the
        smarter way, which compares the position data in the translation
        subtitles with the existing subtitles, skips and inserts subtitles as
        needed to have at least a rough chronological match. The latter thus
        takes into account that not all subtitles are translated, or vice versa
        and that one main subtitle may correspond to two translation subtitles,
        or vice versa, as per length restrictions or whatever.

        Return the amount of subtitles that needed to be moved in order to
        arrange them in ascending chronological order.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        Raise :exc:`aeidon.FormatError` if unable to detect format.
        Raise :exc:`aeidon.ParseError` if parsing fails.
        """
        encoding = encoding or aeidon.util.get_default_encoding()
        align_method = align_method or aeidon.align_methods.POSITION
        # Check for a Unicode BOM first to avoid getting a FormatError in the
        # case where an unsuitable encoding decodes a file into garbage without
        # raising a UnicodeDecodeError. If a Unicode BOM is found, use the
        # corresponding Unicode encoding to open the file.
        bom_encoding = aeidon.encodings.detect_bom(path)
        if bom_encoding not in (encoding, None):
            return self.open_translation(path, bom_encoding, align_method)
        format = aeidon.util.detect_format(path, encoding)
        self.tran_file = aeidon.files.new(format, path, encoding)
        subtitles = self._read_file(self.tran_file)
        subtitles, sort_count = self._sort_subtitles(subtitles)
        for subtitle in subtitles:
            subtitle.framerate = self.framerate
        for subtitle in self.subtitles:
            subtitle.tran_text = ""
        blocked = self.block("subtitles-inserted")
        if align_method == aeidon.align_methods.POSITION:
            self._align_translations_by_position(subtitles)
        if align_method == aeidon.align_methods.NUMBER:
            self._align_translations_by_number(subtitles)
        self.unblock("subtitles-inserted", blocked)
        self.tran_changed = 0
        self.emit("translation-file-opened", self.tran_file)
        return sort_count
