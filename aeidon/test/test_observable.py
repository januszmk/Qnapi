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


class PuppetObservable(aeidon.Observable):

    signals = ("do",)

    def __init__(self):
        aeidon.Observable.__init__(self)
        self.x = 0


class TestObservable(aeidon.TestCase):

    def on_notify_x(self, obj, value):
        assert obj is self.obs
        assert value == self.obs.x
        self.notify_count += 1

    def on_do(self, obj):
        assert obj is self.obs
        self.do_count += 1

    def setup_method(self, method):
        self.obs = PuppetObservable()
        self.do_count = 0
        self.notify_count = 0
        self.obs.connect("do", self.on_do)
        self.obs.connect("notify::x", self.on_notify_x)

    def test_block(self):
        assert self.obs.block("do")
        assert not self.obs.block("do")
        self.obs.emit("do")
        assert self.do_count == 0

    def test_block_all(self):
        assert self.obs.block_all()
        assert not self.obs.block_all()
        self.obs.emit("do")
        assert self.do_count == 0
        self.obs.notify("x")
        assert self.notify_count == 0

    def test_connect(self):
        self.obs.connect("do", lambda *args: None)
        self.obs.connect("notify::x", lambda *args: None)

    def test_disconnect(self):
        self.obs.disconnect("do", self.on_do)
        self.obs.emit("do")
        assert self.do_count == 0

    def test_emit(self):
        self.obs.x = 1
        assert self.notify_count == 1
        self.obs.emit("do")
        assert self.do_count == 1

    def test_freeze_notify(self):
        assert self.obs.freeze_notify()
        assert not self.obs.freeze_notify()
        self.obs.x = 1
        assert self.notify_count == 0

    def test_notify(self):
        self.obs.notify("x")
        assert self.notify_count == 1

    def test_thaw_notify(self):
        self.obs.freeze_notify()
        self.obs.x = 1
        self.obs.x = 2
        assert self.obs.thaw_notify()
        assert not self.obs.thaw_notify()
        assert self.notify_count == 1

    def test_unblock(self):
        self.obs.block("do")
        assert self.obs.unblock("do")
        assert not self.obs.unblock("do")
        self.obs.emit("do")
        assert self.do_count == 1

    def test_unblock_all(self):
        self.obs.block_all()
        assert self.obs.unblock_all()
        assert not self.obs.unblock_all()
        self.obs.emit("do")
        assert self.do_count == 1
        self.obs.notify("x")
        assert self.notify_count == 1
