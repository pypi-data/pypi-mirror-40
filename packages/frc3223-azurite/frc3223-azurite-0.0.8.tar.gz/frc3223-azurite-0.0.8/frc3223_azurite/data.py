import csv
import numpy


def read_csv(fnom):
    """
    takes a csv file that consists of one header row and many data rows
    and reads it into a numpy array.

    :returns: dictionary mapping header text to column data
    """
    with open(fnom, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
    data = numpy.genfromtxt(fnom, delimiter=',', skip_header=1)
    assert len(headers) == data.shape[1]
    results = {}
    for i, header in enumerate(headers):
        results[header] = data[:, i]

    return results


def show_data(fnom, time_key='ts', 
        s_t=None, e_t=None,
        s=None, e=None, 
        value_keys=None, show_dt=True
        ):
    from matplotlib import pyplot as plt
    data = read_csv(fnom)
    assert s_t is None or s is None, "only one of s, s_t can be specified"
    assert e_t is None or e is None, "only one of e, e_t can be specified"

    if s_t is not None:
        s = numpy.argmax(data[time_key] >= s_t)
        print ("s_t=%s -> s=%s" % (s_t, s))
    elif s is None:
        s = 0
        print("s=%s" % (s,))
    if e_t is not None:
        e = numpy.argmin(data[time_key] <= e_t)
        print ("e_t=%s -> e=%s" % (e_t, e))
    elif e is None:
        e = len(data[time_key])
        print("e=%s" % (e,))

    value_keys = data.keys() if value_keys is None else value_keys
    ts = data[time_key][s:e]
    if show_dt:
        dts = ts[1:] - ts[:-1]
        plt.plot(ts[1:], dts)
        plt.ylabel("dt")
        plt.xlabel("t")
        plt.show()
    for key in value_keys:
        if key == time_key: continue

        values = data[key][s:e]
        plt.plot(ts, values)
        plt.xlabel(time_key)
        plt.ylabel(key)
        plt.show()

def _sg_filter(x, m, k=0):
    """
    x = Vector of sample times
    m = Order of the smoothing polynomial
    k = Which derivative
    """
    mid = len(x) // 2        
    a = x - x[mid]
    expa = lambda x: list(map(lambda i: i**x, a)  )  
    A = numpy.r_[list(map(expa, range(0,m+1)))].transpose()
    Ai = numpy.linalg.pinv(A)

    return Ai[k]

def sg_smooth(x, y, size=5, order=2, deriv=0):
    """
    smooth data with a savitzky golay filter
    """

    if deriv > order:
        raise Exception( "deriv must be <= order")

    n = len(x)
    m = size

    result = numpy.zeros(n)

    for i in range(m, n-m):
        start, end = i - m, i + m + 1
        f = _sg_filter(x[start:end], order, deriv)
        result[i] = numpy.dot(f, y[start:end])

    if deriv > 1:
        result *= math.factorial(deriv)

    return result
