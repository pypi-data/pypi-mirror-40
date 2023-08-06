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

from sif.logger import bot
import sys
import os

def main(args):

    lookup = { 'ipython': ipython,
               'python': python,
               'bpython': bpython }

    shells = ['ipython', 'python', 'bpython']

    # The user must supply an image
    if args.image is None:
        bot.exit('You must provide an image to load a SIFHeader client.')

    image = args.image[0]

    # The image must exist
    if not os.path.exists(image):
        bot.exit('Cannot find %s' % image)

    # Present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](image)
        except ImportError:
            pass
    

def ipython(image):
    '''give the user an ipython shell, optionally load image
    '''
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    from IPython import embed
    embed()


def bpython(image):
    import bpython
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    bpython.embed(locals_={'header': header,
                           'image': image,
                           'SIFHeader': SIFHeader})

def python(image):
    import code
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    code.interact(local={"header": header,
                         'image': image,
                         'SIFHeader': SIFHeader})
