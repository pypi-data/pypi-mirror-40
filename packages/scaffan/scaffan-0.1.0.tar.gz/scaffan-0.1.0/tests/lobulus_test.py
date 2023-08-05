#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
import unittest
import io3d
# import openslide
import scaffan
import scaffan.algorithm


class MainGuiTest(unittest.TestCase):

    def test_read_annotations(self):
        # fn = io3d.datasets.join_path("medical", "orig", "CMU-1.ndpi", get_root=True)
        # fn = io3d.datasets.join_path("medical", "orig", "CMU-1.ndpi", get_root=True)
        fn = io3d.datasets.join_path("scaffold", "Hamamatsu", "PIG-003_J-18-0165_HE.ndpi", get_root=True)
        # imsl = openslide.OpenSlide(fn)
        # annotations = scan.read_annotations(fn)
        # scan.annotations_to_px(imsl, annotations)
        mainapp = scaffan.algorithm.Scaffan()
        mainapp.set_input_file(fn)
        mainapp.init_run()
        mainapp.set_annotation_color_selection("#FF00FF")
        # mainapp.parameters.param("Processing", "Show").setValue(True)
        mainapp.run_lobuluses()
        # mainapp.start_gui()



