#!/usr/bin/python2.3

from twisted.internet import defer
from twisted.python import failure, util

"""
this example is analagous to a function calling .errback(failure)
"""


class Counter(object):
    num = 0

def handleFailure(f):
    print "errback"
    print "we got an exception: %s" % (f.getTraceback(),)
    f.trap(RuntimeError)

def handleResult(result):
    Counter.num += 1
    print "callback %s" % (Counter.num,)
    print "\tgot result: %s" % (result,)
    return "yay! handleResult was successful!"

def failAtHandlingResult(result):
    Counter.num += 1
    print "callback %s" % (Counter.num,)
    print "\tgot result: %s" % (result,)
    print "\tabout to raise exception"
    raise RuntimeError, "whoops! we encountered an error"


def nonDeferredExample(result):
    if not isinstance(result, failure.Failure): 
        try:
            result = handleResult(result)
        except:
            result = failure.Failure()
    else:
        pass


    if not isinstance(result, failure.Failure): 
        pass
    else:
        try:
            result = handleFailure(result)
        except:
            result = failure.Failure()


def deferredExample(result):
    d = defer.Deferred()
    d.addCallback(handleResult)
    d.addCallback(failAtHandlingResult)
    d.addErrback(handleFailure)

    d.errback(result)


if __name__ == '__main__':
    result = None
    try:
        raise RuntimeError, "*doh*! failure!"
    except:
        result = failure.Failure()
    nonDeferredExample(result)
    print "\n-------------------------------------------------\n"
    Counter.num = 0
    deferredExample(result)
