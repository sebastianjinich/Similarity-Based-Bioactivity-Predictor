from rdkit import DataStructs
import statistics
import numpy as np


def max_similarity_scorer(fps_to_compare, all_fps_to_compare_with, labels, similarity:DataStructs):
    all_comparisons = [similarity(fps_to_compare, fps) for fps in all_fps_to_compare_with]
    return max(all_comparisons)

def mean_similarity_scorer(fps_to_compare, all_fps_to_compare_with, labels, similarity:DataStructs):
    all_comparisons = [similarity(fps_to_compare, fps) for fps in all_fps_to_compare_with]
    return statistics.mean(all_comparisons)

def upper_cuartile_scorer(fps_to_compare, all_fps_to_compare_with, labels, similarity:DataStructs):
    all_comparisons = [similarity(fps_to_compare, fps) for fps in all_fps_to_compare_with]
    arr = np.array(all_comparisons)
    upper_quartile_value = np.percentile(arr, 75)
    upper_quartile_elements = arr[arr >= upper_quartile_value]
    average = np.mean(upper_quartile_elements)
    return average

def upper_decile_scorer(fps_to_compare, all_fps_to_compare_with, labels, similarity:DataStructs):
    all_comparisons = [similarity(fps_to_compare, fps) for fps in all_fps_to_compare_with]
    arr = np.array(all_comparisons)
    upper_quartile_value = np.percentile(arr, 90)
    upper_quartile_elements = arr[arr >= upper_quartile_value]
    average = np.mean(upper_quartile_elements)
    return average