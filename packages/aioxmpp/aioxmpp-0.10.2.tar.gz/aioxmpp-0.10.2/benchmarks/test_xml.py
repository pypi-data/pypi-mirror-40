########################################################################
# File name: test_xml.py
# This file is part of: aioxmpp
#
# LICENSE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
########################################################################
import base64
import io
import itertools
import unittest
import random

import aioxmpp.xso as xso
import aioxmpp.xml

from aioxmpp.benchtest import times, timed, record


class ShallowRoot(xso.XSO):
    TAG = ("uri:test", "shallow")

    attr = xso.Attr("a")
    data = xso.Text()

    def __init__(self, scale=1):
        super().__init__()
        self.attr = "foobar"*(2*scale)
        self.data = "fnord"*(10*scale)


class DeepLeaf(xso.XSO):
    TAG = ("uri:test", "leaf")

    data = xso.Text()

    def generate(self, rng, depth):
        self.data = "foo" * (2*rng.randint(1, 10))


class DeepNode(xso.XSO):
    TAG = ("uri:test", "node")

    data = xso.Attr("attr")
    children = xso.ChildList([DeepLeaf])

    def generate(self, rng, depth):
        self.data = "foo" * (2*rng.randint(1, 10))
        if depth >= 5:
            cls = DeepLeaf
        else:
            cls = DeepNode

        self.children.append(cls())
        for i in range(rng.randint(2, 10)):
            if rng.randint(1, 10) == 1:
                item = DeepNode()
            else:
                item = DeepLeaf()
            self.children.append(item)

        for item in self.children:
            item.generate(rng, depth+1)


DeepNode.register_child(DeepNode.children, DeepNode)


class DeepRoot(xso.XSO):
    TAG = ("uri:test", "root")

    children = xso.ChildList([DeepLeaf, DeepNode])

    def generate(self, rng):
        self.children[:] = [DeepNode() for i in range(3)]
        for child in self.children:
            child.generate(rng, 1)


class TestxmlValidateNameValue_str(unittest.TestCase):
    KEY = "aioxmpp.xml", "xmlValidateNameValue"

    def test_exhaustive(self):
        validate = aioxmpp.xml.xmlValidateNameValue_str

        r1 = range(0, 0xd800)
        r2 = range(0xe000, 0xf0000)

        range_iter = itertools.chain(
            # exclude surrogates
            r1, r2,
        )

        with timed() as timer:
            for cp in range_iter:
                validate(chr(cp))

        record(self.KEY + ("exhaustive",),
               timer.elapsed / (len(r1) + len(r2)),
               "s")

    def test_exhaustive_dualchar(self):
        validate = aioxmpp.xml.xmlValidateNameValue_str

        strs = ["x" + chr(cp) for cp in range(0, 0xd800)]

        with timed() as timer:
            for s in strs:
                validate(s)

        record(self.KEY + ("exhaustive_dualchar",),
               timer.elapsed / (len(strs)),
               "s")

    def test_random_strings(self):
        key = self.KEY + ("random",)

        validate = aioxmpp.xml.xmlValidateNameValue_str

        rng = random.Random(1)
        samples = []
        for i in range(1000):
            samples.append(base64.b64encode(
                random.getrandbits(120).to_bytes(120//8, 'little')
            ).decode("ascii").rstrip("="))

        for sample in samples:
            with timed() as timer:
                validate(sample)
            record(key, timer.elapsed, "s")


class Testwrite_single_xso(unittest.TestCase):
    KEY = "aioxmpp.xml", "write_single_xso"

    @classmethod
    def setUpClass(cls):
        rng = random.Random(1)
        cls.deep_samples = [
            DeepRoot()
            for i in range(10)
        ]
        for sample in cls.deep_samples:
            with timed(cls.KEY+("deep", "generate")):
                sample.generate(rng)

    def setUp(self):
        self.buf = io.BytesIO(bytearray(1024*1024))

    def _reset_buffer(self):
        self.buf.seek(0)

    @times(1000)
    def test_shallow_and_small(self):
        key = self.KEY + ("shallow+small",)
        item = ShallowRoot()
        self._reset_buffer()
        with timed() as t:
            aioxmpp.xml.write_single_xso(item, self.buf)
        record(key+("sz",), self.buf.tell(), "B")
        record(key+("rate",), self.buf.tell() / t.elapsed, "B/s")

    @times(1000)
    def test_shallow_and_large(self):
        key = self.KEY + ("shallow+large",)
        item = ShallowRoot(scale=100)
        self._reset_buffer()
        with timed() as t:
            aioxmpp.xml.write_single_xso(item, self.buf)
        record(key+("sz",), self.buf.tell(), "B")
        record(key+("rate",), self.buf.tell() / t.elapsed, "B/s")

    @times(1000, pass_iteration=True)
    def test_deep(self, iteration=None):
        key = self.KEY + ("deep",)
        item = self.deep_samples[iteration % len(self.deep_samples)]
        self._reset_buffer()
        with timed() as t:
            aioxmpp.xml.write_single_xso(item, self.buf)
        record(key+("sz",), self.buf.tell(), "B")
        record(key+("rate",), self.buf.tell() / t.elapsed, "B/s")
