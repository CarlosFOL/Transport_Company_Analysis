import pandas as pd

class Budget:
    """
    Amount of money that a driver receives 
    for his trip expenses
    """
    
    
    def __init__(
            self, df_tc: pd.DataFrame, 
            transf_date: bool = False):
        self._transf_date = transf_date
        self._df_tc = df_tc.copy()
    
    
    @property
    def transf_date(self) -> bool:
        """
        It indicates whether to return the 
        trips with a valid transfer date.
        """
        return self._transf_date
    
    
    @property
    def table_tc(self) -> pd.DataFrame:
        """
        The table that records the main attributes of the 
        trips made by the Anonymous Transport Company.
        """
        return self._df_tc
    
    @table_tc.setter
    def table_tc(self, df_tc_up: pd.DataFrame) -> None:
        """
        Update the table_tc contents after 
        manipulating the data in Budget column
        """
        self._df_tc = df_tc_up
        

    @property
    def budget_table(self) -> pd.DataFrame:
        """
        It contains the budget data of these trips 
        that meet the transfer date condition.
        """
        cols = ['FECHA TRANSFERENCIA', 'ORIGEN', 'DESTINO', 
                'FAMILIA', 'NUEVO / SEMINUEVO', 'POR RENDIR S/']
        cond = self.table_tc['FECHA TRANSFERENCIA'] == 'Unregistered'
        if self.transf_date:
            return self.table_tc.loc[~cond, cols]
        else:
            return self.table_tc.loc[cond, cols]
    
    
    def dtypes(self, dtype: object = None) -> pd.Series:
        """Dtypes in Budget
        
        It can show either what types of data 
        are in the budget column or the kind of
        values that exist for a particular dtype.
        """
        budget_dtypes = self.budget_table['POR RENDIR S/'].map(type)
        if dtype == None:
            return budget_dtypes.value_counts()
        else:
            return self.budget_table.loc[
                budget_dtypes == dtype, 'POR RENDIR S/'
                ].value_counts()