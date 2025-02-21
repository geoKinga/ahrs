#!/usr/bin/env python3
import unittest
import numpy as np
import ahrs

class TestQuaternion(unittest.TestCase):
    def setUp(self) -> None:
        # Identity Quaternion
        self.q0 = ahrs.Quaternion()
        # Versor from 3D array
        self.vector3 = np.random.random(3)-0.5
        self.q3 = ahrs.Quaternion(self.vector3)
        self.vector3 /= np.linalg.norm(self.vector3)
        # Versor from 4D array
        self.vector4 = np.random.random(4)-0.5
        self.q4 = ahrs.Quaternion(self.vector4)
        self.vector4 /= np.linalg.norm(self.vector4)
        self.decimal_precision = 15

    def test_identity_quaternion(self):
        self.assertEqual(self.q0.w, 1.0)
        self.assertEqual(self.q0.x, 0.0)
        self.assertEqual(self.q0.y, 0.0)
        self.assertEqual(self.q0.z, 0.0)
        np.testing.assert_equal(self.q0.v, np.zeros(3))

    def test_conjugate(self):
        qc = self.q4.conjugate
        self.assertAlmostEqual(qc[0], self.q4.w, places=self.decimal_precision)
        self.assertAlmostEqual(qc[1], -self.q4.x, places=self.decimal_precision)
        self.assertAlmostEqual(qc[2], -self.q4.y, places=self.decimal_precision)
        self.assertAlmostEqual(qc[3], -self.q4.z, places=self.decimal_precision)
        np.testing.assert_almost_equal(qc[1:], -self.q4.v, decimal=self.decimal_precision)

    def test_conj(self):
        qc = self.q4.conj
        self.assertAlmostEqual(qc[0], self.q4.w, places=self.decimal_precision)
        self.assertAlmostEqual(qc[1], -self.q4.x, places=self.decimal_precision)
        self.assertAlmostEqual(qc[2], -self.q4.y, places=self.decimal_precision)
        self.assertAlmostEqual(qc[3], -self.q4.z, places=self.decimal_precision)
        np.testing.assert_almost_equal(qc[1:], -self.q4.v, decimal=self.decimal_precision)

    def test_inverse(self):
        qi = self.q4.inverse
        self.assertAlmostEqual(qi[0], self.q4.w, places=self.decimal_precision)
        self.assertAlmostEqual(qi[1], -self.q4.x, places=self.decimal_precision)
        self.assertAlmostEqual(qi[2], -self.q4.y, places=self.decimal_precision)
        self.assertAlmostEqual(qi[3], -self.q4.z, places=self.decimal_precision)
        np.testing.assert_almost_equal(qi[1:], -self.q4.v, decimal=self.decimal_precision)

    def test_inv(self):
        qi = self.q4.inv
        self.assertAlmostEqual(qi[0], self.q4.w, places=self.decimal_precision)
        self.assertAlmostEqual(qi[1], -self.q4.x, places=self.decimal_precision)
        self.assertAlmostEqual(qi[2], -self.q4.y, places=self.decimal_precision)
        self.assertAlmostEqual(qi[3], -self.q4.z, places=self.decimal_precision)
        np.testing.assert_almost_equal(qi[1:], -self.q4.v, decimal=self.decimal_precision)

    def test_is_pure(self):
        self.assertFalse(self.q0.is_pure())
        self.assertTrue(self.q3.is_pure())
        self.assertFalse(self.q4.is_pure())

    def test_is_real(self):
        self.assertTrue(self.q0.is_real())
        self.assertFalse(self.q3.is_real())
        self.assertFalse(self.q4.is_real())

    def test_is_versor(self):
        self.assertTrue(self.q0.is_versor())
        self.assertTrue(self.q3.is_versor())
        self.assertTrue(self.q4.is_versor())

    def test_is_identity(self):
        self.assertTrue(self.q0.is_identity())
        self.assertFalse(self.q3.is_identity())
        self.assertFalse(self.q4.is_identity())

    def test_versor_from_3d_array(self):
        self.assertAlmostEqual(self.q3.w, 0.0, places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.x, self.vector3[0], places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.y, self.vector3[1], places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.z, self.vector3[2], places=self.decimal_precision)
        np.testing.assert_almost_equal(self.q3.v, self.vector3, decimal=self.decimal_precision)

    def test_versor_from_4d_array(self):
        self.assertAlmostEqual(self.q4.w, self.vector4[0], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.x, self.vector4[1], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.y, self.vector4[2], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.z, self.vector4[3], places=self.decimal_precision)
        np.testing.assert_almost_equal(self.q4.v, self.vector4[1:], decimal=self.decimal_precision)

    def test_wrong_input_array(self):
        self.assertRaises(TypeError, ahrs.Quaternion, True)
        self.assertRaises(TypeError, ahrs.Quaternion, 3.0)
        self.assertRaises(TypeError, ahrs.Quaternion, "[1.0, 2.0, 3.0, 4.0]")
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random((6, 3)))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random((6, 4)))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random(2))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random(2).tolist())
        self.assertRaises(ValueError, ahrs.Quaternion, np.zeros(3))

    def test_wrong_input_dcm(self):
        self.assertRaises(TypeError, ahrs.Quaternion, dcm=3)
        self.assertRaises(TypeError, ahrs.Quaternion, dcm=3.0)
        self.assertRaises(TypeError, ahrs.Quaternion, dcm="np.identity(3)")
        self.assertRaises(ValueError, ahrs.Quaternion, dcm=np.random.random((3, 3)))
        self.assertRaises(ValueError, ahrs.Quaternion, dcm=-np.identity(3))

