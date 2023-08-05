# -*- coding: utf-8 -*-

from test.picardtestcase import PicardTestCase

from picard.ui.searchdialog import to_seconds


class ToSecondsTestCase(PicardTestCase):
    def test_1(self):
        self.assertEqual(to_seconds("02:02:35"), 155)
