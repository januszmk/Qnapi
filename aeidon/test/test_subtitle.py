# -*- coding: utf-8 -*-

# Copyright (C) 2007-2009,2011-2012 Osmo Salomaa
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


class TestSubtitle(aeidon.TestCase):

    def setup_method(self, method):
        self.tsub = aeidon.Subtitle()
        self.tsub.mode = aeidon.modes.TIME
        self.tsub.framerate = aeidon.framerates.FPS_25_000
        self.tsub.start = "00:00:01.000"
        self.tsub.end = "00:00:03.000"
        self.tsub.main_text = "main"
        self.tsub.tran_text = "translation"
        self.fsub = aeidon.Subtitle()
        self.fsub.mode = aeidon.modes.FRAME
        self.fsub.framerate = aeidon.framerates.FPS_25_000
        self.fsub.start = 100
        self.fsub.end = 300
        self.fsub.main_text = "main"
        self.fsub.tran_text = "translation"

    def test___eq__(self):
        assert self.tsub == self.tsub
        assert self.fsub == self.fsub
        assert self.tsub != self.fsub

    def test___getattr__(self):
        assert "ssa" not in dir(self.tsub)
        self.tsub.ssa.style = "test"
        assert "ssa" in dir(self.tsub)

    def test___getattr____attribute_error(self):
        self.assert_raises(AttributeError,
                           lambda: self.tsub.xxx)

    def test___lt__(self):
        assert self.tsub <  self.fsub
        assert self.fsub >  self.tsub
        assert self.tsub >= self.tsub
        assert self.tsub <= self.tsub
        assert self.fsub >= self.fsub
        assert self.fsub <= self.fsub

    def test_convert_framerate__frame(self):
        self.fsub.start = 100
        self.fsub.end = 200
        framerate = aeidon.framerates.FPS_23_976
        self.fsub.convert_framerate(framerate)
        assert self.fsub.framerate == framerate
        assert self.fsub.start == 96
        assert self.fsub.end == 192

    def test_convert_framerate__time(self):
        self.tsub.start = "00:00:01.000"
        self.tsub.end = "00:00:02.000"
        framerate = aeidon.framerates.FPS_23_976
        self.tsub.convert_framerate(framerate)
        assert self.tsub.framerate == framerate
        assert self.tsub.start == "00:00:01.043"
        assert self.tsub.end == "00:00:02.085"

    def test_copy(self):
        copy = self.tsub.copy()
        assert copy is not self.tsub
        assert "ssa" not in dir(copy)
        self.tsub.ssa.style = "test"
        copy = self.tsub.copy()
        assert copy.ssa.style == "test"
        names = dir(self.tsub.ssa)
        for name in (x for x in names if not x.startswith("_")):
            value = getattr(self.tsub.ssa, name)
            assert getattr(copy.ssa, name) == value
        assert copy.ssa is not self.tsub.ssa

    def test_duration__get(self):
        assert self.tsub.duration == "00:00:02.000"
        assert self.fsub.duration == 200

    def test_duration__set_frame(self):
        self.fsub.duration = 500
        assert self.fsub.end_frame == 600
        self.fsub.duration = "00:00:10.000"
        assert self.fsub.end_frame == 350
        self.fsub.duration = 5.0
        assert self.fsub.end_frame == 225

    def test_duration__set_time(self):
        self.tsub.duration = "00:00:10.000"
        assert self.tsub.end_time == "00:00:11.000"
        self.tsub.duration = 500
        assert self.tsub.end_time == "00:00:21.000"
        self.tsub.duration = 10.0
        assert self.tsub.end_time == "00:00:11.000"

    def test_duration_frame__get(self):
        assert self.tsub.duration_frame == 50
        assert self.fsub.duration_frame == 200

    def test_duration_frame__set(self):
        self.fsub.duration_frame = 500
        assert self.fsub.end_frame == 600

    def test_duration_seconds__get(self):
        assert self.tsub.duration_seconds == 2.0
        assert self.fsub.duration_seconds == 8.0

    def test_duration_seconds__set(self):
        self.tsub.duration_seconds = 3.0
        assert self.tsub.end_seconds == 4.0

    def test_duration_time__get(self):
        assert self.tsub.duration_time == "00:00:02.000"
        assert self.fsub.duration_time == "00:00:08.000"

    def test_duration_time__set(self):
        self.tsub.duration_time = "00:00:03.000"
        assert self.tsub.end_time == "00:00:04.000"

    def test_end__get(self):
        assert self.tsub.end == "00:00:03.000"
        assert self.fsub.end == 300

    def test_end__set_frame(self):
        self.fsub.end = 500
        assert self.fsub.end_frame == 500
        self.fsub.end = "00:00:10.000"
        assert self.fsub.end_frame == 250
        self.fsub.end = 5.0
        assert self.fsub.end_frame == 125

    def test_end__set_time(self):
        self.tsub.end = "00:00:10.000"
        assert self.tsub.end_time == "00:00:10.000"
        self.tsub.end = 500
        assert self.tsub.end_time == "00:00:20.000"
        self.tsub.end = 5.0
        assert self.tsub.end_time == "00:00:05.000"

    def test_end__set_value_error(self):
        def function(x): self.tsub.end = x
        self.assert_raises(ValueError, function, None)

    def test_end_frame__get(self):
        assert self.tsub.end_frame == 75
        assert self.fsub.end_frame == 300

    def test_end_frame__set(self):
        self.fsub.end_frame = 300
        assert self.fsub.end_frame == 300

    def test_end_seconds__get(self):
        assert self.tsub.end_seconds == 3.0
        assert self.fsub.end_seconds == 12.0

    def test_end_seconds__set(self):
        self.tsub.end_seconds = 4.0
        assert self.tsub.end_seconds == 4.0

    def test_end_time__get(self):
        assert self.tsub.end_time == "00:00:03.000"
        assert self.fsub.end_time == "00:00:12.000"

    def test_end_time__set(self):
        self.tsub.end_time = "00:00:04.000"
        assert self.tsub.end_time == "00:00:04.000"

    def test_framerate__get(self):
        assert self.tsub.framerate == aeidon.framerates.FPS_25_000
        assert self.fsub.framerate == aeidon.framerates.FPS_25_000

    def test_framerate__set(self):
        FPS_29_970 = aeidon.framerates.FPS_29_970
        self.tsub.framerate = FPS_29_970
        assert self.tsub.framerate == FPS_29_970

    def test_get_duration(self):
        TIME = aeidon.modes.TIME
        FRAME = aeidon.modes.FRAME
        assert self.tsub.get_duration(TIME) == "00:00:02.000"
        assert self.tsub.get_duration(FRAME) == 50
        assert self.fsub.get_duration(TIME) == "00:00:08.000"
        assert self.fsub.get_duration(FRAME) == 200

    def test_get_end(self):
        TIME = aeidon.modes.TIME
        FRAME = aeidon.modes.FRAME
        assert self.tsub.get_end(TIME) == "00:00:03.000"
        assert self.tsub.get_end(FRAME) == 75
        assert self.fsub.get_end(TIME) == "00:00:12.000"
        assert self.fsub.get_end(FRAME) == 300

    def test_get_start(self):
        TIME = aeidon.modes.TIME
        FRAME = aeidon.modes.FRAME
        assert self.tsub.get_start(TIME) == "00:00:01.000"
        assert self.tsub.get_start(FRAME) == 25
        assert self.fsub.get_start(TIME) == "00:00:04.000"
        assert self.fsub.get_start(FRAME) == 100

    def test_get_text(self):
        MAIN = aeidon.documents.MAIN
        TRAN = aeidon.documents.TRAN
        assert self.tsub.get_text(MAIN) == "main"
        assert self.tsub.get_text(TRAN) == "translation"

    def test_has_container(self):
        assert not self.tsub.has_container("subrip")
        self.tsub.subrip.x1 = 100
        assert self.tsub.has_container("subrip")

    def test_main_text__get(self):
        assert self.tsub.main_text == "main"
        assert self.fsub.main_text == "main"

    def test_main_text__set(self):
        self.tsub.main_text = "test"
        assert self.tsub.main_text == "test"

    def test_mode__get(self):
        assert self.tsub.mode == aeidon.modes.TIME
        assert self.fsub.mode == aeidon.modes.FRAME

    def test_mode__set_frame(self):
        self.fsub.mode = aeidon.modes.FRAME
        self.fsub.mode = aeidon.modes.TIME
        assert self.fsub._start == "00:00:04.000"
        assert self.fsub._end == "00:00:12.000"

    def test_mode__set_time(self):
        self.tsub.mode = aeidon.modes.TIME
        self.tsub.mode = aeidon.modes.FRAME
        assert self.tsub._start == 25
        assert self.tsub._end == 75

    def test_scale_positions__frame(self):
        self.fsub.scale_positions(2.0)
        assert self.fsub.start == 200
        assert self.fsub.end == 600

    def test_scale_positions__time(self):
        self.tsub.scale_positions(2.0)
        assert self.tsub.start == "00:00:02.000"
        assert self.tsub.end == "00:00:06.000"

    def test_set_text(self):
        MAIN = aeidon.documents.MAIN
        TRAN = aeidon.documents.TRAN
        self.tsub.set_text(MAIN, "")
        assert self.tsub.main_text == ""
        self.tsub.set_text(TRAN, "")
        assert self.tsub.tran_text == ""

    def test_shift_positions__frame(self):
        self.fsub.shift_positions(-10)
        assert self.fsub._start == 90
        assert self.fsub._end == 290

    def test_shift_positions__seconds(self):
        self.tsub.shift_positions(1.0)
        assert self.tsub._start == "00:00:02.000"
        assert self.tsub._end == "00:00:04.000"

    def test_shift_positions__time(self):
        self.tsub.shift_positions("00:00:01.000")
        assert self.tsub._start == "00:00:02.000"
        assert self.tsub._end == "00:00:04.000"

    def test_start__get(self):
        assert self.tsub.start == "00:00:01.000"
        assert self.fsub.start == 100

    def test_start__set_frame(self):
        self.fsub.start = 500
        assert self.fsub.start_frame == 500
        self.fsub.start = "00:00:10.000"
        assert self.fsub.start_frame == 250
        self.fsub.start = 5.0
        assert self.fsub.start_frame == 125

    def test_start__set_time(self):
        self.tsub.start = "00:00:10.000"
        assert self.tsub.start_time == "00:00:10.000"
        self.tsub.start = 500
        assert self.tsub.start_time == "00:00:20.000"
        self.tsub.start = 5.0
        assert self.tsub.start_time == "00:00:05.000"

    def test_start_frame__get(self):
        assert self.tsub.start_frame == 25
        assert self.fsub.start_frame == 100

    def test_start_frame__set(self):
        self.fsub.start_frame = 25
        assert self.fsub.start_frame == 25

    def test_start_seconds__get(self):
        assert self.tsub.start_seconds == 1.0
        assert self.fsub.start_seconds == 4.0

    def test_start_seconds__set(self):
        self.tsub.start_seconds = 0.1
        assert self.tsub.start_seconds == 0.1

    def test_start_time__get(self):
        assert self.tsub.start_time == "00:00:01.000"
        assert self.fsub.start_time == "00:00:04.000"

    def test_start_time__set(self):
        self.tsub.start_time = "00:00:00.100"
        assert self.tsub.start_time == "00:00:00.100"

    def test_tran_text__get(self):
        assert self.tsub.tran_text == "translation"
        assert self.fsub.tran_text == "translation"

    def test_tran_text_set(self):
        self.tsub.tran_text = "test"
        assert self.tsub.tran_text == "test"
