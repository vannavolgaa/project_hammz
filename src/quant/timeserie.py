from dataclasses import dataclass
from datetime import datetime 
import numpy as np 
from arch.univariate.base import ARCHModelResult
from arch.univariate import (
    ZeroMean, 
    GARCH, 
    SkewStudent, 
    StudentsT, 
    Normal, 
    EGARCH, 
    ARX)
from arch.univariate.volatility import VarianceForecast

@dataclass
class TimeSerie:
    datamap : dict[datetime, float]

    def __post_init__(self): 
        self.datamap = dict(sorted(self.datamap.items()))
        self.log_difference = self.get_log_difference()
    
    def get_log_difference(self) -> np.array: 
        data = np.log(np.array(list(self.datamap.values())))
        return np.diff(data)
    
    def mean_log_difference(self) -> float: 
        return np.mean(self.log_difference())
    
    def std_log_difference(self) -> float: 
        return np.std(self.log_difference())
    
    def z_score_log_difference(self, ld: np.array) -> np.array: 
        return (ld - self.mean_log_difference())/self.std_log_difference()
    
    def skewed_student_egarch_fit(self) -> ARCHModelResult: 
        archmodel = ZeroMean(self.log_difference, rescale=False)
        archmodel.volatility = EGARCH(1,1,1)
        archmodel.distribution = StudentsT()
        return archmodel.fit(disp=False, show_warning=False)
    
    def ar_12lag_fit(self) -> ARCHModelResult: 
        archmodel = ARX(self.log_difference, lags=12, rescale=False)
        return archmodel.fit(disp=False, show_warning=False)

    


    

