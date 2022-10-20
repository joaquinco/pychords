import librosa
import vamp
from typing import List, NamedTuple
from enum import Enum
import os
import sys
from pkg_resources import resource_filename
import logging


logger = logging.getLogger('pychord')


if not os.getenv('VAMP_PATH'):
    logger.warning('Please make sure VAMP_PATH is specified pointing to the directory containing the '
                   'appropriate compiled library for Chordino. '
                   'This can be sourced by using the Vamp Plugin Pack installer at '
                   'https://code.soundsoftware.ac.uk/projects/vamp-plugin-pack')


class TuningMode(Enum):
    """Options for Tuning Mode parameter (see Chordino doc)"""
    GLOBAL = 0
    LOCAL = 1


class ChromaNormalization(Enum):
    """Options for Chroma Normalization parameter (see Chordino doc)"""
    NONE = 0
    MAX = 1
    L1 = 2
    L2 = 3


class ChordEntry(NamedTuple):
    chord: str
    timestamp: float


class Chordino:
    """
    Class for extracting chords using Chordino (http://www.isophonics.net/nnls-chroma). All parameters are those
    passed to Chordino. You can see further details of what they mean in the
    Chordino -> Parameters section in the above link. The defaults here are the suggested parameter settings for
    when extracting from a generic pop song. See the link for more recommended settings.

    :param use_nnls: Use approximate transcription (NNLS)
    :param roll_on: Spectral roll-on (range: 0 - 5)
    :param local_tunning: Tuning mode (Local or Global)
    :param spectral_whitening: Spectral whitening (range: 0 - 1)
    :param spectral_shape: Spectral shape (range: 0.5 - 0.9)
    :param boost_n_likelihood: Boost likelihood of the N (no chord) label
    :param kwargs: Any other parameters that may become available to the chordino vamp plugin. Param keys are the
     vamp identifier.
    """

    def __init__(self,
                 use_nnls: bool = True,
                 use_hart_notation: bool = False,
                 roll_on: float = 1,
                 local_tunning: bool = False,
                 spectral_whitening: float = 1,
                 spectral_shape=0.7,
                 boost_n_likelihood: float = 0.1,
                 **kwargs):
        self._params = {
            'useNNLS': int(use_nnls),
            'usehartesyntax': int(use_hart_notation),
            'rollon': roll_on,
            'tuningmode': int(local_tunning),
            'whitening': spectral_whitening,
            's': spectral_shape,
            'boostn': boost_n_likelihood
        }
        self._params.update(kwargs)

    def extract(self, file: str, **kwargs) -> List[dict]:
        """
        Extract chord changes from a particular file. The file is loaded into librosa, therefore takes sound files
        supported by librosa (which uses audioread and soundfile). This includes .wav, .mp3, .ogg and others.

        :param file: Absolute file path to the relevant file. A file like object is also acceptable.
        :param kwargs: Keyword arguments for librosa.load
         (see https://librosa.org/doc/0.7.0/generated/librosa.core.load.html)
        :return: List of chord changes for the sound file
        """
        data, rate = librosa.load(file, **kwargs)

        logger.info(
            'Submitting {} to Chordino for chord extraction.'.format(file))

        result = vamp.collect(
            data, rate, 'nnls-chroma:chordino', parameters=self._params)
        logger.info('Chord extraction for {} complete.'.format(file))

        return [
            ChordEntry(chord=entry['label'], timestamp=entry['timestamp'])
            for entry in result['list']
        ]
