import unittest
from Signals import SignalTests
from Asset import AssetsTests
from Login import LoginTests
from SignUp import SignUpTests
from Device import DevicesTests
from ManageUser import ManageUserTests
from Tour import TourTests

def suite():
    suite = unittest.TestSuite()

    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(LoginTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(SignUpTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(AssetsTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(DevicesTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ManageUserTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(SignalTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TourTests))
   
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())