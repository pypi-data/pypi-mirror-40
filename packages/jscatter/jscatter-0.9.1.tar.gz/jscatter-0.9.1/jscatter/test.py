# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015  Ralf Biehl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""

This file is for testing of basic functions in dataarray and related modules.

Run as ::

 cd jscatter/directory
 python test.py

"""

import unittest
import os
import numpy.testing as nptest

import jscatter as js
import numpy as np
import scipy
from scipy import special
import pickle
from numpy import linalg as la

asciitext = """# these are really ugly data
 # temp     ;    293 1 2 3 4 5 6
 # pressure ; 1013 14  bar
 # @name     ; temp1bsa
 &doit
 0,854979E-01  0,178301E+03  0,383044E+02
 0,882382E-01  0,156139E+03  0,135279E+02
 0,909785E-01  **            0,110681E+02
 0,937188E-01  0,147430E+03  0,954762E+01
 0,964591E-01  0,141615E+03  0,846613E+01
 nan           nan           0
 1 2 3

# these are more really ugly data
 # temp     ;    1000 1 2 3 4 5 6
 # pressure ; 1013 12  bar
 # @name     ; temp2bsa
 &doit
 link @linktest
 1 2 3 0.
 2 1 2 3.
 3 1 2 .3
 4 1 2 .3
 5 1 2 .3
 6 1 2 .3
 nan  nan  0 0
 7 2 3 0

 @name linktest
 1 2 3 4 
 2 3 4 5 

