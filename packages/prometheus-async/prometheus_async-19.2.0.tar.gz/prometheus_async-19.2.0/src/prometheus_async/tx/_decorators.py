# Copyright 2016 Hynek Schlawack
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Decorators for Twisted.
"""

from twisted.internet.defer import Deferred
from wrapt import decorator

from .._utils import get_time


def time(metric, deferred=None):
    r"""
    Call ``metric.observe(time)`` with runtime in seconds.

    Can be used as a decorator as well as on ``Deferred``\ s.

    Works with both sync and async results.

    :returns: function or ``Deferred``.
    """
    if deferred is None:

        @decorator
        def time_decorator(f, _, args, kw):
            def observe(value):
                metric.observe(get_time() - start_time)
                return value

            start_time = get_time()
            rv = f(*args, **kw)
            if isinstance(rv, Deferred):
                return rv.addBoth(observe)
            else:
                return observe(rv)

        return time_decorator
    else:

        def observe(value):
            metric.observe(get_time() - start_time)
            return value

        start_time = get_time()
        return deferred.addBoth(observe)


def count_exceptions(metric, deferred=None, exc=BaseException):
    """
    Call ``metric.inc()`` whenever *exc* is caught.

    Can be used as a decorator or on a ``Deferred``.

    :returns: function (if decorator) or ``Deferred``.
    """

    def inc(fail):
        fail.trap(exc)
        metric.inc()
        return fail

    if deferred is None:

        @decorator
        def count_exceptions_decorator(f, _, args, kw):
            try:
                rv = f(*args, **kw)
            except exc:
                metric.inc()
                raise

            if isinstance(rv, Deferred):
                return rv.addErrback(inc)
            else:
                return rv

        return count_exceptions_decorator
    else:
        return deferred.addErrback(inc)


def track_inprogress(metric, deferred=None):
    """
    Call ``metrics.inc()`` on entry and ``metric.dec()`` on exit.

    Can be used as a decorator or on a ``Deferred``.

    :returns: function (if decorator) or ``Deferred``.
    """

    def dec(rv):
        metric.dec()
        return rv

    if deferred is None:

        @decorator
        def track_inprogress_decorator(f, _, args, kw):
            metric.inc()
            try:
                rv = f(*args, **kw)
            finally:
                if isinstance(rv, Deferred):
                    return rv.addBoth(dec)
                else:
                    metric.dec()
                    return rv

        return track_inprogress_decorator
    else:
        metric.inc()
        return deferred.addBoth(dec)
