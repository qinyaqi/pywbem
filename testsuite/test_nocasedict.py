#!/usr/bin/env python
"""
    Test case-insensitive dictionary implementation.
"""

from __future__ import absolute_import

import unittest
import warnings
import six

import pytest
import pytest_extensions

from pywbem.cim_obj import NocaseDict


class NonCompare(object):
    # pylint: disable=too-few-public-methods
    """Class that raises TypeError when comparing for equality or hashing."""

    def __eq__(self, other):
        raise TypeError("Cannot compare %s to %s" % (type(self), type(other)))

    def __ne__(self, other):
        raise TypeError("Cannot compare %s to %s" % (type(self), type(other)))

    def __hash__(self):
        raise TypeError("Cannot hash %s" % type(self))


class TestInit(unittest.TestCase):
    """Test initialization"""
    def test_all(self):
        """Test all init options"""
        # Empty

        dic = NocaseDict()
        self.assertTrue(len(dic) == 0)

        dic = NocaseDict(None)
        self.assertTrue(len(dic) == 0)

        dic = NocaseDict(list())
        self.assertTrue(len(dic) == 0)

        dic = NocaseDict(tuple())
        self.assertTrue(len(dic) == 0)

        dic = NocaseDict(dict())
        self.assertTrue(len(dic) == 0)

        dic = NocaseDict(dic)
        self.assertTrue(len(dic) == 0)

        # Initialise from iterable

        dic = NocaseDict([('Dog', 'Cat'), ('Budgie', 'Fish')])
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        dic = NocaseDict((('Dog', 'Cat'), ('Budgie', 'Fish')))
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        # Initialise from dictionary

        dic = NocaseDict({'Dog': 'Cat', 'Budgie': 'Fish'})
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        # Initialise from kwargs

        dic = NocaseDict(Dog='Cat', Budgie='Fish')
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        # Initialise from iterable and kwargs

        dic = NocaseDict([('Dog', 'Cat'), ], Budgie='Fish')
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        dic = NocaseDict((('Dog', 'Cat'),), Budgie='Fish')
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        # Initialise from dictionary and kwargs

        dic = NocaseDict({'Dog': 'Cat'}, Budgie='Fish')
        self.assertTrue(len(dic) == 2)
        self.assertTrue(dic['Dog'] == 'Cat' and dic['Budgie'] == 'Fish')

        # Initialise from unsupported object type

        try:
            dic = NocaseDict('illegal')
        except TypeError:
            pass
        else:
            self.fail("TypeError was unexpectedly not thrown.")

        # Initialise with too many positional arguments

        try:
            dic = NocaseDict(list(), list())
        except TypeError:
            pass
        else:
            self.fail("TypeError was unexpectedly not thrown.")


class BaseTest(unittest.TestCase):
    """Base class for following unit test. Does common setup which
       creates a NoCaseDict.
    """
    def setUp(self):
        """unittest setUp creates NoCaseDict"""
        self.dic = NocaseDict()
        self.dic['Dog'] = 'Cat'
        self.dic['Budgie'] = 'Fish'


class TestGetitem(BaseTest):
    """Tests for getitem"""
    def test_all(self):
        """All tests"""
        self.assertTrue(self.dic['dog'] == 'Cat')
        self.assertTrue(self.dic['DOG'] == 'Cat')

        try:
            self.dic['notfound']
        except KeyError:
            pass
        else:
            self.fail("KeyError was unexpectedly not thrown.")


class TestLen(BaseTest):
    """Tests for len of dict"""
    def test_all(self):
        """Test method"""
        self.assertTrue(len(self.dic) == 2)


class TestSetitem(BaseTest):
    """Test setting items"""
    def test_all(self):
        """All setitem tests"""
        self.dic['DOG'] = 'Kitten'
        self.assertTrue(self.dic['DOG'] == 'Kitten')
        self.assertTrue(self.dic['Dog'] == 'Kitten')
        self.assertTrue(self.dic['dog'] == 'Kitten')

        # Check that using a non-string key raises an exception

        try:
            self.dic[1234] = '1234'
        except TypeError:
            pass
        else:
            self.fail('TypeError expected')


class TestDelitem(BaseTest):
    """Class for del items from dictionary"""
    def test_all(self):
        """All tests"""
        del self.dic['DOG']
        del self.dic['budgie']
        self.assertTrue(self.dic.keys() == [])

        try:
            del self.dic['notfound']
        except KeyError:
            pass
        else:
            self.fail("KeyError was unexpectedly not thrown.")


