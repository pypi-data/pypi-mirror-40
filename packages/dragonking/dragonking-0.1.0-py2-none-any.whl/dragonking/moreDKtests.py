# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 22:47:15 2018

@author: Daniel
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#####SUM-SUM (SS) TEST STATISTIC#####
# Sum-sum (SS) test statistic to identify dragon kings (DKs)
#
# \code{ss_stat} calculates the SS test statistic to determine whether
# there is significant support for the existence of \code{r} DKs in
# \code{vals}. This test is susceptible to swamping.
#
## reference: Wheatley S, Sornette D (2015). Multiple outlier detection in samples with exponential & pareto tails: Redeeming the inward approach & detecting dragon kings.
# Swiss Finance Institute Research Paper Series No. 15-28. <doi:10.2139/ssrn.2645709>
## reference: Balakrishnan K (1996). Exponential distribution: Theory, methods and applications.
# \emph{CRC Press}. pp. 228-30. ISBN: 9782884491921
## reference: Chikkagoudar MS, Kunchur SH (1983). Distributions of test statistics for multiple outliers in exponential samples.
# \emph{Commun Stat Theory Methods}, \strong{12}: 2127-42. <doi:10.1080/03610928308828596>
## reference: Lewis T, Fieller NRJ (1979). A recursive algorithm for null distributions for outliers: I gamma samples.
# \emph{Technometrics}, \strong{21}(3): 371-6. <doi:10.2307/1267762>

## calculate and return SS test statistic for DKs

# type(vals)=np.array
##  numeric vector with at least 3 elements
# type(r)= int
## indicating number of DKs in \code{vals}
def ss_stat(vals,r):

  # calculate test statistic
  test_stat = float(sum(vals[0:r])) / sum(vals)

  # return test statistic
  return(test_stat)

####Example:
### ss_stat(temp, r = 3)


#####SUM-ROBUST-SUM (SRS) TEST STATISTIC#####
# Sum-robust-sum (SRS) test statistic to identify dragon kings (DKs)
#
# \code{srs_stat} calculates the SRS test statistic to determine whether
# there is significant support for the existence of \code{r} DKs in
# \code{vals}. This test provides robustness to denominator masking.
#
## reference: Wheatley S, Sornette D (2015). Multiple outlier detection in samples with exponential & pareto tails: Redeeming the inward approach & detecting dragon kings.
# Swiss Finance Institute Research Paper Series No. 15-28. <doi:10.2139/ssrn.2645709>
## reference: Iglewicz B, Martinez J (1982). Outlier detection using robust measures of scale.
# \emph{J Stat Comput Simul}, \strong{15}(4): 285-93. <doi:10.1080/00949658208810595>

## calculate and return SRS test statistic for DKs
  
# type(vals)=np.array
##  numeric vector with at least 3 elements
# type(r)= int
## indicating number of DKs in \code{vals}
def srs_stat(vals, r, m):
 
  # calculate test statistic
  test_stat = float(sum(vals[0:r])) / sum(vals[(m):len(vals)])

  # return test statistic
  return(test_stat)

####Example:
### srs_stat(temp, r = 2, m = 3)

#####MAX-SUM (MS) TEST STATISTIC#####
# Max-sum (MS) test statistic to identify dragon kings (DKs)
#
# \code{ms_stat} calculates the MS test statistic to determine whether
# there is significant support for the existence of \code{r} DKs in
# \code{vals}. This statistic is less susceptible to swamping, but is also
# less powerful in the case of clustered outliers, in comparison to the SS
# and SRS test statistics.
#
## reference: Wheatley S, Sornette D (2015). Multiple outlier detection in samples with exponential & pareto tails: Redeeming the inward approach & detecting dragon kings.
# Swiss Finance Institute Research Paper Series No. 15-28. <doi:10.2139/ssrn.2645709>
## reference: Hawkins DM (1980). Identification of outliers, vol. 11. \emph{Chapman and Hall}. 
#ISBN: 9789401539944
## reference: Kimber AC (1982). Tests for many outliers in an exponential sample.
# \emph{Appl Statist}, \strong{31}(3): 263-71. <doi:10.2307/2348000>

## calculate and return MS test statistic for DKs

## calculate test statistic for DKs
# ms_stat(temp, r = 3)
def ms_stat(vals, r):

  # calculate test statistic
  test_stat = float(vals[r-1]) / sum(vals[r-1:len(vals)])

  # return test statistic
  return(test_stat)


#####MAX-ROBUST-SUM (MRS) TEST STATISTIC#####
# Max-robust-sum (MRS) test statistic to identify dragon kings (DKs)
#
# \code{mrs_stat} calculates the MRS test statistic to determine whether
# there is significant support for the existence of \code{r} DKs in
# \code{vals}. This test avoids denominator masking.
#
# references: Wheatley S, Sornette D (2015). Multiple outlier detection in samples with exponential & pareto tails: Redeeming the inward approach & detecting dragon kings. Swiss Finance Institute Research Paper Series No. 15-28. <doi:10.2139/ssrn.2645709>
# 

## calculate test statistic for DKs
  
# type(vals) = np.array
##  numeric vector with at least 3 elements
# type(r) = integer
## indicating number of DKs in \code{vals}
# type(m) = integer
## pre-specified maximum number of DKs in \code{vals}
#
## calculate and return MRS test statistic for DKs
  
# mrs_stat(temp, r = 2, m = 3)
def mrs_stat(vals, r, m):

  ## calculate test statistic
  test_stat = float(vals[r-1])/ sum(vals[(m):len(vals)])

  ## return test statistic
  return(test_stat)

#####DIXON TEST STATISTIC#####
# Dixon test statistic to identify dragon kings (DKs)
#
# \code{dixon_stat} calculates the DIxon test statistic to determine whether
# there is significant support for the existence of \code{r} DKs in
# \code{vals}. This test is less susceptible to swamping and masking, but is
# also less powerful than the SS and SRS test statistics.
#
# reference: Wheatley S, Sornette D (2015). Multiple outlier detection in samples with exponential & pareto tails: Redeeming the inward approach & detecting dragon kings. Swiss Finance Institute Research Paper Series No. 15-28. <doi:10.2139/ssrn.2645709>
# reference: Dixon WJ (1950). Analysis of extreme values. \emph{Ann Math Stat}, \strong{21}(4): 488-506. <doi:10.1214/aoms/1177729747>
# reference: Likes J (1967). Distribution of Dixon's statistics in the case of an exponential population. \emph{Metrika}, \strong{11}(1): 46-54. <doi:10.1007/bf02613574>

## calculate test statistic for DKs

# type(vals) = np.array
##  numeric vector with at least 3 elements
# type(r) = integer
## indicating number of DKs in \code{vals}

## calculate and return Dixon test statistic for DKs

# dixon_stat(temp, r = 3)
def dixon_stat(vals, r):

  # calculate test statistic
  test_stat = float(vals[0]) / vals[r]

  # return test statistic
  return(test_stat)
