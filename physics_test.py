import unittest
import physics as phy
import numpy as np

# Test funcions of functions in physics.py

class test_physics(unittest.TestCase):


    def test_normal_vec(self):
        L = 4
        r = np.array([[0,0],[1,2],[0,3]])
        rx, ry, D = phy.normal_vec_2d(r, L)

        print(D)
        print(rx)
        print(ry)
        # D_test = np.array([[1,np.sqrt(5)],[np.sqrt(5),1]])
        # rx_test = np.array([[0,-1],[1,0]])/np.sqrt(5)
        # ry_test = np.array([[0,-2],[2,0]])/np.sqrt(5)
        # np.testing.assert_array_almost_equal(D, D_test)
        # np.testing.assert_array_almost_equal(rx, rx_test)
        # np.testing.assert_array_almost_equal(ry, ry_test)

    #
    # def test_find_force(self):
    #     r = np.array([[0,0],[.1,.2]])
    #     L = 1
    #     f = phy.find_force(phy.leonard_jones, r, L)
    #     # print(f)




if __name__ == '__main__':
    unittest.main()