"""


class dataArrayTest(unittest.TestCase):
    """
    Test for dataArray and access of all inside
    """

    def setUp(self):
        # create some data to test
        self.x = np.r_[0:10:0.1]
        x = self.x
        self.data = js.dA(
            np.c_[x, 1.234 * np.sin(x) + 0.001 * np.random.randn(len(x)), x * 0 + 0.001].T)  # simulate data with error
        self.data.amp = 1.234
        self.data.fit(lambda x, A, a, B: A * np.sin(a * x) + B, {'a': 1.2, 'B': 0}, {}, {'x': 'X', 'A': 'amp'},
                      output=False)
        x = np.r_[0:100:]
        data2 = js.dA(np.c_[x, x * 0 + 1.].T)
        data2.test = 'dumdum'
        data2.Y[1::4] = 2
        data2.Y[2::4] = 4
        data2.Y[3::4] = 5
        self.data3 = data2.prune(lower=7, number=25, type='mean+')
        with open('asciitestfile.dat', 'w') as f:    (f.write(asciitext))
        self.data4 = js.dA('asciitestfile.dat', replace={'#': '', ';': '', ',': '.'}, skiplines=['*', '**', 'nan'],
                           ignore='')
        self.data5 = js.dA('asciitestfile.dat', replace={'#': '', ';': '', ',': '.'},
                           skiplines=lambda w: any(a in ['**', 'nan'] for a in w), ignore='', index=1)
        self.data5.save('asciitestfile2.dat')
        self.data6 = js.dA('asciitestfile2.dat')
        self.sums = js.dA(np.c_[1:101, 0:100].T).prune(number=9, type='sum')
        self.mean = js.dA(np.c_[1:101, 0:100].T).prune(number=9, type='mean')

    def tearDown(self):
        os.remove('asciitestfile.dat')
        os.remove('asciitestfile2.dat')

    def test_fitchi2(self):
        # self.assertEqual( self.data.X,self.x )
        self.assertTrue(np.alltrue(self.data.X == self.x))
        self.assertLess(abs(self.data.lastfit.A - self.data.amp), 0.01)
        self.assertLess(abs(self.data.B), 0.1)
        self.assertLess(abs(self.data.lastfit.chi2 - 1), 0.5)

    def test_prune(self):
        self.assertEqual(self.data3.Y[-1], 3)
        self.assertAlmostEqual(self.data3.eY[-1], 1.58113883)
        self.assertEqual(self.data3.shape[1], 25)
        self.assertEqual(self.data3.X[0], 8.5)
        self.assertTrue(self.data3.test == 'dumdum')
        self.assertEqual(self.sums.X[5], 61.0)
        self.assertEqual(self.sums.Y[5], 660.)
        self.assertListEqual((self.sums.Y / self.sums[-1]).tolist(), self.mean.Y.tolist())

    def test_readwrite(self):
        self.assertEqual(self.data4.pressure[0], self.data5.pressure[0])
        self.assertEqual(self.data4.X[4], 1)
        self.assertEqual(self.data4[2, 4], 3)
        self.assertEqual(self.data4.pressure[-1], 'bar')
        self.assertEqual(self.data5.link.X[1], 2.0)
        self.assertEqual(self.data6.link.X[1], self.data5.link.X[1])
        self.assertEqual(self.data6.comment[1], self.data5.comment[1])


class dataListTest(unittest.TestCase):
    """
    Test for dataList and access of all inside

    Fit includes access of attributes and lot more
    if it is working it should be ok

    """

    def setUp(self):
        # model
        self.model = lambda A, D, t, wave=0: A * np.exp(-wave ** 2 * D * t)
        # data
        self.diff = js.dL(os.path.join(js.examples.datapath, 'iqt_1hho.dat'))
        self.diffm = self.diff.copy()
        self.diffm1 = self.diff.copy()
        self.diffm1.pop(10)
        self.diffm1.insert(10, os.path.join(js.examples.datapath, 'iqt_1hho.dat'), index=2)
        self.diffm1.append(os.path.join(js.examples.datapath, 'iqt_1hho.dat'), index=2)
        self.diff.fit(self.model, {'D': [0.1], 'A': 1}, {}, {'t': 'X', 'wave': 'q'}, condition=lambda a: a.X > 0.01,
                      output=False)
        self.diff.save('testdiffreread.dat')
        self.diffread = js.dL('testdiffreread.dat')
        self.pfdat = js.dL([js.dynamic.simpleDiffusion(q, np.r_[1:100:5], 1, 0.05) for q in np.r_[0.2:2:0.4]])
        self.pfdat[:3].save('pfdattestwrite.dat')
        self.pfreread = js.dL('pfdattestwrite.dat')
        self.pfreread.append('pfdattestwrite.dat', index=-1, XYeYeX=(0, 2, 1))  # take last and change Y,eY columns
        self.pfcalc = js.dynamic.simpleDiffusion(0.4, np.r_[1:100:5], 1, 0.05).Y
        self.pffit = self.pfdat.polyfit(wavevector=0.4, func=np.log, invfunc=np.exp, degy=2).Y
        self.serializedm = pickle.dumps(self.diffm.copy())
        self.serialized = pickle.dumps(self.diff.copy())

    def tearDown(self):
        os.remove('pfdattestwrite.dat')
        os.remove('testdiffreread.dat')

    def test_basic(self):
        self.diffm.mergeAttribut('q')
        self.assertEqual(self.diffm1[10].q, 0.4)
        self.assertEqual(self.diffm1[-1].q, 0.4)
        self.assertAlmostEqual(self.diffm.qmean[4], 0.65, places=4)

    def test_fitchi2(self):
        self.assertEqual(self.diff[0]._time[-1], 100.)
        self.assertAlmostEqual(self.diff.D[0], 0.086595, 5)
        self.assertAlmostEqual(self.diff.D_err.mean(), 0.00188324, 5)
        self.assertAlmostEqual(self.diff.A[0], 0.99, 2)
        self.assertAlmostEqual(self.diff.lastfit.chi2, 0.99, 2)
        self.assertAlmostEqual((self.pffit - self.pfcalc).sum(), 0)

    def test_readwritetest(self):
        # Test if file was read correctly
        self.assertAlmostEqual(self.pfdat[2].Y[-1], self.pfreread[-2].Y[-1])
        # test if append worked and Y and ey are changed
        self.assertAlmostEqual(self.pfdat[2].Y[-1], self.pfreread[-1].eY[-1])
        # test if dataList reread is working
        # test for length
        self.assertEqual(len(self.diff), len(self.diffread))
        # test common attributes
        self.assertAlmostEqual(self.diff.D_err[-1], self.diffread.D_err[-1], delta=1e-12)
        self.assertAlmostEqual(self.diff.D[-1], self.diffread.D[-1], delta=1e-12)

    def test_pickle(self):
        # normal pickle of dataList
        restoredm = pickle.loads(self.serializedm)
        nptest.assert_array_equal(restoredm[3].Y, self.diffm[3].Y)
        # model was lambda an cannot be pickled so it is removed
        restored = pickle.loads(self.serialized)
        nptest.assert_array_equal(restored[3].Y, self.diff[3].Y)
        self.assertEqual(restored.model, 'removed during serialization')


def f(x, a, b, c, d):
    return [x, x + a + b + c + d]


class parallelTest(unittest.TestCase):
    """
    Test for parallel
    """

    def setUp(self):
        # loop over first argument, here x
        self.abcd = [1, 2, 3, 4]
        self.res = js.parallel.doForList(f, looplist=range(100), a=self.abcd[0], b=self.abcd[1], c=self.abcd[2],
                                         d=self.abcd[3])

    def test_parallel(self):
        self.assertEqual(self.res[0][0] + np.sum(self.abcd), self.res[0][1])
        self.assertEqual(self.res[-1][0] + np.sum(self.abcd), self.res[-1][1])


class formelTest(unittest.TestCase):
    """
    Test for som things in formel
    """

    def setUp(self):
        self.waterelectrondensity = js.formel.scatteringLengthDensityCalc(['55.55h2o1', '0d2o1', '0.1Na1Cl1'],
                                                                          T=237.15 + 20)
        # points on sphere
        self.r = js.formel.fibonacciLatticePointsOnSphere(1000)
        self.fibzero = la.norm(js.formel.rphitheta2xyz(self.r).mean(axis=0))
        # pseudorandom gives always same numbers
        pr = js.formel.randomPointsOnSphere(1000)
        self.pseudorandomcenter = la.norm(js.formel.rphitheta2xyz(pr).mean(axis=0))
        t = np.r_[0:150:0.5]
        D = 0.3
        ds = 0.01
        self.diff = js.dynamic.simpleDiffusion(t=t, q=0.5, D=D)
        distrib = scipy.stats.norm(loc=D, scale=ds)
        x = np.r_[D - 5 * ds:D + 5 * ds:30j]
        pdf = np.c_[x, distrib.pdf(x)].T
        self.diff_g = js.formel.parQuadratureSimpson(js.dynamic.simpleDiffusion, -3 * ds + D, 3 * ds + D, parname='D',
                                                     weights=pdf, tol=0.01, q=0.5, t=t)

        self.gaussint = js.formel.parQuadratureAdaptiveGauss(js.formel.gauss, -20, 120, 'x', mean=50, sigma=10)

        # convolve
        s1 = 3
        s2 = 4
        m1 = 50
        m2 = 10
        G1 = js.formel.gauss(np.r_[0:100.1:0.1], mean=m1, sigma=s1)
        G2 = js.formel.gauss(np.r_[-30:30.1:0.2], mean=m2, sigma=s2)
        self.ggf = js.formel.convolve(G1, G2, 'full')
        self.gg = js.formel.convolve(G1, G2, 'valid')
        # smooth
        t = np.r_[-3:3:0.01]
        data = np.sin(t) + (js.formel.randomPointsInCube(len(t), 1000, 1).T[0] - 0.5) * 0.1
        self.smooth = js.dA(np.vstack([t, data]))
        self.smooth.Y = js.formel.smooth(self.smooth, windowlen=40, window='gaussian')

    def test_otherStuff(self):
        self.assertAlmostEqual(self.fibzero, 6.148627865656653e-06, 7)
        self.assertAlmostEqual(self.pseudorandomcenter, 0.003683277648, 7)
        # Ea
        z = np.linspace(-2., 2., 50)
        self.assertTrue(np.allclose(js.formel.Ea(z ** 2, 2.), np.cosh(z)))
        z = np.linspace(0., 2., 50)
        self.assertTrue(np.allclose(js.formel.Ea(np.sqrt(z), 0.5), np.exp(z) * special.erfc(-np.sqrt(z))))
        x = np.r_[-10:10:0.1]
        self.assertTrue(np.all(js.formel.Ea(x, 1, 1) - np.exp(x) < 1e-10))

    def test_materialData(self):
        self.assertAlmostEqual(self.waterelectrondensity[1], 334.329, delta=1e-2)
        self.assertAlmostEqual(js.formel.waterdensity(['55.55h2o1']), 0.9982071296, 7)
        self.assertAlmostEqual(js.formel.waterdensity(['55.55h2o1', '2.5Na1Cl1']), 1.096136675, 7)
        self.assertAlmostEqual(js.formel.bufferviscosity(['55.55h2o1', '1sodiumchloride']), 0.0010965190497, 7)
        self.assertAlmostEqual(js.formel.watercompressibility(units=1), 5.15392074e-05, 7)
        self.assertAlmostEqual(js.formel.viscosity(), 0.0010020268897, 7)

    def test_quadrature(self):
        # integration
        self.assertTrue(all(np.abs((self.diff.Y - self.diff_g.Y)) < 0.005))
        self.assertAlmostEqual(self.gaussint.Y[0], 1, 7)
        # convolution
        self.assertAlmostEqual(self.gg.Y.max(), self.ggf.Y.max(), 7)
        self.assertAlmostEqual(self.gg.X[self.gg.Y.argmax()], 60, 7)
        self.assertAlmostEqual(self.gg.X[self.gg.Y.argmax()], self.ggf.X[self.ggf.Y.argmax()], 7)
        self.assertAlmostEqual(self.ggf.X.max(), 130, 7)
        self.assertAlmostEqual(self.gg.X.max(), 70, 7)
        # smooth
        self.assertAlmostEqual(self.smooth.X[self.smooth.Y.argmax()] / np.pi, 0.5061127, 6)


class structurefactorTest(unittest.TestCase):
    """
    Test for structurefactor
    """

    def setUp(self):
        q = np.r_[0:5:0.5]
        q1 = js.loglist(0.01, 100, 2 ** 13)
        R = 2.5
        eta = 0.3
        scl = 5
        self.PY = js.sf.PercusYevick(q, 3, eta=0.2)
        self.RMSA = js.sf.RMSA(q, 3, 1, 0.001, eta=0.2)
        self.RMSA2 = js.sf.RMSA(q, 3, 1, 4.00, eta=0.3)
        self.fcc = js.sf.fccLattice(2, 1)
        self.fccSq = js.sf.latticeStructureFactor(np.r_[0.1:4:0.1], self.fcc)
        self.sfh = js.sf.RMSA(q=q1, R=R, scl=scl, gamma=0.01, eta=eta)
        self.grh = js.sf.sq2gr(self.sfh, R, interpolatefactor=1)

    def test_PYRMSA(self):
        # both like hard Sphere if small surface potential
        self.assertAlmostEqual(self.PY.Y[0], self.RMSA.Y[0], delta=1e-3)
        self.assertAlmostEqual(self.RMSA2.Y[0], 0.09347659, delta=1e-3)
        # Test of RMSA and sq2gr for correct q and Y value.
        self.assertAlmostEqual(self.grh.prune(lower=5).Y[0], 2.24010143, delta=1e-6)

    def test_latticePeaks(self):
        # peak positions in fcc crystal, test for lattices
        self.assertAlmostEqual(self.fccSq.q_hkl[0], 5.441398, delta=1e-6)
        self.assertAlmostEqual(self.fccSq.q_hkl[10], 17.77153170, delta=1e-6)


class formfactorTest(unittest.TestCase):
    """
    Test for formfactor
    """

    def setUp(self):
        self.csSphereI = js.ff.sphereCoreShell(0, 1., 2., -7., 1.).Y[0]
        R = 2
        NN = 10
        grid = np.mgrid[-R:R:1j * NN, -R:R:1j * NN, -R:R:1j * NN].reshape(3, -1).T
        p2 = 1 * 2  # p defines a superball with 1->sphere p=inf cuboid ....
        inside = lambda xyz, R: (np.abs(xyz[:, 0]) / R) ** p2 + (np.abs(xyz[:, 1]) / R) ** p2 + (
                np.abs(xyz[:, 2]) / R) ** p2 <= 1
        insidegrid = grid[inside(grid, R)]
        self.cloudsphere = js.ff.cloudScattering(np.r_[0, 2.3], insidegrid,
                                                 relError=50)  # takes about 1.9 s on single core
        self.gauss = js.ff.gaussianChain(np.r_[3:5:0.05], 5)

    def test_formfactor(self):
        # designed to have forward scattering equal zero
        self.assertEqual(self.csSphereI, 0)
        # This should get the minimum of the sphere formfactor at 2.3
        self.assertAlmostEqual(self.cloudsphere.Y[1], 1.27815704e-04)
        # normalization to one
        self.assertAlmostEqual(self.cloudsphere.Y[0], 1.)
        # mean of plateau in kratky plot
        self.assertAlmostEqual(np.diff(self.gauss.Y * self.gauss.X ** 2).mean(), 5.7681188e-6, delta=1e-4)


class sasTest(unittest.TestCase):
    """
    Test for sas
    """

    def setUp(self):
        q = np.r_[0.5:2:0.005]
        self.AgBeref = js.sas.AgBeReference(q, 0.58378)
        # test sasImage calibration
        self.calibration = js.sas.sasImage(os.path.join(js.examples.datapath, 'calibration.tiff'))
        self.calibration.recalibrateDetDistance()
        self.small = self.calibration.reduceSize(2, self.calibration.beamcenter, 100)
        self.small.data[:, :] = 100
        self.small.maskCircle([50, 50], 20)
        smalla = self.small.asdataArray('linear')
        self.smallamax = smalla[:, (np.abs(smalla.X) < 1) & (np.abs(smalla.Z) < 1)].max()
        small = self.calibration.reduceSize(2, self.calibration.beamcenter, 100)
        small.maskSectors([30, 30 + 180], 20, radialmax=100, invert=True)
        ismall = small.radialAverage()
        self.ismallYmax = ismall.Y[ismall.Y.argmax()]
        self.ismallXmax = ismall.X[ismall.Y.argmax()]

    def test_sas(self):
        # peak position of AgBe reference
        self.assertAlmostEqual(self.AgBeref.X[self.AgBeref.Y.argmax()], 1.076, delta=1e-3)
        self.assertAlmostEqual(self.calibration.detector_distance[0], 0.180676, delta=1e-4)
        self.assertAlmostEqual(self.smallamax, 100)
        self.assertAlmostEqual(self.ismallXmax, 1.051445, delta=1e-5)
        self.assertAlmostEqual(self.ismallYmax, 1219.9218, delta=1e-2)


class dynamicTest(unittest.TestCase):
    """
    Test for dynamic
    """

    def setUp(self):
        w = np.r_[-100:100:0.5]
        start = {'s0': 6, 'm0': 0, 'a0': 1, 's1': None, 'm1': 0, 'a1': 1, 'bgr': 0.00}
        resolution = js.dynamic.resolution_w(w, **start)
        D = 0.035
        qq = 5  # diffusion coefficient of protein alcohol dehydrogenase (140 kDa) is 0.035 nm**2/ns

        self.diff_ffw = js.dynamic.time2frequencyFF(js.dynamic.simpleDiffusion, resolution, q=qq, D=D)
        diff_w = js.dynamic.transDiff_w(w, q=qq, D=D)
        self.diff_cw = js.dynamic.convolve(diff_w, resolution, normB=1)

    def test_time2frequencyFF(self):
        X = self.diff_cw.X
        # compare diffusion with convolution and transform from time domain
        self.assertTrue(np.all(np.abs(
            (self.diff_ffw.interp(self.diff_cw.X[abs(X) < 70]) - self.diff_cw.Y[abs(X) < 70]) / self.diff_cw.Y[
                abs(X) < 70]) < 0.025))


def suite():
    loader = unittest.TestLoader()
    s = unittest.TestSuite()
    s.addTest(loader.loadTestsFromTestCase(dataListTest))
    s.addTest(loader.loadTestsFromTestCase(dataArrayTest))
    s.addTest(loader.loadTestsFromTestCase(parallelTest))
    s.addTest(loader.loadTestsFromTestCase(formelTest))
    s.addTest(loader.loadTestsFromTestCase(formfactorTest))
    s.addTest(loader.loadTestsFromTestCase(structurefactorTest))
    s.addTest(loader.loadTestsFromTestCase(sasTest))
    s.addTest(loader.loadTestsFromTestCase(dynamicTest))
    return s


def doTest(verbosity=1):
    """
    Do some test on Jscatter.

    Parameters
    ----------
    verbosity : int, default 1
        Verbosity level


    """
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite())


if __name__ == '__main__':
    unittest.main()