class TestQuaternionArray(unittest.TestCase):
    def setUp(self) -> None:
        self.Q0 = ahrs.QuaternionArray()
        self.Q1 = ahrs.QuaternionArray(np.identity(4))
        self.decimal_precision = 15

    def test_identity_quaternion(self):
        self.assertEqual(self.Q0.w, [1.0])
        self.assertEqual(self.Q0.x, [0.0])
        self.assertEqual(self.Q0.y, [0.0])
        self.assertEqual(self.Q0.z, [0.0])
        np.testing.assert_equal(self.Q0.v, np.atleast_2d(np.zeros(3)))

    def test_4_by_4_array(self):
        np.testing.assert_equal(self.Q1.w, [1.0, 0.0, 0.0, 0.0])
        np.testing.assert_equal(self.Q1.x, [0.0, 1.0, 0.0, 0.0])
        np.testing.assert_equal(self.Q1.y, [0.0, 0.0, 1.0, 0.0])
        np.testing.assert_equal(self.Q1.z, [0.0, 0.0, 0.0, 1.0])
        np.testing.assert_equal(self.Q1.v, np.identity(4)[:, 1:])

    def test_quaternion_average(self):
        # Create 10 continuous quaternions representing rotations around the
        # Z-axis between 0 and 90 degrees and average them. The mean quaternion
        # must be, naturally, equal to the 45 degree quaternion.
        Q = ahrs.QuaternionArray([ahrs.Quaternion(rpy=np.array([0.0, 0.0, x])*ahrs.DEG2RAD) for x in range(0, 100, 10)])
        np.testing.assert_almost_equal(Q.average(), ahrs.Quaternion(rpy=np.array([0.0, 0.0, 45.0])*ahrs.DEG2RAD), decimal=self.decimal_precision)

    def test_wrong_input_array(self):
        self.assertRaises(TypeError, ahrs.QuaternionArray, True)
        self.assertRaises(TypeError, ahrs.QuaternionArray, 3.0)
        self.assertRaises(TypeError, ahrs.QuaternionArray, "[[1.0, 2.0, 3.0, 4.0]]")

if __name__ == "__main__":
    unittest.main()
