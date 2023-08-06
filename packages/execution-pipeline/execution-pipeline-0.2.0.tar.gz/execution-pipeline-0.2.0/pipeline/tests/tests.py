import unittest

from pipeline.tests import helpers


class TestPipelineBasics(unittest.TestCase):

    def test_pre_execution_pipeline(self):
        a = helpers.A('sup')
        self.assertFalse(a.stored == 'sup')
        self.assertTrue(a.stored == 'this argument is always changed')

    def test_post_execution_pipeline(self):
        a = helpers.A()
        self.assertTrue(a.fun_boys(1, 2, 3, 4, 5)['added'] == 'yup')
        print(a.fun_boys1(1, 2, 3, 4, 5))
        self.assertTrue(a.fun_boys1(1, 2, 3, 4, 5)['also_added'] == 'also yup')

    def test_error_pipeline(self):
        a = helpers.A()
        self.assertEqual(a.fun_boys2(), "Don't worry, we handled a TypeError.")  # handles TypeError
        self.assertEqual(a.fun_boys2(1, 2, 3, 4, 5), "Don't worry, we handled MyException.")  # handles FailedTestError

    def test_cache_pipeline(self):
        # pipeline will return the last value of the function call instead of the current return value.
        # (such is the nature of caching :( )

        mc = helpers.MC()
        mc.changed_value = 500
        self.assertEqual(mc.fun_boys3(1, 2, 3, 4, 5), 500)
        mc.changed_value = 200
        self.assertEqual(mc.fun_boys3(1, 2, 3, 4, 5), 500)

        rc = helpers.RC()
        rc.changed_value = 500
        self.assertEqual(rc.fun_boys3(1, 2, 3, 4, 5), 500)
        rc.changed_value = 200
        self.assertEqual(rc.fun_boys3(1, 2, 3, 4, 5), 500)

        mmc = helpers.MMC()
        mmc.changed_value = 500
        self.assertEqual(mmc.fun_boys3(1, 2, 3, 4, 5), 500)
        mmc.changed_value = 200
        self.assertEqual(mmc.fun_boys3(1, 2, 3, 4, 5), 500)

    def test_no_cache_collision(self):
        # we have to ensure that methods across distinct classes are identified uniquely by key in the cache
        class1 = helpers.DistinctClass1()
        class2 = helpers.DistinctClass2()
        self.assertNotEqual(class1.avoid_collision(), class2.avoid_collision())


if __name__ == '__main__':
    unittest.main()
