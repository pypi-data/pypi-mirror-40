'''

Copyright (C) 2018-2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

The SIF header format is developed and licensed by Sylabs,
see https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go

'''

class Descriptor:
    '''A SIF Descriptor is the base, from which we derive 
       a Deffile, Signature, and Partition block. We read the descriptors after 
       the global header See
       https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go for details
       This isn't a class with functions, just an organizational structure
       for fields and the format string.    

       # Datatype  int32   <1i
       # Used      bool    ?
       # ID        uint32  I 
       # Groupid   uint32  I 
       # Link      uint32  I 
       # Fileoff   int64   q
       # Filelen   int64   q
       # Storelen  int64   q
       # Ctime     int64   q       
       # Mtime     int64   q              
       # UID       int64   q              
       # Gid       int64   q              

       # TODO these two aren't parsed yet
       # Name  [DescrNameLen]byte    self.base.DescrNameLen
       # Extra [DescrMaxPrivLen]byte // big enough for extra data below

    '''

    name = 'Descriptor'
    fields = [ "Datatype",  
               "Used",
               "ID",
               "Groupid",
               "Link",
               "Fileoff",
               "Filelen",
               "Storelen",
               "Ctime",
               "Mtime",
               "UID",
               "Gid"     ]

    # Format string to read in above
    fmt = '<i?3I7q'

    def __str__(self):
        return "SIF Descriptor version 02 %s" % self.name

    def __repr__(self):
        return self.__str__()


class Deffile(Descriptor):
    '''A SIF Deffile is the first descriptor. It is essentially a Descriptor.
    '''
    name = 'Deffile'

    def __init__(self):
        Descriptor.__init__(self)


class Partition(Descriptor):
    '''A SIF Partition is the third block (id 2 at index 1). It has,
       in addition to the same fields, a fstype, parttype, and content.
       I'm not sure what content is, but the fstype and partype (I think)
       are under "extra"

           fstype: Squashfs   int32
           parttype: System   int32
           content: Linux     (not sure)
    '''
    name = 'Partition'

    def __init__(self):
        Descriptor.__init__(self)


class Signature(Descriptor):
    '''A SIF Signature is the fourth block (third descriptor) 
       It has the following fields under "extra"

           hashtype: SHA384
           entity: @ 
    '''
    name = 'Signature'

    def __init__(self):
        Descriptor.__init__(self)
