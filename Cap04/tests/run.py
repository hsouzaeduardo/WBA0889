import unittest
if __name__ == '__main__':
    tests = unittest.TestLoader().discover('Cap04/tests', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)