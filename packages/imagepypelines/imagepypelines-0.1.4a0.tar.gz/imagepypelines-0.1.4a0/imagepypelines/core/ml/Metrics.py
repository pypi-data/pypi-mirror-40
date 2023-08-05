# import numpy as np
# import scipy.stats as st
#
# def accuracy(predicted, ground_truth):
#     """calculates accuracy given ground truth and predicted labels"""
#     num_correct = np.sum(np.asarray(predicted) == np.asarray(ground_truth))
#     mean = float(num_correct) / len(predicted)
#
#     std =
#
#
#
# class Metrics(object):
#     def __init__(self, fold_data=None):
#         self.fold_data = fold_data
#         if self.fold_data is None:
#             self.fold_data = []
#
#     def add_fold(predictions,ground_truth):
#         predictions = np.asarray(predictions)
#         ground_truth = np.asarray(ground_truth)
#
#         assert predictions.shape == ground_truth.shape,\
#             "there must be an equal number of predictions and truths"
#
#         self.fold_data.append( (predictions,ground_truth) )
#
#     @staticmethod
#     def __mean_ci(predictions,ground_truth,confidence=.95):
#         z = st.norm.ppf(1-(1-confidence)/2)
#         N = predictions.size
#
#         iscorrect = (predictions == ground_truth)
#         u = np.mean(iscorrect)
#         ci = z * np.sqrt( u*(1-u) / N ) # z * standard error
#         return u-ci, u+ci
#
#
#     def accuracy1():
#         fold_means
