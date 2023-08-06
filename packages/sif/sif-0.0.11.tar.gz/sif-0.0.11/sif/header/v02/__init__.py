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

# We will add different versions to bases

from .globalHeader import ( arches, HeaderBase )
from .descriptors import ( Deffile, Partition, Signature )
