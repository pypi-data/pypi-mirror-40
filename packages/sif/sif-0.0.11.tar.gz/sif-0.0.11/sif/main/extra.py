    def load_next(self, until_char=None):
        '''read in the header, byte by byte, and go until we hit the 
           null terminating character \0
        '''
        # If not defined, load until terminating string
        if until_char is None:
            until_char = self.base.EndChar

        byte = filey.read(1)
        item = b''

        # We will use the number to decode it
        number = 1
        while byte:
            item = item + byte
            byte = filey.read(1)
            number += 1
            if byte == until_char:
                break

        # The length is the number of characters we've read
        fmt = '%ss' % number
        return self.unpack(fmt, item)


    def _load_signatures(self, filey=None, close_file=False):

        # By default, we assume that we will not close the file handle
        close_file = False
 
        # Unless it's not provided, we need to clean up
        if filey == None:
            filey = open(self.image, 'rb')
            close_file = True

        offset = ( self.meta['descroff'] +      # start of offset
                   self.base.DescrNameLen +     # length of name (128)
                   self.base.DescrMaxPrivLen )  # max private length

        # Let's try reading in different ones...
        for o in range(0, self.meta['descrlen']):
            offset = self.meta['descroff'] + o
            filey.seek(offset)
            values = self.unpack_bytes(filey, self.Deffile.fmt)
            if values[3] = [1, 2, 3]:
                print('offset %s, %s' %(offset, values))


        # let's try to find based on iota increments
        for o in range(0, self.meta['descrlen'] * 10):
            offset = self.meta['descroff'] + o
            filey.seek(offset)
            values = self.unpack_bytes(filey, part.fmt)
            if int(values[0]/1000) == 16:
                print('offset %s, %s' %(offset, values))



        filey.seek(self.Signature.start)

        # Brute force it again 
        for o in range(0, self.meta['datalen']):
            offset = self.Signature.start + o
            filey.seek(offset)
            values = self.unpack_bytes(filey, self.Signature.fmt)
            if values[0] != 0:
                try:
                    when = datetime.datetime.fromtimestamp(values[8])
                    if when.year > 2015 and when.year < 2019:
                        print('Offset %s: %s' % (offset, datetime.datetime.fromtimestamp(values[8])))
                    #print('offset %s, %s' %(offset, values))
                except:
                    pass

        # see sif.header module for the default fields and format strings
        values = self.unpack_bytes(filey, self.Signature.fmt)
         
        # Update the descriptors dictionary
        for d in range(len(values)):
            partition[self.Partition.fields[d]] = values[d]

        # squashfs-955608129.img
        name = self.read_and_strip(filey, "%sc" % self.base.DescrNameLen)
        partition['name'] = name

        # I think partype and fstype might be part of extra?
        fstype, partype = self.unpack_bytes(filey, "2i")
        partition['fstype'] = fstype        
        partition['partype'] = partype

        # The remaining extra is the self.base.DescrMaxPrivLen - len(2i)
        fmt = '%sc' % (self.base.DescrMaxPrivLen - calcsize('2i'))
       
        # Can we get a name (this seems wrong) !
        extra = self.read_and_strip(filey, fmt)

        partition['extra'] = extra

        # Can we find the start of the signature?
        self.Signature.start = filey.tell()