class TestHasKey(BaseTest):
    """Class to test haskey on dict"""
    def test_all(self):
        """Method to test haskey"""
        self.assertTrue('DOG' in self.dic)
        self.assertTrue('budgie' in self.dic)
        self.assertTrue(1234 not in self.dic)


class TestKeys(BaseTest):
    """Class for TestKeys method"""
    def test_all(self):
        """All tests in single method"""
        keys = self.dic.keys()
        animals = ['Budgie', 'Dog']
        for ani in animals:
            self.assertTrue(ani in keys)
            keys.remove(ani)
        self.assertTrue(keys == [])


class TestValues(BaseTest):
    """Class for values tests"""
    def test_all(self):
        """Test all for TestValues"""
        values = self.dic.values()
        animals = ['Cat', 'Fish']
        for ani in animals:
            self.assertTrue(ani in values)
            values.remove(ani)
        self.assertTrue(values == [])


class TestItems(BaseTest):
    """Class for Test items"""
    def test_all(self):
        """All tests for item"""
        items = self.dic.items()
        animals = [('Dog', 'Cat'), ('Budgie', 'Fish')]
        for ani in animals:
            self.assertTrue(ani in items)
            items.remove(ani)
        self.assertTrue(items == [])


class TestClear(BaseTest):
    """Class for dict clear method"""
    def test_all(self):
        """All clear method tests"""
        self.dic.clear()
        self.assertTrue(len(self.dic) == 0)


class TestUpdate(BaseTest):
    """Class for test update method"""
    def test_all(self):
        """All methods for TestUpdate"""
        self.dic.clear()
        self.dic.update({'Chicken': 'Ham'})
        self.assertTrue(self.dic.keys() == ['Chicken'])
        self.assertTrue(self.dic.values() == ['Ham'])
        self.dic.clear()
        self.dic.update({'Chicken': 'Ham'}, {'Dog': 'Cat'})
        keys = self.dic.keys()
        vals = self.dic.values()
        keys = list(keys)
        vals = list(vals)
        keys.sort()
        vals.sort()
        self.assertTrue(keys == ['Chicken', 'Dog'])
        self.assertTrue(vals == ['Cat', 'Ham'])
        self.dic.update([('Chicken', 'Egg')], {'Fish': 'Eel'})
        self.assertTrue(self.dic['chicken'] == 'Egg')
        self.assertTrue(self.dic['fish'] == 'Eel')
        self.dic.update({'Fish': 'Salmon'}, Cow='Beef')
        self.assertTrue(self.dic['fish'] == 'Salmon')
        self.assertTrue(self.dic['Cow'] == 'Beef')
        self.assertTrue(self.dic['COW'] == 'Beef')
        self.assertTrue(self.dic['cow'] == 'Beef')


class TestCopy(BaseTest):
    """Class to test dict copy"""
    def test_all(self):
        """All tests for dict copy"""
        cp = self.dic.copy()
        self.assertEqual(cp, self.dic)
        self.assertTrue(isinstance(cp, NocaseDict))
        cp['Dog'] = 'Kitten'
        self.assertTrue(self.dic['Dog'] == 'Cat')
        self.assertTrue(cp['Dog'] == 'Kitten')


class TestGet(BaseTest):
    """Class to test get method"""
    def test_all(self):
        """Test get method"""
        self.assertTrue(self.dic.get('Dog', 'Chicken') == 'Cat')
        self.assertTrue(self.dic.get('Ningaui') is None)
        self.assertTrue(self.dic.get('Ningaui', 'Chicken') == 'Chicken')


class TestSetDefault(BaseTest):
    """Class for setdefault test methods"""
    def test_all(self):
        """All tests for setdefault of dict"""
        self.dic.setdefault('Dog', 'Kitten')
        self.assertTrue(self.dic['Dog'] == 'Cat')
        self.dic.setdefault('Ningaui', 'Chicken')
        self.assertTrue(self.dic['Ningaui'] == 'Chicken')


class TestPopItem(BaseTest):
    """Class for PopItem"""
    def test_all(self):
        """This test does nothing"""
        pass


