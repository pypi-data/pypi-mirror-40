BinSeqs - Support for binary sequence formats in Bioython
=========================================================

BinSeqs is a Python package intended to enrich the SeqIO
framework from [Biopython](https://biopython.org/) by adding
support for some binary sequence formats.


Formats supported
-----------------

* `xdna` format, used by _DNA Strider_ and
  [Serial Cloner](http://serialbasics.free.fr/Serial_Cloner.html):
  reading and writing supported
* `snapgene` format, used by [SnapGene](https://www.snapgene.com/):
  reading support only


Usage
-----
The BinSeqs parsers and writers are not designed to be used
independently and should instead be used through the Biopython's
SeqIO module.

Simply import the `incenp.bio.seqio` module to make the parsers
and writers available to Biopython's SeqIO:

    from Bio import SeqIO
    import incenp.bio.seqio

    records = list(SeqIO.parse('snapgene_file.dna', 'snapgene'))
    SeqIO.write(records, 'serialcloner_file.xdna', 'xdna')


Copying
-------
BinSeqs is free software and distributed under the terms of
a BSD-like license. The full license is included in the
[LICENSE.txt file](LICENSE.txt) of the source distribution.


Homepage
--------
The project is located at https://incenp.org/dvlpt/binseqs.html
(homepage) and https://git.incenp.org/damien/binseqs (repository
and bug tracker).
