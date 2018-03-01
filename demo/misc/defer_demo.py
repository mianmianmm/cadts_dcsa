from twisted.internet.defer import Deferred


def callback1(result):
    print 'Callback 1 said: ', result
    return result


def callback2(result):
    print 'Callback 2 said: ', result
    return result


def callback3(result):
    print 'Callback 3 said: ', result
    raise Exception('Callback 3')


def errback1(result):
    print 'Errback 1 said: ', result
    return result


def errback2(result):
    raise Exception('Errback 2')


def errback3(result):
    print 'Errback 3 said: ', result
    return result


d = Deferred()
d.addCallback(callback1)
d.addCallback(callback2)
d.addCallback(callback3)

d.addErrback(errback3)

d.callback('Test')
