
# Copyright (C) 2018-2019 Vanessa Sochat.

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

import os
import uuid
from sif.logger import bot
from sif.defaults import SIF_VERSION
from struct import ( unpack, calcsize )

class SIFHeader:

    def __init__(self, image, load_header=True, version=None):

        # Load the base for a particular SIF version
        self.load_base(version)

        # We will store global headers, and descriptors
        self.meta = dict()
        self.desc = dict()

        if not os.path.exists(image):
            bot.exit('Cannot find %s.' % image)

        if not self.is_sif(image):
            bot.exit('%s is not a SIF file.' % image)

        bot.info('%s is a SIF file.' % image)
        self.image = image

        # The user might want to wait to load
        if load_header is True:
            self.load_header()


    def __str__(self):
        '''string representation of a SIF image shows the path'''
        return "<SIF:%s>" % self.image

    def __repr__(self):
        '''representation of SIF image is also the path'''
        return self.__str__()


################################################################################
# Printing
################################################################################


    def print_header(self):
        '''print the metadata for the user to see
        '''
        for key, val in self.meta.items():
            bot.info('SIF Header %s %s' % (key, val) )
        bot.newline()

    def print_descriptor(self, descriptor, skip_keys=None):
        '''print the definition file metadata for the user to see

           Parameters
           ==========
           name: the key in self.desc to iterate over
           skip_keys: skip these keys in self.desc[key]
        ''' 
        if skip_keys == None:
            skip_keys = []

        if not isinstance(skip_keys, list):
            skip_keys = [skip_keys]

        if descriptor in self.desc:
            name = descriptor.capitalize()
            for key, val in self.desc[descriptor].items():
                if key not in skip_keys:
                    bot.info('%s %s %s' % (name, key, val) )
        bot.newline()


    def print_descriptor_deffile(self):
        self.print_descriptor('deffile', 'content')

    def print_descriptor_partition(self):
        self.print_descriptor('partition')

    def print_descriptor_signature(self):
        self.print_descriptor('signature')

    def print_deffile(self):
        '''print the definition file for the user to see
        '''
        if 'deffile' in self.desc:
            if 'content' in self.desc['deffile']:
                print(self.desc['deffile']['content'])

    def print_arch(self):
        '''print the human friendly architecture'''
        if 'arch' in self.meta:
            if self.meta['arch'] in self.arches:
                bot.info('Architecture: %s' % self.arches[self.meta['arch']])
            bot.newline()

################################################################################
# Validation
################################################################################


    def is_sif(self, image):
        '''determine if an image is SIF based on finding SIF_MAGIC
        ''' 

        with open(image, 'rb') as filey:

            # Skip the first line
            filey.seek(self.base.HdrLaunchLen)

            # Read # of bytes corresponding to length of sif magic
            fmt = "%ss" % self.base.HdrMagicLen
 
            # Read length of header magic (if fails, not sif)           
            try:
                line = self.unpack_chars(filey, fmt)
            except UnicodeDecodeError:
                pass
                return False

            if line != None:
                if isinstance(line, str) and line.startswith(self.base.HdrMagic):
                    return True

            return False


    def unpack_chars(self, filey, fmt, number=None, encoding='utf-8'):
        '''unpack characters, and handle the encoding and removing
           an end character.
        '''
        line, = self.unpack_bytes(filey, fmt, number)

        # Return numbers, otherwise parse bytes to string
        if isinstance(line, (int, float)):
            return line

        return line.decode(encoding).replace(self.base.EndChar, '')


################################################################################
# Loading
################################################################################

    def load_base(self, version=None):
        '''load a sif base, or default to version 02
        '''
        from sif.header import get_structure
        SIF = get_structure(version)

        # We have a header base, arches
        self.base = SIF.HeaderBase
        self.arches = SIF.arches

        # Descriptors
        self.Deffile = SIF.Deffile 
        self.Partition = SIF.Partition
        self.Signature = SIF.Signature

    def read_and_strip(self, filey, fmt, number=None):
        '''read a number of bytes (number of based on a format) from the
           file, remove empty / white spaces indicated by \0.
        '''
        values = self.read_bytes(filey, fmt, number)
         
        try:
            return values.decode('utf-8').replace('\0', '')
        except:
            return values


    def read_bytes(self, filey, fmt, number=None):
        '''just read a number of bytes from an open file.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        if number == None:
            number = calcsize(fmt)

        return filey.read(number)


    def unpack_bytes(self, filey, fmt, number=None):
        '''read AND unpack a number of bytes from an open file. If a 
           format is provided, convert to utf-8 and return the string. 
           If fmt is None, assume a character string of the same length.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        byte_values = self.read_bytes(filey, fmt, number)
        return unpack(fmt, byte_values)



