#!/usr/bin/env python

# Copyright (C) 2019 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sif
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="SIF Python")

    # Global Variables
    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet', dest="quiet", 
                        help="show SIF Python verison and exit", 
                        default=False, action='store_true')

    parser.add_argument('--version', dest="version", 
                        help="suppress additional output.", 
                        default=False, action='store_true')

    description = 'actions for SIF Python'
    subparsers = parser.add_subparsers(help='sif python actions',
                                       title='actions',
                                       description=description,
                                       dest="command")


    # Local shell with client loaded
    shell = subparsers.add_parser("shell",
                                  help="shell into a session a client.")

    shell.add_argument("image", nargs=1,
                       help="the image to load into the client", 
                       type=str, default=None)

    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    '''main is the entrypoint to the sregistry client. The flow works to first
    to determine the subparser in use based on the command. The command then
    imports the correct main (files imported in this folder) associated with
    the action of choice. When the client is imported, it is actually importing
    a return of the function get_client() under sregistry/main, which plays
    the job of "sniffing" the environment to determine what flavor of client
    the user wants to activate. Installed within a singularity image, this
    start up style maps well to Standard Container Integration Format (SCIF)
    apps, where each client is a different entrypoint activated based on the
    environment variables.
    '''

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''

        version = sif.__version__

        print("\nSIF Python v%s" % version)
        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "DEBUG"

    # Show the version and exit
    if args.version is True:
        print(sif.__version__)
        sys.exit(0)

    from sif.logger import bot

    # Does the user want a shell?
    if args.command == "shell": from .shell import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)

if __name__ == '__main__':
    main()
