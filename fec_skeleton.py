import pandas as pd
import matplotlib.pyplot as plt

class FECAnalyzer:
    def __init__(self, filepath):
        """initial, provide file path, attribution"""
        self.filepath = filepath
        self.mrbo = None

    def load_and_clean(self):
        """
        load CSV file, drop neg amount, add party columns, substracte 
        only Obama/Romney
        """
        pass

    def _clean_occupation(self, df, occ_mapping=None):
        """cleaning occupation (inner method for aide)"""
        pass

    def occupation_pivot(self, df, min_total=1_000_000):
        """create occ+party pivot, add total column"""
        pass

    def plot_top_occupations(self, pivot_df, top_n=10):
        """plot contribution by occupations hbar"""
        pass

    def state_analysis(self, df, top_n=10):
        """plot contribution by state"""
        pass