testcases_NocaseDict_equal_hash = [

    # Each testcase tuple has these items:
    # * desc: Short testcase description.
    # * kwargs: Input arguments for test function, as a dict:
    #   * obj1: CIMInstanceName object #1 to use.
    #   * obj2: CIMInstanceName object #2 to use.
    #   * exp_obj_equal: Expected equality of the objects.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty dictionary",
        dict(
            obj1=NocaseDict([]),
            obj2=NocaseDict([]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "One item, keys and values equal",
        dict(
            obj1=NocaseDict([('k1', 'v1')]),
            obj2=NocaseDict([('k1', 'v1')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "One item, keys equal, values different",
        dict(
            obj1=NocaseDict([('k1', 'v1')]),
            obj2=NocaseDict([('k1', 'v1_x')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "One item, keys different, values equal",
        dict(
            obj1=NocaseDict([('k1', 'v1')]),
            obj2=NocaseDict([('k2', 'v1')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "One item, keys equal, values both None",
        dict(
            obj1=NocaseDict([('k1', None)]),
            obj2=NocaseDict([('k1', None)]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "One item, keys different lexical case, values equal",
        dict(
            obj1=NocaseDict([('K1', 'v1')]),
            obj2=NocaseDict([('k1', 'v1')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two equal items, in same order",
        dict(
            obj1=NocaseDict([('k1', 'v1'), ('k2', 'v2')]),
            obj2=NocaseDict([('k1', 'v1'), ('k2', 'v2')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two items, keys different lexical case, in same order",
        dict(
            obj1=NocaseDict([('K1', 'v1'), ('k2', 'v2')]),
            obj2=NocaseDict([('k1', 'v1'), ('K2', 'v2')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two equal items, in different order",
        dict(
            obj1=NocaseDict([('k1', 'v1'), ('k2', 'v2')]),
            obj2=NocaseDict([('k2', 'v2'), ('k1', 'v1')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Two items, keys different lexical case, in different order",
        dict(
            obj1=NocaseDict([('k1', 'v1'), ('K2', 'v2')]),
            obj2=NocaseDict([('k2', 'v2'), ('K1', 'v1')]),
            exp_obj_equal=True,
        ),
        None, None, True
    ),
    (
        "Comparing unicode value with binary value",
        dict(
            obj1=NocaseDict([('k1', b'v1')]),
            obj2=NocaseDict([('k2', u'v2')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Matching unicode key with string key",
        dict(
            obj1=NocaseDict([('k1', 'v1')]),
            obj2=NocaseDict([(u'k2', 'v2')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Higher key missing",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', 'Fish')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Lower key missing",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Dog', 'Cat')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "First non-matching key is less. But longer size!",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', 'Fish'), ('Curly', 'Snake'),
                             ('Cozy', 'Dog')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Only non-matching keys that are less. But longer size!",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Alf', 'F'), ('Anton', 'S'), ('Aussie', 'D')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "First non-matching key is greater. But shorter size!",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgio', 'Fish')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Only non-matching keys that are greater. But shorter size!",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Zoe', 'F')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. First non-matching key is less",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', 'Fish'), ('Curly', 'Snake')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. Only non-matching keys that are less",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Alf', 'F'), ('Anton', 'S')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size. Only non-matching keys that are greater",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Zoe', 'F'), ('Zulu', 'S')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size, only matching keys. First non-matching value is less",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Car')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
    (
        "Same size, only matching keys. First non-matching value is greater",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Caz')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
]

testcases_NocaseDict_equal = [

    # Each testcase tuple has these items:
    # * desc: Short testcase description.
    # * kwargs: Input arguments for test function, as a dict:
    #   * obj1: CIMInstanceName object #1 to use.
    #   * obj2: CIMInstanceName object #2 to use.
    #   * exp_obj_equal: Expected equality of the objects.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "A value raises TypeError when compared (and equal still succeeds)",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', NonCompare()), ('Dog', 'Cat')]),
            exp_obj_equal=False,
        ),
        None, None, True
    ),
]

testcases_NocaseDict_hash = [

    # Each testcase tuple has these items:
    # * desc: Short testcase description.
    # * kwargs: Input arguments for test function, as a dict:
    #   * obj1: CIMInstanceName object #1 to use.
    #   * obj2: CIMInstanceName object #2 to use.
    #   * exp_obj_equal: Expected equality of the objects.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "A value raises TypeError when compared (and hash fails)",
        dict(
            obj1=NocaseDict([('Budgie', 'Fish'), ('Dog', 'Cat')]),
            obj2=NocaseDict([('Budgie', NonCompare()), ('Dog', 'Cat')]),
            exp_obj_equal=False,
        ),
        TypeError, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    testcases_NocaseDict_equal_hash + testcases_NocaseDict_equal)
@pytest_extensions.test_function
def test_NocaseDict_equal(
        desc, kwargs, exp_exc_types, exp_warn_types, condition):
    """
    All test cases for NocaseDict.__eq__().
    """

    obj1 = kwargs['obj1']
    obj2 = kwargs['obj2']

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    eq1 = (obj1 == obj2)
    eq2 = (obj2 == obj1)
    ne1 = (obj1 != obj2)
    ne2 = (obj2 != obj1)

    exp_obj_equal = kwargs['exp_obj_equal']

    assert eq1 == exp_obj_equal
    assert eq2 == exp_obj_equal
    assert ne1 != exp_obj_equal
    assert ne2 != exp_obj_equal


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    testcases_NocaseDict_equal_hash + testcases_NocaseDict_hash)
@pytest_extensions.test_function
def test_NocaseDict_hash(
        desc, kwargs, exp_exc_types, exp_warn_types, condition):
    """
    All test cases for NocaseDict.__hash__().
    """

    obj1 = kwargs['obj1']
    obj2 = kwargs['obj2']

    # Double check they are different objects
    assert id(obj1) != id(obj2)

    # The code to be tested
    hash1 = hash(obj1)
    hash2 = hash(obj2)

    exp_hash_equal = kwargs['exp_obj_equal']

    assert (hash1 == hash2) == exp_hash_equal


class TestOrdering(BaseTest):
    """Verify that ordering comparisons between NocaseDict instances
    issue a deprecation warning, and for Python 3, in addition raise
    TypeError."""

    def assertWarning(self, comp_str):
        """Common function for assert warning"""
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            if six.PY2:
                eval(comp_str)  # pylint: disable=eval-used
            else:
                try:
                    eval(comp_str)  # pylint: disable=eval-used
                except TypeError as exc:
                    msg = str(exc)
                    if "not supported between instances" not in msg and \
                            "unorderable types" not in msg:
                        self.fail("Applying ordering to a dictionary in "
                                  "Python 3 did raise TypeError but with an "
                                  "unexpected message: %s" % msg)
                except Exception as exc:  # pylint: disable=broad-except
                    msg = str(exc)
                    self.fail("Applying ordering to a dictionary in Python 3 "
                              "did not raise TypeError, but %s: %s" %
                              (exc.__class__.__name__, msg))
                else:
                    self.fail("Applying ordering to a dictionary in Python 3 "
                              "succeeded (should not happen)")
            assert len(wlist) >= 1
            assert issubclass(wlist[-1].category, DeprecationWarning)
            assert "deprecated" in str(wlist[-1].message)

    def test_all(self):
        """Test for the compare options that should generate assertWarning"""
        self.assertWarning("self.dic < self.dic")
        self.assertWarning("self.dic <= self.dic")
        self.assertWarning("self.dic > self.dic")
        self.assertWarning("self.dic >= self.dic")


class TestContains(BaseTest):
    """Class for dict contains functionality"""
    def test_all(self):
        """Method for test dict contains functionality"""
        self.assertTrue('dog' in self.dic)
        self.assertTrue('Dog' in self.dic)
        self.assertTrue('Cat' not in self.dic)


class TestForLoop(BaseTest):
    """Class for test for loop with dictionary"""
    def test_all(self):
        """Test method for TestForLoop"""
        keys = set()
        for key in self.dic:
            keys.add(key)
        self.assertEqual(keys, set(['Budgie', 'Dog']))


class TestIterkeys(BaseTest):
    """Class for iterkeys test"""
    def test_all(self):
        """iterkeys test method"""
        keys = set()
        for key in self.dic.iterkeys():
            keys.add(key)
        self.assertEqual(keys, set(['Budgie', 'Dog']))


class TestItervalues(BaseTest):
    """Class for test itervalues test"""
    def test_all(self):
        """itervalues test method"""
        vals = set()
        for val in self.dic.itervalues():
            vals.add(val)
        self.assertEqual(vals, set(['Cat', 'Fish']))


class TestIteritems(BaseTest):
    """Class to test iteritems for dict"""
    def test_all(self):
        """Method for test iteritems for dict"""
        items = set()
        for item in self.dic.iteritems():
            items.add(item)
        self.assertEqual(items, set([('Budgie', 'Fish'), ('Dog', 'Cat')]))


class TestRepr(unittest.TestCase):
    """Class to test repr functionality for NocaseDict"""
    def test_reliable_order(self):
        """Test that repr() has a reliable result despite different orders of
        insertion into the dictionary."""

        dic1 = NocaseDict()
        dic1['Budgie'] = 'Fish'
        dic1['Dog'] = 'Cat'
        dic1['Foo'] = 'Bla'

        dic2 = NocaseDict()
        dic2['Foo'] = 'Bla'
        dic2['Dog'] = 'Cat'
        dic2['Budgie'] = 'Fish'

        self.assertEqual(repr(dic1), repr(dic2))


if __name__ == '__main__':
    unittest.main()
