import numpy as np
import re

def np_to_pmatrix(matrix: np.ndarray) -> str:

    latex_matrix = r"\begin{pmatrix}"

    for row in matrix:
        latex_matrix += "\n"
        pretty_row = [f"{x:.2f}" for x in row]
        row_str = "\t" + r" & ".join(pretty_row) + r"\\"
    
        latex_matrix += row_str

    latex_matrix += "\n"
    latex_matrix += r"\end{pmatrix}"

    return latex_matrix