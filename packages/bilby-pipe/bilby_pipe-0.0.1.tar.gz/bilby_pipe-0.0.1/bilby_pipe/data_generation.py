#!/usr/bin/env python
"""
Module containing the tools for data generation
"""
from __future__ import division, print_function

import sys
import os

import bilby
import deepdish

from bilby_pipe.utils import logger
from bilby_pipe.main import Input, DataDump, parse_args
from bilby_pipe.bilbyargparser import BilbyArgParser


def create_parser():
    """ Generate a parser for the data_generation.py script

    Additional options can be added to the returned parser beforing calling
    `parser.parse_args` to generate the arguments`

    Returns
    -------
    parser: BilbyArgParser
        A parser with all the default options already added

    """
    parser = BilbyArgParser(ignore_unknown_config_file_keys=True)
    parser.add('--ini', is_config_file=True, help='The ini-style config file')
    parser.add('--idx', type=int, help="The level A job index", default=0)
    parser.add('--cluster', type=int,
               help='The condor cluster ID', default=None)
    parser.add('--process', type=int,
               help='The condor process ID', default=None)
    parser.add('--outdir', default='.', help='Output directory')
    parser.add('--label', default='label', help='Output label')

    det_parser = parser.add_argument_group(title='Detector arguments')
    det_parser.add(
        '--detectors', action='append',
        help=('The names of detectors to include. If given in the ini file, '
              'multiple detectors are specified by `detectors=[H1, L1]`. If '
              'given at the command line, as `--detectors H1 --detectors L1`'))
    det_parser.add('--calibration', type=int, default=2,
                   help='Which calibration to use')
    det_parser.add('--duration', type=int, default=4,
                   help='The duration of data around the event to use')
    det_parser.add("--trigger-time", default=None, type=float,
                   help="The trigger time")
    det_parser.add("--sampling-frequency", default=4096, type=int)
    det_parser.add("--channel-names", default=None, nargs="*",
                   help="Channel names to use, if not provided known "
                   "channel names will be tested.")
    det_parser.add('--psd-duration', default=500, type=int,
                   help='Time used to generate the PSD, default is 500.')
    det_parser.add('--minimum-frequency', default=20, type=float)

    # Method specific options below here
    data_parser = parser.add_argument_group(title='Data setting methods')
    data_parser.add('--gracedb', type=str, help='Gracedb UID', default=None)
    data_parser.add('--gps-file', type=str, help='File containing GPS times')
    data_parser.add('--injection-file', type=str, default=None,
                    help='Path to an injection file')
    data_parser.add('--waveform-approximant', default='IMRPhenomPv2', type=str,
                    help="Name of the waveform approximant for injection")
    data_parser.add('--reference-frequency', default=20, type=float,
                    help="The reference frequency")
    return parser


