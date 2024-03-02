import pandas as pd

class Budget:
    """
    Amount of money that a driver receives 
    for his trip expenses
    """
    def __init__(
            self, df_tc: pd.DataFrame, 
            transf_date: bool = False):
        cond = df_tc['FECHA TRANSFERENCIA'] == 'Unregistered'
        if transf_date:
            self._df_tc = df_tc[~cond]
        else:
            self._df_tc = df_tc[cond]
        
    @property
    def budget_table(self) -> pd.DataFrame:
        """
        It contains the information about the 
        budget of those trips that meet the 
        previous condition.
        """
        return self._df_tc
    
    def dtypes(self, dtype: object = None) -> pd.Series:
        """Dtypes in Budget
        
        It can show either what types of data 
        are in the budget column or the kind of
        values that exist for a particular dtype'
        """
        budget_dtypes = self.budget_table['POR RENDIR S/'].map(type)
        if dtype == None:
            return budget_dtypes.value_counts()
        else:
            return self.budget_table.loc[
                budget_dtypes == dtype, 'POR RENDIR S/'
                ].value_counts()