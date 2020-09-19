import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.transform import transform_data
from utils.ingest import import_fred

sns.set(rc={"figure.figsize": (16, 12)})

if __name__ == '__main__':
    raw_df = import_fred()

    parsed_df = transform_data(raw_df)