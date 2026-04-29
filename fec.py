#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_path = '/home/hujm/pydata-book/datasets/fec/P00000001-ALL.csv'

class FECAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.mrbo = None

    def load_and_clean(self):
        df = pd.read_csv(self.filepath, low_memory=False)
        df = df[df['contb_receipt_amt'] > 0].copy()

        party_map = {
                'Obama, Barack': 'Democrat',
                'Romney, Mitt': 'Republican',
        }
        df['party'] = df['cand_nm'].map(party_map)
        df.dropna(subset=['party'], inplace=True)

        candidates = ['Obama, Barack', 'Romney, Mitt']
        self.mrbo = df[df['cand_nm'].isin(candidates)].copy()
        print(f"Loaded {len(self.mrbo)} records after cleaning")
        return self.mrbo

    def _clean_occupation(self, df, occ_mapping=None):
        if occ_mapping is None:
            occ_mapping = {
                    'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
                    'INFORMATION REQUESTED': 'NOT PROVIDED',
                    'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
                    'C.E.O.': 'CEO',
                    'LAWYER': 'ATTORNEY',
            }
        df = df.copy()
        df['clean_occ'] = df['contbr_occupation'].map(lambda x: occ_mapping.get(x, x))
        return df
