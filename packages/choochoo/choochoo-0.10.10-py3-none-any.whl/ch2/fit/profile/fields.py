
from collections import namedtuple
from itertools import repeat, zip_longest

from .support import Named
from ...lib.data import WarnDict

TIMESTAMP_GLOBAL_TYPE = 253


class ScaledField(Named):

    def __init__(self, log, name, units, scale, offset, accumulate):
        super().__init__(log, name)
        self._units = units
        self._scale = scale if scale else None  # treat 0 as none
        self._offset = offset
        self._accumulate = accumulate
        if accumulate:
            self._log.warning('Accumulation not supported for %s' % self.name)

    def _parse_and_scale(self, type, data, count, endian, timestamp, scale=None, offset=None, **options):
        values = type.parse_type(data, count, endian, timestamp, **options)
        if scale is None: scale = self._scale if self._scale else None
        if offset is None: offset = self._offset
        if scale is not None or offset is not None:
            if values is not None:
                if self._accumulate:
                    raise Exception('Accumulation not supported for %s' % self.name)
                if scale is None: scale = 1
                if offset is None: offset = 0
                if scale != 1 or offset != 0:  # keeps integer values integers
                    try:
                        values = tuple(value / scale - offset for value in values)
                    except Exception as e:
                        raise Exception('Error scaling %s: %s' % (self.name, e))
        yield self.name, (values, self._units)

    def post(self, message, types):
        '''
        Called after message creation.
        '''
        pass


class TypedField(ScaledField):

    def __init__(self, log, name, field_no, units, scale, offset, accumulate, field_type, types):
        super().__init__(log, name, units, scale, offset, accumulate)
        self.number = field_no
        if name in types.overrides:
            self._log.info('Overriding type for %s (not %s)' % (name, field_type))
            field_type = name
        self.type = types.profile_to_type(field_type)
        # if types.is_type(name):
        #     self.type = types.profile_to_type(name)
        #     log.warning('Overriding type (%s) for predefined %s' % (field_type, name))
        # else:
        #     self.type = types.profile_to_type(field_type)

    def parse_field(self, data, count, endian, timestamp, references, message, **options):
        yield from self._parse_and_scale(self.type, data, count, endian, timestamp, **options)


class RowField(TypedField):

    def __init__(self, log, row, types):
        super().__init__(log, row.field_name, row.single_int(log, row.field_no), row.units,
                         row.single_int(log, row.scale), row.single_int(log, row.offset),
                         row.single_int(log, row.accumulate), row.field_type, types)


class DelegateField(ScaledField):

    def parse_field(self, data, count, endian, timestamp, references, message, **options):
        # todo - do we need to worry about padding data?
        delegate = message.profile_to_field(self.name)
        yield from delegate.parse_field(data, count, endian, timestamp, references, message,
                                        scale=self._scale, offset=self._offset, **options)

    def size(self, message):
        delegate = message.profile_to_field(self.name)
        return delegate.type.size


class Zip:

    def _zip(self, *fields):
        return zip_longest(*(self.__split(field) for field in fields))

    def __split(self, field):
        if field:
            for value in str(field).split(','):
                yield value.strip()
        else:
            yield None


class CompositeField(Zip, TypedField):

    def __init__(self, log, row, types):
        super().__init__(log, row.field_name, row.single_int(log, row.field_no), row.units,
                         None, None, None, row.field_type, types)
        self.number = row.single_int(log, row.field_no)
        self.__components = []
        for (name, bits, units, scale, offset, accumulate) in \
                self._zip(row.components, row.bits, row.units, row.scale, row.offset, row.accumulate):
            self.__components.append((int(bits),
                                      # set scale / offset below because they seem to override delegate
                                      # (see intensity in CSV examples in SDK inside current_activity_type_intensity)
                                      DelegateField(log, name, units,
                                                    1 if scale is None else float(scale),
                                                    0 if offset is None else float(offset),
                                                    None if accumulate is None else int(accumulate))))

    def parse_field(self, data, count, endian, timestamp, references, message, rtn_composite=False, **options):
        if rtn_composite:
            yield (self.name, (('COMPOSITE',), self._units))
        byteorder = ['little', 'big'][endian]
        bits = int.from_bytes(data, byteorder=byteorder)
        for nbits, field in self.__components:
            nbytes = max((nbits+7) // 8, field.size(message))
            data = (bits & ((1 << nbits) - 1)).to_bytes(nbytes, byteorder=byteorder)
            bits >>= nbits
            yield from field.parse_field(data, 1, endian, timestamp, references, message,
                                         rtn_composite=rtn_composite, **options)


class DynamicField(Zip, RowField):

    def __init__(self, log, row, rows, types):
        super().__init__(log, row, types)
        self.__dynamic_lookup = WarnDict(log, 'No dynamic field for %r')
        self.references = []
        for row in rows.lookahead():
            if row and row.field_name and row.field_no is None:
                for name, value in self._zip(row.ref_name, row.ref_value):
                    # need to use a list (not set) to preserve order
                    # (and consistently disambiguate multiple matches)
                    if name not in self.references:
                        self.references.append(name)
                    self.__dynamic_lookup[(name, value)] = row.field_name
            else:
                break

    def post(self, message, types):
        # fill in values for when mapping is not used
        for (name, value), field in list(self.__dynamic_lookup.items()):
            value = types.profile_to_type(message.profile_to_field(name).type.name).profile_to_internal(value)
            self.__dynamic_lookup[(name, value)] = field

    def parse_field(self, data, count, endian, timestamp, references, message, warn=False, **options):
        for name in self.references:
            if name in references:
                lookup = (name, references[name][0][0])  # drop units and take first value
                if lookup in self.__dynamic_lookup:
                    yield from message.profile_to_field(self.__dynamic_lookup[lookup]).parse_field(
                        data, count, endian, timestamp, references, message, **options)
                    return
        if warn:
            self._log.warning('Could not resolve dynamic field %s' % self.name)
        yield from super().parse_field(data, count, endian, timestamp, references, message, warn=warn, **options)


def MessageField(log, row, rows, types):
    log.debug('Parsing field %s' % row.field_name)
    if row.components:
        return CompositeField(log, row, types)
    else:
        peek = rows.peek()
        if peek and peek.field_name and peek.field_no is None:
            return DynamicField(log, row, rows, types)
        else:
            return RowField(log, row, types)


class Row(namedtuple('BaseRow',
                     'msg_name, field_no, field_name, field_type, array, components, scale, offset, ' +
                     'units, bits, accumulate, ref_name, ref_value, comment, products, example')):

    __slots__ = ()

    def __new__(cls, row):
        return super().__new__(cls, *tuple(row)[0:16])

    def single_int(self, log, value):
        try:
            return None if value is None else int(value)
        except ValueError:
            log.warning('Cannot parse "%s" as a single integer', value)
            return None
