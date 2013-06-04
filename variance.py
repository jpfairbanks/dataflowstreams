import math
import collections
import numpy as np
import numpy.random as rand
import scipy
import scipy.stats as stats
import matplotlib.pyplot as plt

class variance_state(object):
    """This object encapsulates the data necessary to maintain 
    a streaming variance estimator. This includes the sum, variance, count.
    You can put data into it which causes the state to update, and you can probe it for the answers
    to questions vs.mean(), vs.zscore(datum), vs.sigma()"""
    
    #sumhat
    #varhat
    #count
    def __init__(self):
        """start a state with no data. all parameters are set to 0.0 """
        self.sumhat = 0.0
        self.varhat = 0.0
        self.count  = 0.0
    def mean(self):
        """returns the estimated mean so far
        :returns: @todo

        """
        return self.sumhat/self.count
    def sigma(self):
        """Returns the sigma estimate
        :returns: @todo

        """
        return math.sqrt(self.varhat/self.count)

    def push(self, datum):
        """Pushes a datum into the structure updating the state.

        :datum: a number type
        :returns: the z-score of the datum

        """
        self.sumhat += datum
        self.count  += 1
        muhat = self.mean()
        self.varhat += (datum - muhat)**2
        z = 0
        sigma = self.sigma()
        if sigma != 0:
            z = (datum - muhat)/sigma
        return z

    def zscore(self, datum):
        """Gets the zscore of an element without updating the parameters.

        :datum: a number type
        :returns: the z-score of datum

        """
        z = 0
        sigma = self.sigma()
        if sigma() != 0:
            z = (datum - muhat)/sigma()
        return z

    def __repr__(self):
        """print this as a string
        :returns: @todo

        """
        return "sumhat:%f; varhat:%f, count:%f;"%(self.sumhat,self.varhat,self.count)

class normal_filter(object):
    """A filter that keeps elements that are within the normal range and rejects those outside. assuming a standard normal distribution
    Ask for its accept queue and reject queue.
    """

    def __init__(self, threshold=2):
        """@todo: to be defined """
        self.accept = collections.deque()
        self.reject = collections.deque()
        self.thresh = threshold

    def push(self, datum):
        """Push a datum through the filter

        :datum: expects a tuple of numbers, the [0] element is the data element and [1] is the zscore
        :returns: nothing

        """
        if abs(datum[1]) < self.thresh:
            self.accept.append(datum[0])
        else:
            self.reject.append(datum[0])
            #print(len(self.accept), datum)
            

def generate(nsamp, mean=0, var=1, outlier_frac=.1, outlier_mean=10):
    nin = nsamp*(1-outlier_frac)
    nout = nsamp - nin
    inlier  = rand.randn(nin)*var + mean
    #print(inlier)
    outlier = rand.randn(nout)*var + outlier_mean
    #print(outlier)
    return np.hstack([inlier, outlier])

def shuffle(a):
    p = rand.permutation(len(a))
    shuffled = a[p]
    #print(a, shuffled)
    return shuffled

def streaming_zscore(a, initial_data=None):
    """Computes the running zscore of each element. 

    :a: the data
    :returns: zarray  an array of zscores computed online

    """
    nsamp = len(a)
    if initial_data == None:
        vs = variance_state()
    else:
        vs = initial_data
    zarray = np.zeros(nsamp)
    #print(zarray)
    #print(a)
    for i, x in enumerate(a):
        #print(i,x)
        zarray[i] = vs.push(x)
    #print(zarray)
    return zarray, vs

def apply_round(data, state):
    """Take the data and do streaming zscore and apply the normal filter

    :data: the stream of numbers
    :state: the state of the last round
    :returns: the stream of accepted numbers and the state of the variance estimator

    """
    zarray, state = streaming_zscore(data, state)
    nf = normal_filter(3.0)
    for datum in zip(data, zarray):
        nf.push(datum)
    rejects = nf.reject
    graduates = nf.accept
    if len(rejects) != 0 :
        print("the min/max of accepted data")
        #print(np.min(nf.accept), np.max(nf.accept))
        print("the min/max of rejected data")
        #print(np.min(nf.reject), np.max(nf.reject))
        print("this round outliers found: %d" % len(nf.reject))
        #print(rejects)
    return graduates, state

def main():
    nsamp  = 200000
    a = generate(nsamp, outlier_mean=15, outlier_frac=.10)
    a = shuffle(a)
    print(a)
    plt.hist(a)
    #begin looping
    i = 1
    num_old_grads = nsamp+1
    graduates = a
    #while len(graduates) < num_old_grads:
    while i < 5:
        num_old_grads = len(graduates)
        print("round %d" % i)
        i+=1
        graduates, state = apply_round(graduates, None)
        print(state)
        plt.hist(graduates, color='g', alpha=.3 )
if __name__ == '__main__':
    main()
