import re
from difflib import get_close_matches

import hamcrest as hc

# Words to ignore when looking up matchers
IGNORED_WORDS = ['should', 'to', 'be', 'a', 'an', 'is', 'the', 'as']

# Map of registered matchers as alias:callable
matchers = {}
# Map of normalized matcher aliases as normalized:alias
normalized = {}


def register(matcher, *aliases):
    """
    Register a matcher associated to one or more aliases. Each alias
    given is also normalized.
    """
    for alias in aliases:
        matchers[alias] = matcher
        # Map a normalized version of the alias
        norm = normalize(alias)
        normalized[norm] = alias
        # Map a version without snake case
        norm = norm.replace('_', '')
        normalized[norm] = alias

def unregister(matcher):
    """
    Unregister a matcher (or alias) from the registry
    """

    # If it's a string handle it like an alias
    if isinstance(matcher, basestring) and matcher in matchers:
        matcher = matchers[matcher]

    # Find all aliases associated to the matcher
    aliases = [k for k, v in matchers.iteritems() if v == matcher]
    for alias in aliases:
        del matchers[alias]
        # Clean up the normalized versions
        norms = [k for k, v in normalized.iteritems() if v == alias]
        for norm in norms:
            del normalized[norm]

    return len(aliases) > 0

def normalize(alias):
    """
    Normalizes an alias by removing adverbs defined in IGNORED_WORDS
    """

    # Convert from CamelCase to snake_case
    alias = re.sub(r'([a-z])([A-Z])', r'\1_\2', alias)
    # Ignore words
    words = alias.lower().split('_')
    words = filter(lambda(x): x not in IGNORED_WORDS, words)
    return '_'.join(words)

def lookup(alias):
    """
    Tries to find a matcher callable associated to the given alias. If
    an exact match does not exists it will try normalizing it and even
    removing underscores to find one.
    """

    if alias in matchers:
        return matchers[alias]
    else:
        norm = normalize(alias)
        if norm in normalized:
            alias = normalized[norm]
            return matchers[alias]

    # Check without snake case
    if -1 != alias.find('_'):
        norm = normalize(alias).replace('_', '')
        return lookup(norm)

    return None

def suggest(alias, max=3, cutoff=0.5):
    """
    Suggest a list of aliases which are similar enough
    """

    list = matchers.keys()
    similar = get_close_matches(alias, list, n=max, cutoff=cutoff)

    return similar


# Matchers should be defined with verbose aliases to allow the use of
# natural english where possible. When looking up a matcher common adverbs
# like 'to', 'be' or 'is' are ignored in the comparison.

register(hc.equal_to,
    'be_equal_to', 'be_eql_to', 'be_eq_to')
register(hc.instance_of,
    'be_an_instance_of', 'be_a', 'be_an')
register(hc.same_instance,
    'be_the_same_instance_as', 'be_the_same_as', 'be')

register(hc.has_entry,
    'have_the_entry', 'contain_the_entry')
register(hc.has_entries,
    'have_the_entries', 'contain_the_entries')
register(hc.has_key,
    'have_the_key', 'contain_the_key')
register(hc.has_value,
    'have_the_value', 'contain_the_value')
register(hc.is_in,
    'be_in')
register(hc.has_item,
    'have_the_item', 'contain_the_item')
register(hc.has_items,
    'have_the_items', 'contain_the_items')
register(hc.contains_inanyorder,
    'have_in_any_order', 'contain_in_any_order')
register(hc.contains,
    'have', 'contain')
register(hc.only_contains,
    'have_only', 'contain_only')
register(hc.close_to,
    'be_close_to')
register(hc.greater_than,
    'be_greater_than', 'be_gt')
register(hc.greater_than_or_equal_to,
    'be_greater_than_or_equal_to', 'be_ge')
register(hc.less_than,
    'be_less_than', 'be_lt')
register(hc.less_than_or_equal_to,
    'be_less_than_or_equal_to', 'be_le')
register(hc.has_length,
    'have_length')
register(hc.has_property,
    'have_the_property', 'contain_the_property')
register(hc.has_string,
    'have_the_string', 'contain_the_string')
register(hc.equal_to_ignoring_case,
    'be_equal_to_ignoring_case')
register(hc.equal_to_ignoring_whitespace,
    'be_equal_to_ignoring_whitespace')
