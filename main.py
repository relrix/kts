#!/usr/bin/python

import os
import sys
import json
import warnings
import argparse

from modules import Kts
from modules.recognize import MicrophoneRecognizer
from argparse import RawTextHelpFormatter

from modules.album_art import draw_404, draw_album_art

warnings.filterwarnings("ignore")

DEFAULT_CONFIG_FILE = "kts.config"


def init(configpath):
    """ 
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print("Cannot open configuration: %s. Exiting" % (str(err)))
        sys.exit(1)

    # create a kts instance
    return Kts(config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="KTS: Audio Fingerprinting library",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--config', nargs='?',
                        help='Path to configuration file\n'
                             'Usages: \n'
                             '--config /path/to/config-file\n')
    parser.add_argument('-f', '--fingerprint', nargs='*',
                        help='Fingerprint files in a directory\n'
                             'Usages: \n'
                             '--fingerprint /path/to/directory extension\n'
                             '--fingerprint /path/to/directory')
    parser.add_argument('-r', '--recognize', nargs=2,
                        help='Recognize what is '
                             'playing through the microphone\n'
                             'Usage: \n'
                             '--recognize mic number_of_seconds \n')
    args = parser.parse_args()

    if not args.fingerprint and not args.recognize:
        parser.print_help()
        sys.exit(0)

    config_file = args.config
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE

    kts_obj = init(config_file)
    if args.fingerprint:
        # Fingerprint all files in a directory
        if len(args.fingerprint) == 2:
            directory = args.fingerprint[0]
            extension = args.fingerprint[1]
            print("Fingerprinting all .%s files in the %s directory"
                  % (extension, directory))
            kts_obj.fingerprint_directory(directory, ["." + extension], 4)

        elif len(args.fingerprint) == 1:
            filepath = args.fingerprint[0]
            if os.path.isdir(filepath):
                print("Please specify an extension if you'd like to fingerprint a directory!")
                sys.exit(1)
                kts_obj.fingerprint_file(filepath)

    elif args.recognize:
        # Recognize audio source
        song = None
        source = args.recognize[0]
        opt_arg = args.recognize[1]

        if source in ('mic', 'microphone'):
            print "Listening...."
            song = kts_obj.recognize(MicrophoneRecognizer, seconds=int (opt_arg))
        print(song)
        try:
            if(int(song['confidence']) > 30 ):
                draw_album_art(song['song_name'], song['confidence'])
            else:
                draw_404(song['confidence'])
        except:
            draw_404("0")

    sys.exit(0)
