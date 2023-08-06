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
# Copyright (C) 2015 Dominik Kriegner <dominik.kriegner@gmail.com>

import os.path
import unittest

import numpy
import xrayutilities as xu

testfile = 'p08_00019.FIO'
datadir = os.path.join(os.path.dirname(__file__), 'data')
fullfilename = os.path.join(datadir, testfile)


@unittest.skipIf(not os.path.isfile(fullfilename),
                 "additional test data needed (http://xrayutilities.sf.io)")
class TestIO_FIO(unittest.TestCase):
    dshape = (601,)
    dmax = 2272108.0
    dmin = 66133.0
    dmaxcorr = 216583893672.0
    dmincorr = 0.0
    motmax = 8.000001
    motmin = 0.0
    tpos = 300
    dtpos = 1278952.0
    motorname = 'Motor_TT'
    countername = 'MythenIntegral'
    h5file = '_test_fio.h5'
    P08_normalizer = xu.IntensityNormalizer(
        "MCA",
        time='CountingTime',
        mon='MonitorEnergyWindow',
        absfun=lambda d: d['AttenuationFactor'])

    @classmethod
    def setUpClass(cls):
        scanname = os.path.splitext(testfile)[0]
        mcatmp = os.path.join(datadir, scanname, scanname+"_mythen_%i.raw")
        cls.fiofile = xu.io.SPECTRAFile(fullfilename, mcatmp=mcatmp)
        cls.sdata = cls.fiofile.data
        cls.motor = cls.sdata[cls.motorname]
        cls.inte = cls.sdata[cls.countername]
        cls.fiofile.Save2HDF5(cls.h5file, scanname)
        [cls.h5tt, dummy, cls.h5int], cls.h5data = xu.io.geth5_spectra_map(
            cls.h5file, [19], cls.motorname, 'ZS', cls.countername)

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.h5file)
        except OSError:
            pass

    def test_datashape(self):
        self.assertEqual(self.dshape, self.sdata[self.motorname].shape)
        self.assertEqual(self.dshape, self.sdata[self.countername].shape)

    def test_datavalues(self):
        self.assertAlmostEqual(self.motmax, self.motor.max(), places=6)
        self.assertAlmostEqual(self.motmin, self.motor.min(), places=6)
        self.assertAlmostEqual(self.dmax, self.inte.max(), places=6)
        self.assertAlmostEqual(self.dmin, self.inte.min(), places=6)
        self.assertAlmostEqual(self.dtpos, self.inte[self.tpos], places=6)

    def test_hdf5file(self):
        self.assertTrue(numpy.all(self.inte == self.h5int))
        self.assertTrue(numpy.all(self.motor == self.h5tt))

    def test_normalizer(self):
        mcac = self.P08_normalizer(self.h5data)
        self.assertAlmostEqual(self.dmaxcorr, mcac.max(), places=6)
        self.assertAlmostEqual(self.dmincorr, mcac.min(), places=6)


if __name__ == '__main__':
    unittest.main()