################################################################################
# Global Header
################################################################################

            
    def load_header(self):
        '''Once we know is sif, load the header.
        ''' 

        # Start at end of interpreter line, and after sif magix
        byte_start = self.base.HdrLaunchLen + self.base.HdrMagicLen

        with open(self.image, 'rb') as filey:

            # Skip the first line
            filey.seek(byte_start)

            # 1. Read the version
            self.meta['version'] = self.unpack_chars(filey, 
                                                     number=self.base.HdrVersionLen, 
                                                     fmt = "%ss" % self.base.HdrVersionLen)

            # 2. Read the architecture
            self.meta['arch'] = self.unpack_chars(filey, 
                                                  number=self.base.HdrArchLen,
                                                  fmt = "<%ss" % self.base.HdrArchLen)

            # 3. Read the uuid - this returns little endian bytes
            uuid_bytes = self.read_bytes(filey, fmt='<16c')

            # Let the uuid library read the binary data for us!
            self.meta['uuid'] = str(uuid.UUID(bytes_le=uuid_bytes))

            # 4. Read in the remaining Global header fields, 1 signed int
            items = ['ctime', 
                     'mtime', 
                     'dfree',
                     'dtotal',
                     'descroff',
                     'descrlen', 
                     'dataoff', 
                     'datalen']

            for item in items:
                self.meta[item] = self.unpack_bytes(filey, fmt='1q')[0]

            # Load the definition file descriptors
            self.desc['deffile'] = self._load_deffile()
            self.desc['partition'] = self._load_partition()
            self.desc['signature'] = self._load_signature()

        # Update the user with what was loaded
        self.print_header()
        self.print_arch()
        self.print_descriptor_deffile() 
        self.print_descriptor_partition()
        self.print_descriptor_signature()

################################################################################
# Descriptors
################################################################################


    def _load_deffile(self):
        ''' load the header descriptor for the definition file. If a file
            object is not provided, open. The fields and format string are 
            provided via the self.Deffile object, which we get from 
            self.header --> __init__.py --> get_structure() --> SIF
        '''

        filey = open(self.image, 'rb')

        # Read to the description offset
        descriptors = dict()
        filey.seek(self.meta['descroff'])

        # see sif.header module for the default fields and format strings
        values = self.unpack_bytes(filey, self.Deffile.fmt)
         
        # Update the descriptors dictionary
        for d in range(len(values)):
            descriptors[self.Deffile.fields[d]] = values[d]

        # Can we get a name (this seems wrong) - loads as "."
        name = self.read_and_strip(filey, "%sc" % self.base.DescrNameLen)
        extra = self.read_and_strip(filey, '%sc' % self.base.DescrMaxPrivLen)

        descriptors['name'] = name
        descriptors['extra'] = extra

        # Save the location for the start of the partition
        self.Partition.start = filey.tell()

        # Definition File - offset should point us to the deffile    
        filey.seek(descriptors['Fileoff'])

        # And the length is also provided
        fmt = '%sc' % descriptors['Filelen']
        number = calcsize(fmt)
        deffile = filey.read(number)

        # Try to decode to utf-8 for the user
        try:
            deffile = deffile.decode('utf-8')
        except:
            pass

        descriptors['content'] = deffile
        filey.close()

        return descriptors


    def _load_partition(self):
        ''' load the paritition descriptor. We must get the start based on
            first reading the deffile desciptor, which adds the location
            to self.Parition.start. If we don't have this attribute, we need
            to run it first (This should not happen in normal cases, as they
            are called under one function, one after the other)
        '''
        if not hasattr(self.Partition, 'start'):
            self._load_deffile()

        filey = open(self.image, 'rb')

        partition = dict()
        filey.seek(self.Partition.start)

        # see sif.header module for the default fields and format strings
        values = self.unpack_bytes(filey, self.Deffile.fmt)
         
        # Update the descriptors dictionary
        for d in range(len(values)):
            partition[self.Partition.fields[d]] = values[d]

        # squashfs-955608129.img
        name = self.read_and_strip(filey, "%sc" % self.base.DescrNameLen)
        partition['name'] = name

        # partype and fstype might be part of extra?
        fstype, partype = self.unpack_bytes(filey, "2i")
        partition['fstype'] = fstype        
        partition['partype'] = partype

        # The remaining extra is the self.base.DescrMaxPrivLen - len(2i)
        fmt = '%sc' % (self.base.DescrMaxPrivLen - calcsize('2i'))       
        extra = self.read_and_strip(filey, fmt)

        partition['extra'] = extra

        # Can we find the start of the signature?
        self.Signature.start = filey.tell()
        filey.close()
        return partition


    def _load_signature(self):
        '''finally, load the signature descriptor. We again get the start
           based on loading the partition first.
        '''
        if not hasattr(self.Signature, 'start'):
            self._load_partition()

        filey = open(self.image, 'rb')

        signature = dict()
        filey.seek(self.Signature.start)
        values = self.unpack_bytes(filey, self.Signature.fmt)

        # If the first value is 0, the container isn't signed
        if values[0] != 0:

            for d in range(len(values)):
                signature[self.Signature.fields[d]] = values[d]

            # squashfs-955608129.img
            name = self.read_and_strip(filey, "%sc" % self.base.DescrNameLen)
            signature['name'] = name
            hashtype, = self.unpack_bytes(filey, "i") # unpack tuple

            # We need to parse the entity here (I don't know what that means)
            # see self.base.DescEntityLen

            # Go to the signature block, and retrieve it
            filey.seek(signature['Fileoff'])
            fmt = '%sc' % signature['Filelen']
            signed = self.read_and_strip(filey, fmt)

            signature['hastype'] = hashtype
            signature['publicKey'] = signed

        filey.close()
        return signature
