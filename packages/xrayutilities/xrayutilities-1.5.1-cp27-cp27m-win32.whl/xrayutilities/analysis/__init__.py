# This file is part of xrayutilities.
#
# xrayutilities is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011-2016 Dominik Kriegner <dominik.kriegner@gmail.com>

"""
xrayutilities.analysis is a package for assisting with the analysis of
x-ray diffraction data, mainly reciprocal space maps

Routines for obtaining line cuts from gridded reciprocal space maps are
offered, with the ability to integrate the intensity perpendicular to the
line cut direction.
"""

# functions from sample_align.py
from .sample_align import psd_refl_align
from .sample_align import psd_chdeg
from .sample_align import linear_detector_calib
from .sample_align import area_detector_calib
from .sample_align import area_detector_calib_hkl
from .sample_align import miscut_calc
from .sample_align import fit_bragg_peak

# functions from line_cuts.py
from .line_cuts import get_qx_scan
from .line_cuts import get_qy_scan
from .line_cuts import get_qz_scan
from .line_cuts import get_omega_scan
from .line_cuts import get_radial_scan
from .line_cuts import get_ttheta_scan

# misc
from .misc import getangles
from .misc import getunitvector
from .misc import coplanar_intensity
