################################################################################
#
# Dan Heeks, 2010
#
# This program is released under the New BSD license. See the file COPYING for details.
################################################################################

import nc
import iso_modal
import math

################################################################################
class Creator(iso_modal.Creator):

    def __init__(self):
        iso_modal.Creator.__init__(self)
        self.arc_centre_positive = True
        self.drillExpanded = True
        self.can_do_helical_arcs = False

    def tool_defn(self, id, name='', radius=None, length=None, gradient=None):
        pass
    
    def dwell(self, t):
        # to do, find out what dwell is on this machine
        pass
    
    def SPACE(self):
         return('')
            
################################################################################

nc.creator = Creator()
