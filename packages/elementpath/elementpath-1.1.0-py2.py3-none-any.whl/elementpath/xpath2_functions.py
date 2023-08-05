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
XPath 2.0 implementation - part 2 (functions)
"""
import sys
import decimal
import math
import datetime
import time
import re
import locale
import unicodedata

from .compat import PY3, string_base_type, unicode_chr, urllib_quote, unicode_type
from .datatypes import DateTime, Date, Time, Timezone, Duration, DayTimeDuration
from .namespaces import prefixed_to_qname, get_namespace
from .xpath_helpers import is_document_node, is_xpath_node, is_element_node, is_attribute_node, \
    node_name, node_string_value, node_nilled, node_base_uri, node_document_uri, data_value, string_value

from .xpath2_parser import XPath2Parser
method = XPath2Parser.method
function = XPath2Parser.function

###
# Regex compiled patterns for functions and XSD constructors
WHITESPACES_RE_PATTERN = re.compile(r'\s+')
NMTOKEN_PATTERN = re.compile(r'^[\w.\-:]+$', flags=0 if PY3 else re.U)
NAME_PATTERN = re.compile(r'^(?:[^\d\W]|:)[\w.\-:]*$', flags=0 if PY3 else re.U)
NCNAME_PATTERN = re.compile(r'^[^\d\W][\w.\-]*$', flags=0 if PY3 else re.U)
QNAME_PATTERN = re.compile(
    r'^(?:(?P<prefix>[^\d\W][\w.-]*):)?(?P<local>[^\d\W][\w.-]*)$', flags=0 if PY3 else re.U
)
HEX_BINARY_PATTERN = re.compile(r'^[0-9a-fA-F]+$')
NOT_BASE64_BINARY_PATTERN = re.compile(r'[^0-9a-zA-z+/= \t\n]')
LANGUAGE_CODE_PATTERN = re.compile(r'^([a-zA-Z]{2}|[iI]-[a-zA-Z]+|[xX]-[a-zA-Z]{1,8})(-[a-zA-Z]{1,8})*$')
WRONG_ESCAPE_PATTERN = re.compile(r'%(?![a-eA-E\d]{2})')
WRONG_REPLACEMENT_PATTERN = re.compile(r'(?<!\\)\$([^\d]|$)|((?<=[^\\])|^)\\([^$]|$)|\\\\\$')


###
# Node types
@method(function('document-node', nargs=(0, 1)))
def evaluate(self, context=None):
    if context is not None:
        if context.item is None and is_document_node(context.root):
            if not self:
                return context.root
            elif is_element_node(context.root.getroot(), self[0].evaluate(context)):
                return context.root


@method(function('element', nargs=(0, 2)))
def evaluate(self, context=None):
    if context is not None:
        if not self:
            if is_element_node(context.item):
                return context.item
        elif is_element_node(context.item, self[1].evaluate(context)):
            return context.item


@method(function('schema-attribute', nargs=1))
def evaluate(self, context=None):
    attribute_name = self[0].source
    qname = prefixed_to_qname(attribute_name, self.parser.namespaces)
    if self.parser.schema.get_attribute(qname) is None:
        self.missing_name("attribute %r not found in schema" % attribute_name)

    if context is not None:
        if is_attribute_node(context.item, qname):
            return context.item


@method(function('schema-element', nargs=1))
def evaluate(self, context=None):
    element_name = self[0].source
    qname = prefixed_to_qname(element_name, self.parser.namespaces)
    if self.parser.schema.get_element(qname) is None \
            and self.parser.schema.get_substitution_group(qname) is None:
        self.missing_name("element %r not found in schema" % element_name)

    if context is not None:
        if is_element_node(context.item) and context.item.tag == qname:
            return context.item


@method(function('empty-sequence', nargs=0))
def evaluate(self, context=None):
    if context is not None:
        return isinstance(context.item, list) and not context.item


@method('document-node')
@method('element')
@method('schema-attribute')
@method('schema-element')
@method('empty-sequence')
def select(self, context=None):
    if context is not None:
        for _ in context.iter_children_or_self():
            item = self.evaluate(context)
            if item is not None:
                yield item


###
# Function for QNames
@method(function('prefix-from-QName', nargs=1))
def evaluate(self, context=None):
    qname = self.get_argument(context)
    if qname is None:
        return []
    elif not isinstance(qname, string_base_type):
        raise self.error('FORG0006', 'argument has an invalid type %r' % type(qname))
    match = QNAME_PATTERN.match(qname)
    if match is None:
        raise self.error('FOCA0002', 'argument must be an xs:QName')
    return match.groupdict()['prefix'] or []


@method(function('local-name-from-QName', nargs=1))
def evaluate(self, context=None):
    qname = self.get_argument(context)
    if qname is None:
        return []
    elif not isinstance(qname, string_base_type):
        raise self.error('FORG0006', 'argument has an invalid type %r' % type(qname))
    match = QNAME_PATTERN.match(qname)
    if match is None:
        raise self.error('FOCA0002', 'argument must be an xs:QName')
    return match.groupdict()['local']


@method(function('namespace-uri-from-QName', nargs=1))
def evaluate(self, context=None):
    qname = self.get_argument(context)
    if qname is None:
        return []
    elif not isinstance(qname, string_base_type):
        raise self.error('FORG0006', 'argument has an invalid type %r' % type(qname))
    elif not qname:
        return ''

    match = QNAME_PATTERN.match(qname)
    if match is None:
        raise self.error('FOCA0002', 'argument must be an xs:QName')
    try:
        return self.parser.namespaces[match.groupdict()['prefix'] or '']
    except KeyError as err:
        raise self.error('FONS0004', 'No namespace found for prefix %s' % str(err))


@method(function('namespace-uri-for-prefix', nargs=2))
def evaluate(self, context=None):
    if context is not None:
        pfx = self.get_argument(context.copy())
        if pfx is None:
            pfx = ''
        if not isinstance(pfx, string_base_type):
            raise self.error('FORG0006', '1st argument has an invalid type %r' % type(pfx))

        elem = self.get_argument(context, index=1)
        if not is_element_node(elem):
            raise self.error('FORG0006', '2nd argument %r is not a node' % elem)
        ns_uris = {get_namespace(e.tag) for e in elem.iter()}
        for p, uri in self.parser.namespaces.items():
            if uri in ns_uris:
                if p == pfx:
                    return uri
        return []


@method(function('in-scope-prefixes', nargs=1))
def select(self, context=None):
    if context is not None:
        elem = self.get_argument(context)
        if not is_element_node(elem):
            raise self.error('FORG0006', 'argument %r is not a node' % elem)
        for e in elem.iter():
            tag_ns = get_namespace(e.tag)
            for pfx, uri in self.parser.namespaces.items():
                if uri == tag_ns:
                    yield pfx


@method(function('resolve-QName', nargs=2))
def evaluate(self, context=None):
    if context is not None:
        qname = self.get_argument(context.copy())
        if qname is None:
            return []
        if not isinstance(qname, string_base_type):
            raise self.error('FORG0006', '1st argument has an invalid type %r' % type(qname))
        match = QNAME_PATTERN.match(qname)
        if match is None:
            raise self.error('FOCA0002', '1st argument must be an xs:QName')
        pfx = match.groupdict()['prefix'] or ''

        elem = self.get_argument(context, index=1)
        if not is_element_node(elem):
            raise self.error('FORG0006', '2nd argument %r is not a node' % elem)
        ns_uris = {get_namespace(e.tag) for e in elem.iter()}
        for p, uri in self.parser.namespaces.items():
            if uri in ns_uris:
                if p == pfx:
                    return '{%s}%s' % (uri, match.groupdict()['local']) if uri else match.groupdict()['local']
        raise self.error('FONS0004', 'No namespace found for prefix %r' % pfx)


###
# Context item
@method(function('item', nargs=0))
def evaluate(self, context=None):
    if context is None:
        return
    elif context.item is None:
        return context.root
    else:
        return context.item


###
# Accessor functions
@method(function('node-name', nargs=1))
def evaluate(self, context=None):
    return node_name(self.get_argument(context))


@method(function('nilled', nargs=1))
def evaluate(self, context=None):
    return node_nilled(self.get_argument(context))


@method(function('data', nargs=1))
def select(self, context=None):
    for item in self[0].select(context):
        value = data_value(item)
        if value is None:
            raise self.error('FOTY0012', "argument node does not have a typed value: %r" % item)
        else:
            yield value


@method(function('base-uri', nargs=(0, 1)))
def evaluate(self, context=None):
    item = self.get_argument(context)
    if item is None:
        self.missing_context("context item is undefined")
    elif not is_xpath_node(item):
        self.wrong_context_type("context item is not a node")
    else:
        return node_base_uri


@method(function('document-uri', nargs=1))
def evaluate(self, context=None):
    return node_document_uri(self.get_argument(context))


###
# Number functions
@method(function('round-half-to-even', nargs=(1, 2)))
def evaluate(self, context=None):
    item = self.get_argument(context)
    try:
        precision = 0 if len(self) < 2 else self[1].evaluate(context)
        if PY3 or precision < 0:
            value = round(decimal.Decimal(item), precision)
        else:
            number = decimal.Decimal(item)
            exp = decimal.Decimal('1' if not precision else '.%s1' % ('0' * (precision - 1)))
            value = float(number.quantize(exp, rounding='ROUND_HALF_EVEN'))
    except TypeError as err:
        if item is not None and not isinstance(item, list):
            self.wrong_type(str(err))
    except decimal.DecimalException as err:
        if item is not None and not isinstance(item, list):
            self.wrong_value(str(err))
    else:
        return float(value)


@method(function('abs', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context)
    try:
        return abs(node_string_value(item) if is_xpath_node(item) else item)
    except TypeError:
        return float('nan')


###
# Aggregate functions
@method(function('avg', nargs=1))
def evaluate(self, context=None):
    result = list(self[0].select(context))
    if not result:
        return result
    elif isinstance(result[0], Duration):
        value = result[0]
        try:
            for item in result[1:]:
                value = value + item
            return value / len(result)
        except TypeError as err:
            self.wrong_type(str(err))
    else:
        try:
            return sum(result) / len(result)
        except TypeError as err:
            self.wrong_type(str(err))


@method(function('max', nargs=(1, 2)))
def evaluate(self, context=None):
    locale.setlocale(locale.LC_ALL, '')
    default_locale = locale.getlocale()
    if len(self) > 1:
        collation = self.get_argument(context, 1)
        try:
            locale.setlocale(locale.LC_ALL, collation)
        except locale.Error as err:
            self.wrong_value(str(err) + ' ' + repr(collation))

    try:
        value = max(self[0].select(context))
    except TypeError as err:
        self.wrong_type(str(err))
    else:
        locale.setlocale(locale.LC_ALL, default_locale)
        return value


@method(function('min', nargs=(1, 2)))
def evaluate(self, context=None):
    locale.setlocale(locale.LC_ALL, '')
    default_locale = locale.getlocale()
    if len(self) > 1:
        collation = self.get_argument(context, 1)
        try:
            locale.setlocale(locale.LC_ALL, collation)
        except locale.Error as err:
            self.wrong_value(str(err) + ' ' + repr(collation))

    try:
        value = min(self[0].select(context))
    except TypeError as err:
        self.wrong_type(str(err))
    else:
        locale.setlocale(locale.LC_ALL, default_locale)
        return value


###
# General functions for sequences
@method(function('empty', nargs=1))
@method(function('exists', nargs=1))
def evaluate(self, context=None):
    return next(iter(self.select(context)))


@method('empty')
def select(self, context=None):
    try:
        next(iter(self[0].select(context)))
    except StopIteration:
        yield True
    else:
        yield False


@method('exists')
def select(self, context=None):
    try:
        next(iter(self[0].select(context)))
    except StopIteration:
        yield False
    else:
        yield True


@method(function('distinct-values', nargs=(1, 2)))
def select(self, context=None):
    nan = False
    results = []
    for item in self[0].select(context):
        value = data_value(item)
        if context is not None:
            context.item = value
        if not nan and isinstance(value, float) and math.isnan(value):
            yield value
            nan = True
        elif value not in results:
            yield value
            results.append(value)


@method(function('insert-before', nargs=3))
def select(self, context=None):
    insert_at_pos = max(0, self[1].value - 1)
    inserted = False
    for pos, result in enumerate(self[0].select(context)):
        if not inserted and pos == insert_at_pos:
            for item in self[2].select(context):
                yield item
            inserted = True
        yield result

    if not inserted:
        for item in self[2].select(context):
            yield item


@method(function('index-of', nargs=(1, 3)))
def select(self, context=None):
    value = self[1].evaluate(context)
    for pos, result in enumerate(self[0].select(context)):
        if result == value:
            yield pos + 1


@method(function('remove', nargs=2))
def select(self, context=None):
    target = self[1].evaluate(context) - 1
    for pos, result in enumerate(self[0].select(context)):
        if pos != target:
            yield result


@method(function('reverse', nargs=1))
def select(self, context=None):
    for result in reversed(list(self[0].select(context))):
        yield result


@method(function('subsequence', nargs=(2, 3)))
def select(self, context=None):
    starting_loc = self[1].evaluate(context) - 1
    length = self[2].evaluate(context) if len(self) >= 3 else 0
    for pos, result in enumerate(self[0].select(context)):
        if starting_loc <= pos and (not length or pos < starting_loc + length):
            yield result


@method(function('unordered', nargs=1))
def select(self, context=None):
    for result in sorted(list(self[0].select(context)), key=lambda x: string_value(x)):
        yield result


###
# Cardinality functions for sequences
@method(function('zero-or-one', nargs=1))
def select(self, context=None):
    results = iter(self[0].select(context))
    try:
        item = next(results)
    except StopIteration:
        return

    try:
        next(results)
    except StopIteration:
        yield item
    else:
        raise self.error('FORG0003')


@method(function('one-or-more', nargs=1))
def select(self, context=None):
    results = iter(self[0].select(context))
    try:
        item = next(results)
    except StopIteration:
        raise self.error('FORG0004')
    else:
        yield item
        while True:
            try:
                yield next(results)
            except StopIteration:
                break


@method(function('exactly-one', nargs=1))
def select(self, context=None):
    results = iter(self[0].select(context))
    try:
        item = next(results)
    except StopIteration:
        raise self.error('FORG0005')
    else:
        try:
            next(results)
        except StopIteration:
            yield item
        else:
            raise self.error('FORG0005')


###
# Regex
@method(function('matches', nargs=(2, 3)))
def evaluate(self, context=None):
    input_string = self.get_argument(context, cls=string_base_type)
    pattern = self.get_argument(context, 1, required=True, cls=string_base_type)
    flags = 0
    if len(self) > 2:
        for c in self.get_argument(context, 2, required=True, cls=string_base_type):
            if c in 'smix':
                flags |= getattr(re, c.upper())
            else:
                raise self.error('FORX0001', "Invalid regular expression flag %r" % c)

    if input_string is None:
        input_string = ''

    try:
        return re.search(pattern, input_string, flags=flags) is not None
    except re.error:
        raise self.error('FORX0002', "Invalid regular expression %r" % pattern)  # TODO: full XML regex syntax


@method(function('replace', nargs=(3, 4)))
def evaluate(self, context=None):
    input_string = self.get_argument(context, cls=string_base_type)
    pattern = self.get_argument(context, 1, required=True, cls=string_base_type)
    replacement = self.get_argument(context, 2, required=True, cls=string_base_type)
    flags = 0
    if len(self) > 3:
        for c in self.get_argument(context, 3, required=True, cls=string_base_type):
            if c in 'smix':
                flags |= getattr(re, c.upper())
            else:
                raise self.error('FORX0001', "Invalid regular expression flag %r" % c)

    if input_string is None:
        input_string = ''

    try:
        pattern = re.compile(pattern, flags=flags)
    except re.error:
        raise self.error('FORX0002', "Invalid regular expression %r" % pattern)  # TODO: full XML regex syntax
    else:
        if pattern.search(''):
            raise self.error('FORX0003', "Regular expression %r matches zero-length string" % pattern.pattern)
        elif WRONG_REPLACEMENT_PATTERN.search(replacement):
            raise self.error('FORX0004', "Invalid replacement string %r" % replacement)
        else:
            if sys.version_info >= (3, 5):
                for g in range(pattern.groups + 1):
                    if '$%d' % g in replacement:
                        replacement = re.sub(r'(?<!\\)\$%d' % g, r'\\g<%d>' % g, replacement)
            else:
                match = pattern.search(input_string)
                for g in range(pattern.groups + 1):
                    if '$%d' % g in replacement:
                        if match and match.group(g) is not None:
                            replacement = re.sub(r'(?<!\\)\$%d' % g, r'\\g<%d>' % g, replacement)
                        else:
                            replacement = re.sub(r'(?<!\\)\$%d' % g, '', replacement)

        return pattern.sub(replacement, input_string)


@method(function('tokenize', nargs=(2, 3)))
def select(self, context=None):
    input_string = self.get_argument(context, cls=string_base_type)
    pattern = self.get_argument(context, 1, required=True, cls=string_base_type)
    flags = 0
    if len(self) > 2:
        for c in self.get_argument(context, 2, required=True, cls=string_base_type):
            if c in 'smix':
                flags |= getattr(re, c.upper())
            else:
                raise self.error('FORX0001', "Invalid regular expression flag %r" % c)

    try:
        pattern = re.compile(pattern, flags=flags)
    except re.error:
        raise self.error('FORX0002', "Invalid regular expression %r" % pattern)
    else:
        if pattern.search(''):
            raise self.error('FORX0003', "Regular expression %r matches zero-length string" % pattern.pattern)

    if input_string:
        for value in pattern.split(input_string):
            if value is not None and pattern.search(value) is None:
                yield value


###
# String functions
@method(function('codepoints-to-string', nargs=1))
def evaluate(self, context=None):
    return ''.join(unicode_chr(cp) for cp in self[0].select(context))


@method(function('string-to-codepoints', nargs=1))
def select(self, context=None):
    for char in self[0].evaluate(context):
        yield ord(char)


@method(function('compare', nargs=(2, 3)))
def evaluate(self, context=None):
    comp1 = self.get_argument(context, 0, cls=string_base_type)
    comp2 = self.get_argument(context, 1, cls=string_base_type)
    if comp1 is None or comp2 is None:
        return []

    locale.setlocale(locale.LC_ALL, '')
    if len(self) < 3:
        value = locale.strcoll(comp1, comp2)
    else:
        collation = self.get_argument(context, 2)
        default_locale = locale.getlocale()
        try:
            locale.setlocale(locale.LC_ALL, collation)
        except locale.Error as err:
            self.wrong_value(str(err) + ' ' + repr(collation))
        value = locale.strcoll(comp1, comp2)
        locale.setlocale(locale.LC_ALL, default_locale)

    return 1 if value > 0 else -1 if value < 0 else 0


@method(function('codepoint-equal', nargs=2))
def evaluate(self, context=None):
    comp1 = self.get_argument(context, 0, cls=string_base_type)
    comp2 = self.get_argument(context, 1, cls=string_base_type)
    if comp1 is None or comp2 is None:
        return []
    elif len(comp1) != len(comp2):
        return False
    else:
        return all(ord(c1) == ord(c2) for c1, c2 in zip(comp1, comp2))


@method(function('string-join', nargs=2))
def evaluate(self, context=None):
    try:
        return self[1].evaluate(context).join(s for s in self[0].select(context))
    except AttributeError as err:
        self.wrong_type("the separator must be a string: %s" % err)
    except TypeError as err:
        self.wrong_type("the values must be strings: %s" % err)


@method(function('normalize-unicode', nargs=(1, 2)))
def evaluate(self, context=None):
    arg = self.get_argument(context, cls=string_base_type)
    if len(self) > 1:
        normalization_form = self.get_argument(context, 1, cls=string_base_type)
        if normalization_form is None:
            self.wrong_type("2nd argument can't be an empty sequence")
        else:
            normalization_form = normalization_form.strip().upper()
    else:
        normalization_form = 'NFC'

    if normalization_form == 'FULLY-NORMALIZED':
        raise NotImplementedError("%r normalization form not supported" % normalization_form)
    if arg is None:
        return ''
    elif not isinstance(arg, unicode_type):
        arg = arg.decode('utf-8')

    try:
        return unicodedata.normalize(normalization_form, arg)
    except ValueError:
        raise self.error('FOCH0003', "unsupported normalization form %r" % normalization_form)


@method(function('upper-case', nargs=1))
def evaluate(self, context=None):
    arg = self.get_argument(context)
    try:
        return '' if arg is None else arg.upper()
    except AttributeError:
        self.wrong_type("the argument must be a string: %r" % arg)


@method(function('lower-case', nargs=1))
def evaluate(self, context=None):
    arg = self.get_argument(context)
    try:
        return '' if arg is None else arg.lower()
    except AttributeError:
        self.wrong_type("the argument must be a string: %r" % arg)


@method(function('encode-for-uri', nargs=1))
def evaluate(self, context=None):
    uri_part = self.get_argument(context)
    try:
        return '' if uri_part is None else urllib_quote(uri_part, safe='~')
    except TypeError:
        self.wrong_type("the argument must be a string: %r" % uri_part)


@method(function('iri-to-uri', nargs=1))
def evaluate(self, context=None):
    iri = self.get_argument(context)
    try:
        return '' if iri is None else urllib_quote(iri, safe='-_.!~*\'()#;/?:@&=+$,[]%')
    except TypeError:
        self.wrong_type("the argument must be a string: %r" % iri)


@method(function('escape-html-uri', nargs=1))
def evaluate(self, context=None):
    uri = self.get_argument(context)
    try:
        return '' if uri is None else urllib_quote(uri, safe=''.join(chr(cp) for cp in range(32, 127)))
    except TypeError:
        self.wrong_type("the argument must be a string: %r" % uri)


@method(function('starts-with', nargs=(2, 3)))
def evaluate(self, context=None):
    arg1 = self.get_argument(context)
    arg2 = self.get_argument(context, index=1)
    try:
        return arg1.startswith(arg2)
    except TypeError:
        self.wrong_type("the arguments must be a string")


@method(function('ends-with', nargs=(2, 3)))
def evaluate(self, context=None):
    arg1 = self.get_argument(context)
    arg2 = self.get_argument(context, index=1)
    try:
        return arg1.endswith(arg2)
    except TypeError:
        self.wrong_type("the arguments must be a string")


###
# Functions on durations, dates and times
@method(function('years-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.months // 12 if item.months >= 0 else -(abs(item.months) // 12)


@method(function('months-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.months % 12 if item.months >= 0 else -(abs(item.months) % 12)


@method(function('days-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.seconds // 86400 if item.seconds >= 0 else -(abs(item.seconds) // 86400)


@method(function('hours-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.seconds // 3600 % 24 if item.seconds >= 0 else -(abs(item.seconds) // 3600 % 24)


@method(function('minutes-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.seconds // 60 % 60 if item.seconds >= 0 else -(abs(item.seconds) // 60 % 60)


@method(function('seconds-from-duration', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Duration)
    if item is None:
        return []
    else:
        return item.seconds % 60 if item.seconds >= 0 else -(abs(item.seconds) % 60)


@method(function('year-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else -(item.dt.year + 1) if item.bce else item.dt.year


@method(function('month-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else item.dt.month


@method(function('day-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else item.dt.day


@method(function('hours-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else item.dt.hour


@method(function('minutes-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else item.dt.minute


@method(function('seconds-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else item.dt.second


@method(function('timezone-from-dateTime', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=DateTime)
    return [] if item is None else DayTimeDuration(seconds=item.tzinfo.offset.total_seconds())


@method(function('year-from-date', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Date)
    return [] if item is None else item.year


@method(function('month-from-date', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Date)
    return [] if item is None else item.month


@method(function('day-from-date', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Date)
    return [] if item is None else item.day


@method(function('timezone-from-date', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Date)
    return [] if item is None else DayTimeDuration(seconds=item.tzinfo.offset.total_seconds())


@method(function('hours-from-time', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Time)
    return [] if item is None else item.hour


@method(function('minutes-from-time', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Time)
    return [] if item is None else item.minute


@method(function('seconds-from-time', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Time)
    return [] if item is None else item.second + item.microsecond / 1000000.0


@method(function('timezone-from-time', nargs=1))
def evaluate(self, context=None):
    item = self.get_argument(context, cls=Time)
    return [] if item is None else DayTimeDuration(seconds=item.tzinfo.offset.total_seconds())


###
# Timezone adjustment functions
@method(function('adjust-dateTime-to-timezone', nargs=(1, 2)))
def evaluate(self, context=None):
    return self.adjust_datetime(context, DateTime)


@method(function('adjust-date-to-timezone', nargs=(1, 2)))
def evaluate(self, context=None):
    return self.adjust_datetime(context, Date)


@method(function('adjust-time-to-timezone', nargs=(1, 2)))
def evaluate(self, context=None):
    return self.adjust_datetime(context, Time)


###
# Context functions
@method(function('current-dateTime', nargs=0))
def evaluate(self, context=None):
    if context is None:
        return DateTime(datetime.datetime.now())
    else:
        return DateTime(context.current_dt)


@method(function('current-date', nargs=0))
def evaluate(self, context=None):
    if context is None:
        return Date(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    else:
        return Date(context.current_dt.replace(hour=0, minute=0, second=0, microsecond=0))


@method(function('current-time', nargs=0))
def evaluate(self, context=None):
    if context is None:
        return Time(datetime.datetime.now().replace(year=1900, month=1, day=1))
    else:
        return Time(context.current_dt.replace(year=1900, month=1, day=1))


@method(function('implicit-timezone', nargs=0))
def evaluate(self, context=None):
    if context is not None and context.timezone is not None:
        return context.timezone
    else:
        return Timezone(datetime.timedelta(seconds=time.timezone))


###
# The root function (Ref: https://www.w3.org/TR/2010/REC-xpath-functions-20101214/#func-root)
@method(function('root', nargs=(0, 1)))
def evaluate(self, context=None):
    if self:
        item = self.get_argument(context)
    elif context is None:
        raise self.error('XPDY0002')
    else:
        item = context.item

    if item is None:
        return []
    elif is_xpath_node(item):
        return item
    else:
        raise self.error('XPTY0004')


###
# The error function (Ref: https://www.w3.org/TR/xpath20/#func-error)
@method(function('error', nargs=(0, 3)))
def evaluate(self, context=None):
    if not self:
        raise self.error('FOER0000')
    elif len(self) == 1:
        item = self.get_argument(context)
        raise self.error(item or 'FOER0000')


# XPath 2.0 definitions continue into module xpath2_constructors