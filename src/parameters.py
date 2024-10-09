from dataclasses import dataclass
from datetime import timedelta 

@dataclass
class BacktestParameters: 
    csv_lines_to_load: int = 500000