class DataGenerationInput(Input):
    """ Handles user-input and creation of intermediate ifo list

    Parameters
    ----------
    parser: configargparse.ArgParser, optional
        The parser containing the command line / ini file inputs
    args_list: list, optional
        A list of the arguments to parse. Defauts to `sys.argv[1:]`

    """
    def __init__(self, args, unknown_args):

        logger.info('Command line arguments: {}'.format(args))
        logger.info('Unknown command line arguments: {}'.format(unknown_args))
        self.meta_data = dict(command_line_args=args,
                              unknown_command_line_args=unknown_args,
                              injection_parameters=None)
        self.ini = args.ini
        self.cluster = args.cluster
        self.process = args.process
        self.idx = args.idx
        self.detectors = args.detectors
        self.calibration = args.calibration
        self.channel_names = args.channel_names
        self.duration = args.duration
        self.trigger_time = args.trigger_time
        self.sampling_frequency = args.sampling_frequency
        self.psd_duration = args.psd_duration
        self.minimum_frequency = args.minimum_frequency
        self.outdir = args.outdir
        self.label = args.label

        self.gracedb = args.gracedb
        self.gps_file = args.gps_file

        self.waveform_approximant = args.waveform_approximant
        self.reference_frequency = args.reference_frequency
        self.injection_file = args.injection_file

    @property
    def minimum_frequency(self):
        return self._minimum_frequency

    @minimum_frequency.setter
    def minimum_frequency(self, minimum_frequency):
        self._minimum_frequency = float(minimum_frequency)

    @property
    def detectors(self):
        """ A list of the detectors to search over, e.g., ['H1', 'L1'] """
        return self._detectors

    @detectors.setter
    def detectors(self, detectors):
        """ Handles various types of user input """
        if isinstance(detectors, list):
            if len(detectors) == 1:
                det_list = self._convert_string_to_list(detectors[0])
            else:
                det_list = detectors
        else:
            raise ValueError('Input `detectors` = {} not understood'
                             .format(detectors))

        det_list.sort()
        det_list = [det.upper() for det in det_list]
        self._detectors = det_list

    @property
    def gracedb(self):
        """ The gracedb of the candidate """
        return self._gracedb

    @gracedb.setter
    def gracedb(self, gracedb):
        """ Set the gracedb ID

        At setting, will load the json candidate data and path to the frame
        cache file.
        """
        if gracedb is None:
            self._gracedb = None
        else:
            logger.info("Setting gracedb id to {}".format(gracedb))
            candidate, frame_caches = bilby.gw.utils.get_gracedb(
                gracedb, self.data_directory, self.duration, self.calibration,
                self.detectors)
            self.meta_data['gracedb_candidate'] = candidate
            self._gracedb = gracedb
            self.trigger_time = candidate['gpstime']
            self.frame_caches = frame_caches

    def _parse_gps_file(self):
        gps_start_times = self.read_gps_file()
        gps_start_time = gps_start_times[self.idx]
        self.trigger_time = gps_start_time + self.duration / 2.0
        self.frame_caches = self.generate_frame_cache_list_from_gpstime(gps_start_time)

    def generate_frame_cache_list_from_gpstime(self, gps_start_time):
        cache_files = []
        for det in self.detectors:
            cache_files.append(bilby.gw.utils.gw_data_find(
                det, gps_start_time=gps_start_time, duration=self.duration,
                calibration=self.calibration, outdir=self.data_directory))
        return cache_files

    @property
    def frame_caches(self):
        """ A list of paths to the frame-cache files """
        try:
            return self._frame_caches
        except AttributeError:
            raise ValueError("frame_caches list is unset")

    @frame_caches.setter
    def frame_caches(self, frame_caches):
        """ Set the frame_caches, if successfull generate the interferometer list """
        if isinstance(frame_caches, list):
            self._frame_caches = frame_caches
            self._set_interferometers_from_frame_caches(frame_caches)
        elif frame_caches is None:
            self._frame_caches = None
        else:
            raise ValueError("frame_caches list must be a list")

    def _set_interferometers_from_frame_caches(self, frame_caches):
        """ Helper method to set the interferometers from a list of frame_caches

        If no channel names are supplied, an attempt is made by bilby to
        infer the correct channel name.

        Parameters
        ----------
        frame_caches: list
            A list of strings pointing to the frame cache file
        """
        interferometers = bilby.gw.detector.InterferometerList([])
        if self.channel_names is None:
            self.channel_names = [None] * len(frame_caches)
        for cache_file, channel_name in zip(frame_caches, self.channel_names):
            interferometer = bilby.gw.detector.load_data_from_cache_file(
                cache_file, self.trigger_time, self.duration,
                self.psd_duration, channel_name)
            interferometer.minimum_frequency = self.minimum_frequency
            interferometers.append(interferometer)
        self.interferometers = interferometers

    @property
    def parameter_conversion(self):
        return bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters

    @property
    def injection_file(self):
        return self._injection_file

    @injection_file.setter
    def injection_file(self, injection_file):
        self._injection_file = injection_file
        if injection_file is None:
            logger.debug("No injection file set")
        elif os.path.isfile(injection_file):
            injection_dict = deepdish.io.load(injection_file)
            injection_df = injection_dict['injections']
            self.injection_parameters = injection_df.iloc[self.process - 1].to_dict()
            self.meta_data['injection_parameters'] = self.injection_parameters
            if self.trigger_time is None:
                self.trigger_time = self.injection_parameters['geocent_time']
            self._set_interferometers_from_simulation()
        else:
            raise FileNotFoundError("Injection file {} not found".format(injection_file))

    def _set_interferometers_from_simulation(self):
        waveform_arguments = dict(waveform_approximant=self.waveform_approximant,
                                  reference_frequency=self.reference_frequency,
                                  minimum_frequency=self.minimum_frequency)

        waveform_generator = bilby.gw.WaveformGenerator(
            duration=self.duration, sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
            parameter_conversion=self.parameter_conversion,
            waveform_arguments=waveform_arguments)

        ifos = bilby.gw.detector.InterferometerList(self.detectors)
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency, duration=self.duration,
            start_time=self.trigger_time - self.duration / 2)
        try:
            ifos.inject_signal(waveform_generator=waveform_generator,
                               parameters=self.injection_parameters)
        except AttributeError:
            pass

        self.interferometers = ifos

    @property
    def interferometers(self):
        """ A bilby.gw.detector.InterferometerList """
        try:
            return self._interferometers
        except AttributeError:
            raise ValueError("interferometers unset, did you provide a set-data method?")

    @interferometers.setter
    def interferometers(self, interferometers):
        self._interferometers = interferometers

    def save_interferometer_list(self):
        data_dump = DataDump(outdir=self.data_directory, label=self.label,
                             idx=self.idx,
                             trigger_time=self.trigger_time,
                             interferometers=self.interferometers,
                             meta_data=self.meta_data)
        data_dump.to_hdf5()


def main():
    args, unknown_args = parse_args(sys.argv[1:], create_parser())
    data = DataGenerationInput(args, unknown_args)
    data.save_interferometer_list()
