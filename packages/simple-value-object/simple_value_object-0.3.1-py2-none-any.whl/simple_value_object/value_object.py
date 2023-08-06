import six
import sys
from inspect import getargspec
import inspect

from .exceptions import NotDeclaredArgsException, ArgWithoutValueException,\
    CannotBeChangeException, ViolatedInvariantException,\
    InvariantReturnValueException

MIN_NUMBER_ARGS = 1


class ValueObject(object):

    def __new__(cls, *args, **kwargs):
        self = super(ValueObject, cls).__new__(cls)

        args_spec = ArgsSpec(self.__init__)

        def check_class_are_initialized():
            no_arguments_in_init_constructor = len(args_spec.args) <= MIN_NUMBER_ARGS
            if no_arguments_in_init_constructor:
                raise NotDeclaredArgsException()
            if None in args:
                raise ArgWithoutValueException()

        def assign_instance_arguments():
            assign_default_values(args_spec)
            override_default_values_with_args(args_spec)

        def assign_default_values(args_spec):
            defaults = () if not args_spec.defaults else args_spec.defaults
            self.__dict__.update(
                dict(zip(args_spec.args[:0:-1], defaults[::-1]))
            )

        def override_default_values_with_args(args_spec):
            self.__dict__.update(
                dict(list(zip(args_spec.args[1:], args)) + list(kwargs.items()))
            )

        def check_invariants():
            for invariant in obtain_invariants():
                if not invariant_execute(invariant):
                    raise ViolatedInvariantException(
                        'Args values {} violates invariant: {}'.format(
                            list(self.__dict__.values()), invariant
                        )
                    )

        def invariant_execute(invariant):
            return_value = invariant(self, self)

            if not isinstance(return_value, bool):
                raise InvariantReturnValueException()

            return return_value

        def is_invariant(method):
            try:
                return 'invariant_func_wrapper' in str(method) and '__init__' not in str(method)
            except TypeError:
                return False

        def obtain_invariants():
            invariants = [member[1] for member in inspect.getmembers(cls, is_invariant)]
            for invariant in invariants:
                yield(invariant)

        check_class_are_initialized()
        assign_instance_arguments()
        check_invariants()

        return self

    def __setattr__(self, name, value):
        raise CannotBeChangeException()

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        args_spec = ArgsSpec(self.__init__)
        args_values = []
        for arg in args_spec.args[1:]:
            value = getattr(self, arg)
            if isinstance(value, six.text_type):
                value = value.encode('utf-8')
            if isinstance(value, six.string_types) or isinstance(value, six.binary_type):
                value = value.decode('utf-8')
            if isinstance(value,ValueObject):
                if sys.version_info[0] < 3:
                    value = repr(value).decode('utf-8')
            args_values.append(u"{}={}".format(arg, value))

        kwargs = u", ".join(args_values)

        result = u"{}({})".format(self.__class__.__name__, kwargs)

        if sys.version_info[0] < 3:
            return result.encode('utf-8')

        return result

    def __hash__(self):
        return self.hash

    @property
    def hash(self):
        return hash(self.__repr__())


class ArgsSpec(object):

    def __init__(self, method):
        try:
            self._args, self._varargs, self._keywords, self._defaults = getargspec(method)
        except TypeError:
            raise NotDeclaredArgsException()

    @property
    def args(self):
        return self._args

    @property
    def varargs(self):
        return self._varargs

    @property
    def keywords(self):
        return self._keywords

    @property
    def defaults(self):
        return self._defaults
