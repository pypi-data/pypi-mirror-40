
.. index:: Probabilities

.. _probabilities:

Probabilities
-------------

To estimate the fraction of the distribution that lies above or 
below some point in a distribution, we can use the standard comparison 
operators (<, <=, >, >=, ==, !=)::

    # What is the percentage of samples below 21?
    >>> x1<21
    0.0014  (i.e., about 0.1%)
    
    # What percentage of samples are 1000 and above?
    >>> Z>=1000
    0.6622  (i.e., about 66%)
    
On the otherhand, if we are comparing distributions to see if one is
"less" or "more" than the other, we actually perform a T-test of the two
objects to compare the two sample means. If the p-value is greater than
0.05 AND the t-statistic has the correct sign, then the comparison will
return ``True``. Let's first create some new samples (the actual values
are contained in the ``_mcpts`` member of the ``UncertainFunction`` class::

    >>> rvs1 = N(5, 10)
    >>> rvs2 = N(5, 10) + N(0, 0.2)
    >>> rvs3 = N(8, 10) + N(0, 0.2)
    
Now, let's compare ``rvs1`` and ``rvs2``. They are similar, but with slightly
different variances, so we would expect the p-value to be large::

    >>> from scipy.stats import ttest_rel
    >>> tstat, pval = ttest_rel(rvs1._mcpts, rvs2._mcpts)
    >>> pval
    0.99888340212679583
    
As expected, because the p-value is essentially, 1.0, the test couldn't tell
them apart, so our comparison returns::

    >>> rvs1<rvs2
    False

However, let's try distributions that are a more different, ``rvs1`` and
``rvs3``. This test should return a smaller p-value and a t-statistic that
we will get the sign from to check the orientation of the comparison::

    >>> tstat, pval = ttest_rel(rvs1._mcpts, rvs3._mcpts)
    >>> pval
    3.0480674044727307e-97

That's a very small p-value, indicating that the distributions are
separated from each other distinctly enough that the test could tell them
apart. Now we need to check the sign of the t-statistic to see if 
``rvs1`` is on the "left" of ``rvs3`` for the comparison::

    >>> float(tstat)
    -21.158661004433682

Because we are using the *less than* comparison and the sign of the 
t-statistic is negative, then we say that this is "oriented" correctly
and, no surprise, we get::

    >>> rvs1<rvs3
    True

If we had tried *greater than*, then we would have gotten the wrong sign
on the t-statistic and the comparison evaluates to ``False``.

One interesting thing about this way of testing two distributions is that
it's possible to get the following::

    >>> x = N(0, 1)
    >>> y = N(0, 10)
    >>> x<y
    False
    >>> x>y
    False
    >>> x==y
    False
    
The equality comparison operators (== and !=) actually test to see if 
the distributions are identical, thus::
    
    >>> x1==x1
    True

    >>> n1 = N(0, 1)
    >>> n2 = N(0, 1)
    >>> n1==n2  # n1 and n2 are independently sampled, so they are not equal
    False
    
    >>> Z*Z==Z**2  # Both sides have the same root samples, so they are equal
    True

If an MCERP object is compared to a scalar value, then a sampled probability
is calculated. For example, let's say we have a 45 black marbles, 5 white
marbles, and we are going to put them all into a hat and pick out 10. What's
the probability that 4 of the ten will be white? Let's see::

    >>> h = H(50, 5, 10)
    >>> h==4
    0.004  # the precise answer is 0.0039..., so not bad.

What's the probability we will get three or less (that includes 0)::

    >>> h<=3
    0.9959
    
For MCERP objects that represent continuous distributions, we see that any
equality operators (usually) return a probability of zero::

    >>> n = N(0, 1)
    >>> n==0
    0.0
    >>> n==0.5
    0.0
    >>> n==1.2345
    0.0

But inequality operators are more useful::

    >>> n<0
    0.5
    >>> n<1.5
    0.9332  # actual is 0.9331927, so not to far off with 10000 samples!
