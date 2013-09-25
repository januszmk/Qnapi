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

import aeidon


class TestTMPlayerOneDigitHour(aeidon.TestCase):

    format = aeidon.formats.TMPLAYER
    name = "tmplayer-1"

    def setup_method(self, method):
        path = self.new_temp_file(self.format, self.name)
        self.file = aeidon.files.new(self.format, path, "ascii")

    def test_read(self):
        assert self.file.read()

    def test_write(self):
        self.file.write(self.file.read(), aeidon.documents.MAIN)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_sample_text(self.format, self.name)
        assert text == reference


class TestTMPlayerTwoDigitHour(TestTMPlayerOneDigitHour):

    name = "tmplayer-2"
