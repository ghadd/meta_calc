from typing import Tuple
import numpy as np
from itertools import product
import jinja2
from pathlib import Path
import sys
from humanize import naturalsize, naturaltime
import time

DEFAULT_PATH = str(Path.home() / "calc.py")


def create_calc(boundaries=Tuple[float, float], step: float = 1e-1,
                filename: str = DEFAULT_PATH, verbose: bool = True):
    values = np.arange(*boundaries, step)
    all_pairs = product(values, repeat=2)

    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")

    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "base.jinja2"
    template = templateEnv.get_template(TEMPLATE_FILE)

    start = time.time()

    content = template.render(
        abs_tol=step,
        pairs=all_pairs,
    )

    with open(filename, 'w') as file:
        file.write(content)

    end = time.time()

    if verbose:
        print("File path: {}".format(str(Path(filename).absolute())))
        print("File size: {}".format(naturalsize(Path(filename).stat().st_size)))
        print("Took {} to render and save".format(naturaltime(end - start)))
        print("Your numbers must be in range of [{};{})".format(*boundaries))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = DEFAULT_PATH

    create_calc((-10, 10), filename=filename, verbose="-v" in sys.argv)
    print("Running generated script (ex. 1.2 + 2.4)...")
    try:
        exec(open(filename).read())
    except Exception as e:
        print("Ah... error occured.")
