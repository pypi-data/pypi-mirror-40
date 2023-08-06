#!/usr/bin/env python
"""
Module containing the tools for creating injection files
"""
from __future__ import division, print_function

import os

import numpy as np
import bilby

from . import utils
from .utils import logger, BilbyPipeError


class Input(object):
    """ Superclass of input handlers """

    @property
    def idx(self):
        """ The level A job index """
        return self._idx

    @idx.setter
    def idx(self, idx):
        self._idx = idx

    @property
    def known_detectors(self):
        try:
            return self._known_detectors
        except AttributeError:
            return ['H1', 'L1', 'V1']

    @known_detectors.setter
    def known_detectors(self, known_detectors):
        self._known_detectors = self._convert_detectors_input(known_detectors)

    @property
    def detectors(self):
        """ A list of the detectors to include, e.g., ['H1', 'L1'] """
        return self._detectors

    @detectors.setter
    def detectors(self, detectors):
        self._detectors = self._convert_detectors_input(detectors)
        self._check_detectors_against_known_detectors()

    def _convert_detectors_input(self, detectors):
        if isinstance(detectors, str):
            det_list = self._split_string_by_space(detectors)
        elif isinstance(detectors, list):
            if len(detectors) == 1:
                det_list = self._split_string_by_space(detectors[0])
            else:
                det_list = detectors
        else:
            raise BilbyPipeError(
                'Input `detectors` = {} not understood'.format(detectors))

        det_list.sort()
        det_list = [det.upper() for det in det_list]
        return det_list

    def _check_detectors_against_known_detectors(self):
        for element in self.detectors:
            if element not in self.known_detectors:
                raise BilbyPipeError(
                    'detectors contains "{}" not in the known '
                    'detectors list: {} '.format(
                        element, self.known_detectors))

    @staticmethod
    def _split_string_by_space(string):
        """ Converts "H1 L1" to ["H1", "L1"] """
        return string.split(' ')

    @staticmethod
    def _convert_string_to_list(string):
        """ Converts various strings to a list """
        string = string.replace(',', ' ')
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('"', '')
        string = string.replace("'", '')
        string_list = string.split()
        return string_list

    @property
    def outdir(self):
        """ The path to the directory where output will be stored """
        return self._outdir

    @outdir.setter
    def outdir(self, outdir):
        self._outdir = os.path.abspath(outdir)
        for dr in [outdir, self.submit_directory,
                   self.data_generation_log_directory,
                   self.data_analysis_log_directory, self.data_directory,
                   self.summary_log_directory, self.result_directory]:
            utils.check_directory_exists_and_if_not_mkdir(dr)

    @property
    def submit_directory(self):
        """ The path to the directory where submit output will be stored """
        return os.path.join(self._outdir, 'submit')

    @property
    def data_generation_log_directory(self):
        """ The path to the directory where log output will be stored """
        return os.path.join(self._outdir, 'log_data_generation')

    @property
    def data_analysis_log_directory(self):
        """ The path to the directory where log output will be stored """
        return os.path.join(self._outdir, 'log_data_analysis')

    @property
    def summary_log_directory(self):
        """ The path to the directory where log output will be stored """
        return os.path.join(self._outdir, 'log_results_page')

    @property
    def data_directory(self):
        """ The path to the directory where data output will be stored """
        return os.path.join(self._outdir, 'data')

    @property
    def result_directory(self):
        """ The path to the directory where result output will be stored """
        return os.path.join(self._outdir, 'result')

    @property
    def webdir(self):
        return self._webdir

    @webdir.setter
    def webdir(self, webdir):
        if webdir is None:
            self._webdir = os.path.join(self.outdir, 'results_page')
        else:
            self._webdir = webdir

    @property
    def gps_file(self):
        """ The gps file containing the list of gps times """
        return self._gps_file

    @gps_file.setter
    def gps_file(self, gps_file):
        """ Set the gps_file

        At setting, will check the file exists, read  the contents, identify
        which element to generate data for, and set the cache file
        """
        if gps_file is None:
            self._gps_file = None
            return
        elif os.path.isfile(gps_file):
            self._gps_file = os.path.abspath(gps_file)
        else:
            raise FileNotFoundError(
                "Input file gps_file={} not understood".format(gps_file))

        try:
            self._parse_gps_file()
        except AttributeError:
            logger.debug("No _parse_gps_file method present")

    def read_gps_file(self):
        gpstimes = np.loadtxt(self.gps_file, ndmin=1)
        return gpstimes

    @property
    def bilby_frequency_domain_source_model(self):
        """ The bilby function to pass to the waveform_generator """
        if self.frequency_domain_source_model in bilby.gw.source.__dict__.keys():
            return bilby.gw.source.__dict__[self._frequency_domain_source_model]
        else:
            raise BilbyPipeError(
                "No source model {} found.".format(
                    self._frequency_domain_source_model))

    @property
    def frequency_domain_source_model(self):
        """ String of which frequency domain source model to use """
        return self._frequency_domain_source_model

    @frequency_domain_source_model.setter
    def frequency_domain_source_model(self, frequency_domain_source_model):
        self._frequency_domain_source_model = frequency_domain_source_model
