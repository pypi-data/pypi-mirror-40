from class_pool.pool import poolize, Pool
from test.base import PoolTestCase


class PoolizeTestCase(PoolTestCase):

    def test_poolize_no_args(self):

        @poolize
        class TestClass(object):
            pass

        self.assertTrue(isinstance(Pool.of(TestClass), Pool))

    def test_poolize_args(self):

        @poolize(abstract=True)
        class TestClass(object):
            pass

        self.assertTrue(isinstance(Pool.of(TestClass), Pool))

    def test_poolize_subclasses(self):

        @poolize
        class TestClass(object):
            pass

        class SubClass(TestClass):
            pass

        pool = Pool.of(TestClass)

        self.assertIn(SubClass.__name__, pool)

    def test_custom_meta(self):

        class MyPool(Pool):
            base_class = None

        @poolize(MyPool)
        class TestClass(object):
            pass

        self.assertTrue(isinstance(Pool.of(TestClass), Pool))
