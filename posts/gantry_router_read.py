################################################################################
#
# Dan Heeks, 2010
#
# This program is released under the New BSD license. See the file COPYING for details.
################################################################################

import iso_read as iso
import sys

# just use the iso reader
class Parser(iso.Parser):
    def __init__(self):
        iso.Parser.__init__(self)
