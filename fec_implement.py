import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = 'datasets/fec/P00000001-ALL.csv' # CHANGE THIS
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
        df = pd.read_csv(self.filepath, low_memory=False)
        df = df[df['contb_receipt_amt'] > 0].copy()
        party_map = {
               'Obama, Barack': 'Democrat',
               'Romney, Mitt': 'Repaublican',
        }
        df['party'] = df['cand_nm'].map(party_map)
        df.dropna(subset=['party'], inplace=True)
        candidates = ['Obama, Barack', 'Romney, Mitt']
        self.mrbo = df[df['cand_nm'].isin(candidates)].copy()
        print(f"Loaded {len(self.mrbo)} records")
        return self.mrbo

    def _clean_occupation(self, df, occ_mapping=None):
        """cleaning occupation (inner method for aide)"""
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

    def occupation_pivot(self, df, min_total=1_000_000):
        """create occ+party pivot, add total column"""
        df = self._clean_occupation(df)
        pivoted = df.pivot_table(
               values='contb_receipt_amt',
               index='clean_occ',
               columns='party',
               aggfunc='sum',
               fill_value=0
        )
        pivoted['total'] = pivoted.sum(axis=1)
        if min_total > 0:
            pivoted = pivoted[pivoted['total'] > min_total]
        return pivoted

    def plot_top_occupations(self, pivot_df, top_n=10):
        """plot contribution by occupations hbar"""
        plot_data = pivot_df.sort_values('total', ascending=False).head(top_n).drop(
                columns='total')
        plot_data.plot(kind='barh', figsize=(10, 8))
        plt.title(f'Top {top_n} Occupations by Total Contribution')
        plt.xlabel('Contribution Amount ($)')
        plt.tight_layout()
        plt.show()

    def bucket_analysis(self, df):
        bins = [1, 10, 100, 1000, 10_000, 100_000, 1_000_000, 10_000_000]
        labels = ['<$10', '$10-100', '$100-1k', '$1k-10k', '$10k-100k', '$100k-1M', '>$1M']
        df = df.copy() # initial data protected
        df['amt_bin'] = pd.cut(df['contb_receipt_amt'], bins=bins, labels=labels)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Contribution Size Distribution Comparison')
        for ax, candidate in zip(axes, ['Obama, Barack', 'Romney, Mitt']):
            sub = df[df['cand_nm'] == candidate]
            counts = sub['amt_bin'].value_counts().sort_index()
            counts.plot(kind='bar', ax=ax, title=candidate.split(',')[0])
            ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()
        
    def state_analysis(self, df, top_n=10):
        """plot contribution by state"""
        state_df = df.groupby(['cand_nm', 'contbr_st'])['contb_receipt_amt'].sum().unstack(
                fill_value=0)
        state_total = state_df.sum().sort_values(ascending=False)
        top_states = state_total.head(top_n).index
        plot_df = state_df[top_states].T
        plot_df.plot(kind='bar', figsize=(12, 6))
        plt.title(f'Top {top_n} States by Total Contribution')
        plt.xlabel('State')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    analyzer = FECAnalyzer(DATA_PATH)
    data = analyzer.load_and_clean()
    pivot = analyzer.occupation_pivot(data, min_total=1_000_000)
    analyzer.plot_top_occupations(pivot, top_n=10)
    analyzer.bucket_analysis(data)
    analyzer.state_analysis(data, top_n=10)
    print('The End')