#register(hc.contains_string, 'have_the_string', 'contain_the_string')
register(hc.ends_with,
    'end_with')
register(hc.starts_with,
    'start_with', 'begin_with')



from hamcrest.core.base_matcher import BaseMatcher

class TypeMatcher(BaseMatcher):
    def _matches(self, item):
        return isinstance(item, self.__class__.types)

    def describe_to(self, description):
        description.append_text(self.__class__.expected)

    def describe_mismatch(self, item, description):
        description.append_text('was a %s ' % item.__class__.__name__)
        description.append_description_of(item)

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls()

class IsInteger(TypeMatcher):
    types = (int, long)
    expected = 'an integer'

class IsFloat(TypeMatcher):
    types = float
    expected = 'a float'

class IsComplex(TypeMatcher):
    types = complex
    expected = 'a complex number'

class IsNumeric(TypeMatcher):
    types = (int, long, float, complex)
    expected = 'a numeric type'

class IsString(TypeMatcher):
    types = basestring
    expected = 'a string'

class IsStr(TypeMatcher):
    types = str
    expected = 'a str'

class IsUnicode(TypeMatcher):
    types = unicode
    expected = 'a unicode string'

class IsByteArray(TypeMatcher):
    types = 'bytearray'
    expected = 'a bytearray'

class IsBuffer(TypeMatcher):
    types = 'buffer'
    expected = 'a buffer'

class IsXrange(TypeMatcher):
    types = 'xrange'
    expected = 'an xrange'

class IsDict(TypeMatcher):
    types = dict
    expected = 'a dict'

class IsList(TypeMatcher):
    types = list
    expected = 'a list'

class IsTuple(TypeMatcher):
    types = tuple
    expected = 'a tuple'

class IsSet(TypeMatcher):
    types = set
    expected = 'a set'

class IsFrozenSet(TypeMatcher):
    types = frozenset
    expected = 'a frozenset'

class IsFunction(TypeMatcher):
    import types
    types = types.FunctionType
    expected = 'a function'

class IsBool(TypeMatcher):
    types = bool
    expected = 'a bool'


register(IsInteger, 'be_an_integer', 'be_an_int')
register(IsFloat, 'be_a_float')
register(IsComplex, 'be_a_complex_number', 'be_a_complex')
register(IsNumeric, 'be_numeric')
register(IsString, 'be_a_string')
register(IsStr, 'be_a_str')
register(IsUnicode, 'be_an_unicode_string', 'be_an_unicode')
register(IsByteArray, 'be_a_bytearray', 'be_a_byte_array')
register(IsBuffer, 'be_a_buffer')
register(IsXrange, 'be_an_xrange')
register(IsDict, 'be_a_dictionary', 'be_a_dict')
register(IsList, 'be_a_list', 'be_an_array')
register(IsTuple, 'be_a_tuple')
register(IsSet, 'be_a_set')
register(IsFrozenSet, 'be_a_frozenset', 'be_a_frozen_set')
register(IsFunction, 'be_a_function', 'be_a_func')
register(IsBool, 'be_a_boolean', 'be_a_bool')


class IsClass(BaseMatcher):
    def _matches(self, item):
        import inspect
        return inspect.isclass(item)

    def describe_to(self, desc):
        desc.append_text('a class')

register(IsClass, 'be_a_class')

class IsIterable(BaseMatcher):
    def _matches(self, item):
        try:
            iter(item)
            return True
        except TypeError:
            return False

    def describe_to(self, description):
        description.append_text('an iterable value')

register(lambda: IsIterable(), 'be_an_iterable')


class IsCallable(BaseMatcher):
    def _matches(self, item):
        return hasattr(item, '__call__')

    def describe_to(self, desc):
        desc.append_text('a callable value')

register(lambda: IsCallable(), 'be_callable')


class IsTruthy(BaseMatcher):
    def _matches(self, item):
        return True if item else False

    def describe_to(self, desc):
        desc.append_text('a truthy value')

class IsFalsy(BaseMatcher):
    def _matches(self, item):
        return True if not item else False

    def describe_to(self, desc):
        desc.append_text('a falsy value')

register(IsTruthy, 'be_a_truthy_value', 'be_truthy')
register(IsFalsy, 'be_a_falsy_value', 'be_falsy')


