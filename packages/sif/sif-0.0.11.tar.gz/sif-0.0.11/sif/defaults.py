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

'''

from sif.logger import bot
from sif.utils import ( 
    get_userhome, 
    read_json, 
    getenv,
    convert2boolean 
)
import tempfile
import os
import sys


#########################
# Caches
#########################

USERHOME = get_userhome()
SIF_VERSION = getenv("SIF_VERSION", "02")

# Singularity Cache
_cache = os.path.join(USERHOME, ".singularity")
SINGULARITY_CACHE = getenv("SINGULARITY_CACHEDIR", default=_cache)

# Temporary Storage
SIF_TMPDIR = os.environ.get('SIF_TMPDIR', tempfile.gettempdir())
