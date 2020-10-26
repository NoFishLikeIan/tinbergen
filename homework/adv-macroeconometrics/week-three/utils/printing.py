import re
import numpy as np
import pandas as pd

from typing import Dict, Tuple, NewType, List

pd.options.display.float_format = lambda num: f'{num:.6f}'

TestResults = NewType("TestResults", Dict[str, Tuple[np.float, np.float]])


def pprint(
    beta: np.ndarray, standard_error: np.ndarray, regressors: List[str],
    tests: TestResults = {},
    title="Withing regression"
):

    table = f"""
\033[1m{title}\033[0m:  

--- β:

{pd.Series(beta.reshape(-1,), index=regressors).to_string()}, 


--- Standard errors:

{pd.DataFrame(standard_error, index=regressors, columns=regressors)}
        """

    for test, values in tests.items():

        t, p = values

        table += f"""
--- {test}
{t:.4f}  {f"p={p:.4f}" if p is not None else ""}
"""

    print(table)


def np_to_pmatrix(matrix: np.ndarray, prec=2) -> str:

    latex_matrix = r"\begin{pmatrix}"

    for row in matrix:
        latex_matrix += "\n"
        pretty_row = [f"{x:.{prec}f}" for x in row]
        row_str = "\t" + r" & ".join(pretty_row) + r"\\"

        latex_matrix += row_str

    latex_matrix += "\n"
    latex_matrix += r"\end{pmatrix}"

    return latex_matrix
