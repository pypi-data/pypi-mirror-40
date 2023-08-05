# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
import numpy as np
from itertools import islice, chain
import scipy.stats
import random
import math

def accuracy(predicted,ground_truth):
    """calculates accuracy given ground truth and predicted labels"""
    num_correct = np.sum(np.asarray(predicted) == np.asarray(ground_truth))
    return float(num_correct) / len(predicted)

def confidence_99(data):
    """returns the 99% confidence mean and deviation for the given
        distribution

    Args:
        data(array-like): data to find the confidence interval for,
            in machine learning applications, this is usually accuracy
            for K-fold cross validation

    Returns:
        float: the mean for this distributions
        float: +/- deviation for this confidence interval

    Example:
        >>> import numpy as np
        >>> import imagepypelines as ip
        >>> # create sample test 'accuracies' from a normal distribution
        >>> # mean accuracy is 75%, std is 10% for this example
        >>> accuracies = np.random.normal(.75, .1, 1000)
        >>> # get 99% confidence interval
        >>> mean, error = ip.confidence_99(accuracies)
    """
    return confidence(data,.99)

def confidence_95(data):
    """returns the 95% confidence mean and deviation for the given
        distribution

    Args:
        data(array-like): data to find the confidence interval for,
            in machine learning applications, this is usually accuracy
            for K-fold cross validation

    Returns:
        float: the mean for this distributions
        float: +/- deviation for this confidence interval

    Example:
        >>> import numpy as np
        >>> import imagepypelines as ip
        >>> # create sample test 'accuracies' from a normal distribution
        >>> # mean accuracy is 75%, std is 10% for this example
        >>> accuracies = np.random.normal(.75, .1, 1000)
        >>> # get 95% confidence interval
        >>> mean, error = ip.confidence_95(accuracies)
    """
    return confidence(data,.95)

def confidence_90(data):
    """returns the 90% confidence mean and deviation for the given
        distribution

    Args:
        data(array-like): data to find the confidence interval for,
            in machine learning applications, this is usually accuracy
            for K-fold cross validation

    Returns:
        float: the mean for this distributions
        float: +/- deviation for this confidence interval

    Example:
        >>> import numpy as np
        >>> import imagepypelines as ip
        >>> # create sample test 'accuracies' from a normal distribution
        >>> # mean accuracy is 75%, std is 10% for this example
        >>> accuracies = np.random.normal(.75, .1, 1000)
        >>> # get 90% confidence interval
        >>> mean, error = ip.confidence_90(accuracies)
    """
    return confidence(data,.90)


def confidence(data, confidence=0.95):
    """returns the confidence mean and deviation for the given
        confidence interval

    Args:
        data(array-like): data to find the confidence interval for,
            in machine learning applications, this is usually accuracy
            for K-fold cross validation
        confidence(float): confidence interval between 0-1, to find
            the desired mean and deviation for

    Returns:
        float: the mean for this distributions
        float: +/- deviation for this confidence interval

    Example:
        >>> import numpy as np
        >>> import imagepypelines as ip
        >>> # create sample test 'accuracies' from a normal distribution
        >>> # mean accuracy is 75%, std is 10% for this example
        >>> accuracies = np.random.normal(.75, .1, 1000)
        >>> # get 95% confidence interval
        >>> mean, error = ip.confidence(accuracies,.95)
    """
    data = np.asarray(data,dtype=np.float32)
    # calculate mean and standard error of measurement
    m, se = np.mean(data), scipy.stats.sem(data)
    # find error using the percent point function and standard error
    h = se * scipy.stats.t.ppf((1 + confidence) / 2.0, len(data)-1)
    return m, h


def chunk(data,n):
    """chunk a list into n chunks"""
    chunk_size = math.ceil( len(data) / n )
    return batch(data, chunk_size)

def batch(data, batch_size):
    """chunks a list into multiple batch_size chunks, the last batch will
    be truncated if the data length isn't a multiple of batch_size
    """
    data = iter(data)
    return list(iter( lambda: list(islice(data, batch_size)), []) )

def chunks2list(batches):
    """turns nested iterables into a single list"""
    return list( chain(*batches) )

def xsample(data,sample_fraction):
    """function to randomly sample list data using a uniform distribution
    """
    assert isinstance(data,list),"data must be a list"
    assert sample_fraction >= 0 and sample_fraction <= 1,\
        "sample_fraction must be a float between 0 and 1"

    n = int(sample_fraction * len(data))
    sampled = random.sample(data,n)
    return sampled

def xysample(data,labels,sample_fraction=.05):
    """function to randomly sample list data and corresponding labels using a uniform
    distribution

    Example:
        >>> import random
        >>> random.seed(0)
        >>> import imagepypelines as ip
        >>> data = [0,1,2,3,4,5,6,7,8,9]
        >>> labels = ['0','1','2','3','4','5','6','7','8','9']
        >>>
        >>> small_data, small_labels = ip.xysample(data,labels,.2)
    """
    assert isinstance(data,list),"data must be a list"
    assert isinstance(labels,list),"labels must be a list"
    assert len(data) == len(labels), \
        "you must have an equal number of data and labels"
    assert min(0,sample_fraction) == 0 and max(1,sample_fraction) == 1,\
        "sample_fraction must be a float between 0 and 1"

    combined = list( zip(data, labels) )
    n = int(sample_fraction * len(data))
    sampled = random.sample(combined,n)
    sampled_data, sampled_labels = zip(*sampled)
    return list(sampled_data), list(sampled_labels)
