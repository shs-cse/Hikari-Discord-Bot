import numpy as np
import pandas as pd

def main():
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(s)
    
if __name__ == "__main__":
    main()