# SIF (Python)

Sif Python (sif) is the Python API for working with the Singularity SIF image
format. This library is under development, and contributions are welcome! 
The basic functionality so far is to parse the header, only using Python:


```
from sif.main import SIFHeader

SIFHeader('boxes.simg')
boxes.simg is a SIF file.
SIF Header version 01
SIF Header arch 02
SIF Header uuid 0eae46df-1975-e44c-888b-8b9915f87f52
SIF Header ctime 1544537033
SIF Header mtime 1546726508
SIF Header dfree 45
SIF Header dtotal 48
SIF Header descroff 4096
SIF Header descrlen 28080
SIF Header dataoff 32768
SIF Header datalen 196953019

Architecture: AMD64 arch code

Deffile Datatype 16385
Deffile Used True
Deffile ID 1
Deffile Groupid 4026531841
Deffile Link 0
Deffile Fileoff 32768
Deffile Filelen 39
Deffile Storelen 39
Deffile Ctime 1544537033
Deffile Mtime 1544537033
Deffile UID 0
Deffile Gid 0
Deffile name .
Deffile extra 

Partition Datatype 16388
Partition Used True
Partition ID 2
Partition Groupid 4026531841
Partition Link 0
Partition Fileoff 36864
Partition Filelen 196947968
Partition Storelen 196952025
Partition Ctime 1544537033
Partition Mtime 1544537033
Partition UID 0
Partition Gid 0
Partition name squashfs-955608129.img
Partition fstype 1
Partition partype 2
Partition extra 02

Signature Datatype 16389
Signature Used True
Signature ID 3
Signature Groupid 4026531841
Signature Link 2
Signature Fileoff 196984832
Signature Filelen 955
Signature Storelen 955
Signature Ctime 1546726508
Signature Mtime 1546726508
Signature UID 0
Signature Gid 0
Signature name part-signature
Signature hastype 2
Signature publicKey -----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

SIFHASH:
4de3d88a550a8c1976b54b91445b027af718cb0bf38133c50dcd723fdba54a28177008e2f4bb7e7cc81aa4d82c0c27fa
-----BEGIN PGP SIGNATURE-----

wsFcBAEBCAAQBQJcMSxrCRBi+gdpIWqw6QAAiZsQAAJgTPQ5QVuiLq0s7PAM9gPK
YLmxEN3UiTS0BF2a/DffKmYMCdrZwKyx0fybWZMOAREfobTbbqNhL0dvk6idMtfR
wvHSDmKl1gx9LZ764ddyaX/NdsHZMrtDLBe2AMuCoAEZOpN0/BQQRiuQMYBbWiVz
3DMyvvqXdzKnc6OYu1wBlr+q0GG2I4HRGGfZayZUHtgh4okPVJSndxgD5Rz1zeC5
GZUiHJyh3Jru8wc7hEivgHGXRfP5S+VedrGYX/gam/iH26t/nMGY7AFN5IIMr1t0
I54HCJCf0NcwTfruzwwE80d6+BrLa082uuS6qD+PKhyEaqm8jZVFw2On9EJuIkje
R6f3Q2IagrOHh/axGrXMUcSA6tBkw0IRbS/NBw/0hjpiRLCOY5C+qp4WWS+Oo34k
09eO4UmlDkKTScc72yxNRTAMBc0f/o5pncirXVCwbUMAMkMsZOBS8lN72WFDGzk4
mnOTsiBntG29ryjtWQctKWJN+M7v8s8ib+iFCgBJbMyBR//z4z1OkkCUDxee5bvF
bnvAVpEpOj0DvOmH/2za3Olyoez3ueGo5HNCfbKq4FBgKo/KB3cIp41cVcohSpSV
zgtARAKG1paRof+zXP0xatL+TDXazytRyNgXrprJbrZvjm4/jXhhT31D8s/8kZx1
hK2q7TKN3URs6h7olmt+
=E8Je
-----END PGP SIGNATURE-----
```



## Usage

By default, the SIF header version provided is the most up to date with Singularity.
If you need to specify a particular header, set the environment variable for it:

```bash
SIF_VERSION="02"
export SIF_VERSION
```

### Python

In Python, you will likely want to start with an image, and load it for inspection.
The client will quickly tell you if it's a SIF header or not based on the `SIF_MAGIC`
after the interpreter line:

**This is a SIF image**

```python
image = 'salad.simg'
from sif.main import SIFHeader
header = SIFHeader(image)

boxes.simg is a SIF file.
Architecture: AMD64 arch code
Found SIF version 01
Found SIF arch 02
```

You don't have to load the header right away:

```python
header = SIFHeader('boxes.simg', load=False)
boxes.simg is a SIF file.

header.load_header()

Architecture: AMD64 arch code
Found SIF version 01
Found SIF arch 02
```

**This is not a SIF image**

```python
image = 'salad.simg'
from sif.main import SIFHeader
header = SIFHeader(image)
...
ERROR salad.simg is not a SIF file.
```

## Licenses

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).
The SIF Header format is licesed by [Sylabs](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go).
