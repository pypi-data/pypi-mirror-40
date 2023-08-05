# -*- coding: utf-8 -*-
#
# Copyright (c), 2018, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
XPath 2.0 implementation - part 3 (XSD constructors and multi-role tokens)
"""
import decimal
import codecs

from .compat import unicode_type, urlparse, URLError, string_base_type
from .exceptions import ElementPathError, ElementPathMissingContextError, xpath_error
from .xpath_helpers import is_attribute_node, boolean_value, string_value
from .datatypes import DateTime, Date, Time, GregorianDay, GregorianMonth, GregorianMonthDay, \
    GregorianYear, GregorianYearMonth, UntypedAtomic, Duration, YearMonthDuration, DayTimeDuration
from .xpath2_functions import XPath2Parser, WHITESPACES_RE_PATTERN, QNAME_PATTERN, \
    NMTOKEN_PATTERN, NAME_PATTERN, NCNAME_PATTERN, HEX_BINARY_PATTERN, \
    NOT_BASE64_BINARY_PATTERN, LANGUAGE_CODE_PATTERN, WRONG_ESCAPE_PATTERN


def collapse_white_spaces(s):
    return WHITESPACES_RE_PATTERN.sub(' ', s).strip()


register = XPath2Parser.register
unregister = XPath2Parser.unregister
method = XPath2Parser.method
constructor = XPath2Parser.constructor


###
# Constructors for string-based XSD types
@constructor('normalizedString')
def cast(value):
    return str(value).replace('\t', ' ').replace('\n', ' ')


@constructor('token')
def cast(value):
    return collapse_white_spaces(value)


@constructor('language')
def cast(value):
    match = LANGUAGE_CODE_PATTERN.match(collapse_white_spaces(value))
    if match is None:
        raise xpath_error('FOCA0002', "%r is not a language code" % value)
    return match.group()


@constructor('NMTOKEN')
def cast(value):
    match = NMTOKEN_PATTERN.match(collapse_white_spaces(value))
    if match is None:
        raise xpath_error('FOCA0002', "%r is not an xs:NMTOKEN value" % value)
    return match.group()


@constructor('Name')
def cast(value):
    match = NAME_PATTERN.match(collapse_white_spaces(value))
    if match is None:
        raise xpath_error('FOCA0002', "%r is not an xs:Name value" % value)
    return match.group()


@constructor('NCName')
@constructor('ID')
@constructor('IDREF')
@constructor('ENTITY')
def cast(value):
    match = NCNAME_PATTERN.match(collapse_white_spaces(value))
    if match is None:
        raise xpath_error('FOCA0002', "invalid value %r for constructor" % value)
    return match.group()


@constructor('anyURI')
def cast(value):
    uri = collapse_white_spaces(value)
    try:
        urlparse(uri)
    except URLError:
        raise xpath_error('FOCA0002', "%r is not an xs:anyURI value" % value)
    if uri.count('#') > 1:
        raise xpath_error('FOCA0002', "%r is not an xs:anyURI value (too many # characters)" % value)
    elif WRONG_ESCAPE_PATTERN.search(uri):
        raise xpath_error('FOCA0002', "%r is not an xs:anyURI value (wrong escaping)" % value)
    return uri


###
# Constructors for numeric XSD types
@constructor('decimal')
def cast(value):
    try:
        return decimal.Decimal(value)
    except (ValueError, decimal.DecimalException) as err:
        raise xpath_error('FORG0001', str(err))


@constructor('double')
@constructor('float')
def cast(value):
    try:
        return float(value)
    except ValueError as err:
        raise xpath_error('FORG0001', str(err))


def cast_to_integer(value, lower_bound=None, higher_bound=None):
    """
    XSD integer types constructor helper.

    :param value: the value to convert.
    :param lower_bound: if not `None` the result must be higher or equal than its value.
    :param higher_bound: if not `None` the result must be lesser than its value.
    :return: an empty list if the argument is the empty sequence or an `int` instance.
    :raise: an `ElementPathValueError` if the value is not decodable to an integer or if \
    the value is out of bounds.
    """
    if isinstance(value, string_base_type):
        try:
            result = int(float(value))
        except ValueError:
            raise xpath_error('FORG0001', 'could not convert %r to integer' % value)
    else:
        try:
            result = int(value)
        except ValueError as err:
            raise xpath_error('FORG0001', str(err))

    if lower_bound is not None and result < lower_bound:
        raise xpath_error('FORG0001', "value %d is too low" % result)
    elif higher_bound is not None and result >= higher_bound:
        raise xpath_error('FORG0001', "value %d is too high" % result)
    return result


@constructor('integer')
def cast(value):
    return cast_to_integer(value)


@constructor('nonNegativeInteger')
def cast(value):
    return cast_to_integer(value, 0)


@constructor('positiveInteger')
def cast(value):
    return cast_to_integer(value, 1)


@constructor('nonPositiveInteger')
def cast(value):
    return cast_to_integer(value, higher_bound=1)


@constructor('negativeInteger')
def cast(value, context=None):
    return cast_to_integer(value, higher_bound=0)


@constructor('long')
def cast(value):
    return cast_to_integer(value, -2**127, 2**127)


@constructor('int')
def cast(value):
    return cast_to_integer(value, -2**63, 2**63)


@constructor('short')
def cast(value):
    return cast_to_integer(value, -2**15, 2**15)


@constructor('byte')
def cast(value):
    return cast_to_integer(value, -2**7, 2**7)


@constructor('unsignedLong')
def cast(value):
    return cast_to_integer(value, 0, 2**128)


@constructor('unsignedInt')
def cast(value):
    return cast_to_integer(value, 0, 2**64)


@constructor('unsignedShort')
def cast(value):
    return cast_to_integer(value, 0, 2**16)


@constructor('unsignedByte')
def cast(value):
    return cast_to_integer(value, 0, 2**8)


###
# Constructors for datetime XSD types
@constructor('dateTime')
def cast(value, tz=None):
    return DateTime.fromstring(value, tz=tz)


@constructor('date')
def cast(value, tz=None):
    return Date.fromstring(value, tz=tz)


@constructor('gDay')
def cast(value, tz=None):
    return GregorianDay.fromstring(value, tz=tz)


@constructor('gMonth')
def cast(value, tz=None):
    return GregorianMonth.fromstring(value, tz=tz)


@constructor('gMonthDay')
def cast(value, tz=None):
    return GregorianMonthDay.fromstring(value, tz=tz)


@constructor('gYear')
def cast(value, tz=None):
    return GregorianYear.fromstring(value, tz=tz)


@constructor('gYearMonth')
def cast(value, tz=None):
    return GregorianYearMonth.fromstring(value, tz=tz)


@constructor('time')
def cast(value, tz=None):
    return Time.fromstring(value, tz=tz)


@method('dateTime')
@method('date')
@method('gDay')
@method('gMonth')
@method('gMonthDay')
@method('gYear')
@method('gYearMonth')
@method('time')
def evaluate(self, context=None):
    item = self.get_argument(context)
    if item is None:
        return []
    try:
        return self.cast(item, tz=None if context is None else context.timezone)
    except ValueError as err:
        raise self.error('FOCA0002', str(err))
    except TypeError as err:
        raise self.error('FORG0006', str(err))


###
# Constructors for time durations XSD types
@constructor('duration')
def cast(value):
    return Duration.fromstring(value)


@constructor('yearMonthDuration')
def cast(value):
    return YearMonthDuration.fromstring(value)


@constructor('dayTimeDuration')
def cast(value):
    return DayTimeDuration.fromstring(value)


###
# Constructors for binary XSD types
@constructor('base64Binary')
def cast(value, from_literal=False):
    if isinstance(value, UntypedAtomic):
        return codecs.encode(unicode_type(value), 'base64')
    elif not isinstance(value, (bytes, unicode_type)):
        raise xpath_error('FORG0006', 'the argument has an invalid type %r' % type(value))
    elif not isinstance(value, bytes) or from_literal:
        return codecs.encode(value.encode('ascii'), 'base64')
    elif HEX_BINARY_PATTERN.search(value.decode('utf-8')):
        value = codecs.decode(value, 'hex') if str is not bytes else value
        return codecs.encode(value, 'base64')
    elif NOT_BASE64_BINARY_PATTERN.search(value.decode('utf-8')):
        return codecs.encode(value, 'base64')
    else:
        return value


@constructor('hexBinary')
def cast(value, from_literal=False):
    if isinstance(value, UntypedAtomic):
        return codecs.encode(unicode_type(value), 'hex')
    elif not isinstance(value, (bytes, unicode_type)):
        raise xpath_error('FORG0006', 'the argument has an invalid type %r' % type(value))
    elif not isinstance(value, bytes) or from_literal:
        return codecs.encode(value.encode('ascii'), 'hex')
    elif HEX_BINARY_PATTERN.search(value.decode('utf-8')):
        return value if isinstance(value, bytes) or str is bytes else codecs.encode(value.encode('ascii'), 'hex')
    else:
        try:
            value = codecs.decode(value, 'base64')
        except ValueError:
            return codecs.encode(value, 'hex')
        else:
            return codecs.encode(value, 'hex')


@method('base64Binary')
@method('hexBinary')
def evaluate(self, context=None):
    item = self.get_argument(context)
    if item is None:
        return []
    try:
        return self.cast(item, self[0].label == 'literal')
    except ElementPathError as err:
        if err.token is None:
            err.token = self
        raise
    except ValueError as err:
        raise self.error('FOCA0002', str(err))
    except TypeError as err:
        raise self.error('FORG0006', str(err))


###
# Multi role-tokens cases
#

# Case 1: In XPath 2.0 the 'attribute' keyword is used both for attribute:: axis and
# attribute() node type function.
#
# First the XPath1 token class has to be removed from the XPath2 symbol table. Then the
# symbol has to be registered usually with the same binding power (bp --> lbp, rbp), a
# multi-value label (using a tuple of values) and a custom pattern. Finally a custom nud
# or led method is required.
unregister('attribute')
register('attribute', lbp=90, rbp=90, label=('function', 'axis'),
         pattern=r'\battribute(?=\s*\:\:|\s*\(\:.*\:\)\s*\:\:|\s*\(|\s*\(\:.*\:\)\()')


@method('attribute')
def nud(self):
    if self.parser.next_token.symbol == '::':
        self.parser.advance('::')
        self.parser.next_token.expected(
            '(name)', '*', 'text', 'node', 'document-node', 'comment', 'processing-instruction',
            'attribute', 'schema-attribute', 'element', 'schema-element'
        )
        self[:] = self.parser.expression(rbp=90),
        self.label = 'axis'
    else:
        self.parser.advance('(')
        if self.parser.next_token.symbol != ')':
            self[:] = self.parser.expression(5),
            if self.parser.next_token.symbol == ',':
                self.parser.advance(',')
                self[1:] = self.parser.expression(5),
        self.parser.advance(')')
        self.label = 'function'
    return self


@method('attribute')
def select(self, context=None):
    if context is None:
        return
    elif self.label == 'axis':
        for _ in context.iter_attributes():
            for result in self[0].select(context):
                yield result
    else:
        attribute_name = self[0].evaluate(context) if self else None
        for item in context.iter_attributes():
            if is_attribute_node(item, attribute_name):
                yield context.item[1]


@method('attribute')
def evaluate(self, context=None):
    if context is not None:
        if is_attribute_node(context.item, self[0].evaluate(context) if self else None):
            return context.item[1]


# Case 2: In XPath 2.0 the 'boolean' keyword is used both for boolean() function and
# for boolean() constructor.
def cast_to_boolean(value, context=None):
    if isinstance(value, bool):
        return value
    elif isinstance(value, (int, float, decimal.Decimal)):
        return bool(value)
    elif isinstance(value, UntypedAtomic):
        value = string_base_type(value)
    elif not isinstance(value, string_base_type):
        raise xpath_error('FORG0006', 'the argument has an invalid type %r' % type(value))

    if value in ('true', '1'):
        return True
    elif value in ('false', '0'):
        return False
    else:
        raise xpath_error('FOCA0002', "%r: not a boolean value" % value)


unregister('boolean')
register('boolean', lbp=90, rbp=90, label=('function', 'constructor'),
         pattern=r'\bboolean(?=\s*\(|\s*\(\:.*\:\)\()', cast=staticmethod(cast_to_boolean))


@method('boolean')
def nud(self):
    self.parser.advance('(')
    self[0:] = self.parser.expression(5),
    self.parser.advance(')')

    try:
        self.value = self.evaluate()  # Static context evaluation
    except ElementPathMissingContextError:
        self.value = None
    return self


@method('boolean')
def evaluate(self, context=None):
    if self.label == 'function':
        return boolean_value(self[0].get_results(context))

    # xs:boolean constructor
    item = self.get_argument(context)
    if item is None:
        return []
    try:
        return self.cast(item, context)
    except ElementPathError as err:
        err.token = self
        raise


# Case 3: In XPath 2.0 the 'string' keyword is used both for fn:string() and xs:string().
unregister('string')
register('string', lbp=90, rbp=90, label=('function', 'constructor'),
         pattern=r'\bstring(?=\s*\(|\s*\(\:.*\:\)\()', cast=staticmethod(lambda v, c=None: str(v)))


@method('string')
def nud(self):
    self.parser.advance('(')
    self[0:] = self.parser.expression(5),

    self.parser.advance(')')

    try:
        self.value = self.evaluate()  # Static context evaluation
    except ElementPathMissingContextError:
        self.value = None
    return self


@method('string')
def evaluate(self, context=None):
    if self.label == 'function':
        return string_value(self.get_argument(context))
    else:
        item = self.get_argument(context)
        return [] if item is None else str(item)


# Case 4: In XPath 2.0 the 'QName' keyword is used both for fn:QName() and xs:QName().
# In this case the label is set by the nud method, in dependence of the number of args.
def cast_to_qname(value, namespaces=None):
    if not isinstance(value, string_base_type):
        raise xpath_error('FORG0006', 'the argument has an invalid type %r' % type(value))

    match = QNAME_PATTERN.match(value)
    if match is None:
        raise xpath_error('FOCA0002', 'the argument must be an xs:QName')

    pfx = match.groupdict()['prefix'] or ''
    if pfx and (not namespaces or pfx not in namespaces):
        raise xpath_error('FONS0004', 'No namespace found for prefix %r' % pfx)
    return value


register('QName', lbp=90, rbp=90, label=('function', 'constructor'),
         pattern=r'\bQName(?=\s*\(|\s*\(\:.*\:\)\()', cast=staticmethod(cast_to_qname))


@method('QName')
def nud(self):
    self.parser.advance('(')
    self[0:] = self.parser.expression(5),
    if self.parser.next_token.symbol == ',':
        self.label = 'function'
        self.parser.advance(',')
        self[1:] = self.parser.expression(5),
    else:
        self.label = 'constructor'
    self.parser.advance(')')

    try:
        self.value = self.evaluate()  # Static context evaluation
    except ElementPathMissingContextError:
        self.value = None
    return self


@method('QName')
def evaluate(self, context=None):
    if self.label == 'constructor':
        item = self.get_argument(context)
        if item is None:
            return []
        try:
            return self.cast(item, self.parser.namespaces)
        except ElementPathError as err:
            if err.token is None:
                err.token = self
            raise
    else:
        uri = self.get_argument(context)
        if uri is None:
            uri = ''
        elif not isinstance(uri, string_base_type):
            raise self.error('FORG0006', '1st argument has an invalid type %r' % type(uri))

        qname = self[1].evaluate(context)
        if not isinstance(qname, string_base_type):
            raise self.error('FORG0006', '2nd argument has an invalid type %r' % type(qname))
        match = QNAME_PATTERN.match(qname)
        if match is None:
            raise self.error('FOCA0002', '2nd argument must be an xs:QName')

        pfx = match.groupdict()['prefix'] or ''
        if not uri:
            if pfx:
                raise self.error('FOCA0002', 'must be a local name when the parameter URI is empty')
        else:
            try:
                if uri != self.parser.namespaces[pfx]:
                    raise self.error('FOCA0002', 'prefix %r is already is used for another namespace' % pfx)
            except KeyError:
                self.parser.namespaces[pfx] = uri
        return qname


XPath2Parser.build_tokenizer()  # XPath 2.0 definitions completed, build the tokenizer.
