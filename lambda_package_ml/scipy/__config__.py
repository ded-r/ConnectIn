# This file is generated by SciPy's build process
# It contains system_info results at the time of building this package.
from enum import Enum

__all__ = ["show"]
_built_with_meson = True


class DisplayModes(Enum):
    stdout = "stdout"
    dicts = "dicts"


def _cleanup(d):
    """
    Removes empty values in a `dict` recursively
    This ensures we remove values that Meson could not provide to CONFIG
    """
    if isinstance(d, dict):
        return { k: _cleanup(v) for k, v in d.items() if v != '' and _cleanup(v) != '' }
    else:
        return d


CONFIG = _cleanup(
    {
        "Compilers": {
            "c": {
                "name": "clang",
                "linker": r"ld64",
                "version": "15.0.0",
                "commands": r"cc",
                "args": r"",
                "linker args": r"",
            },
            "cython": {
                "name": r"cython",
                "linker": r"cython",
                "version": r"3.0.12",
                "commands": r"cython",
                "args": r"",
                "linker args": r"",
            },
            "c++": {
                "name": "clang",
                "linker": r"ld64",
                "version": "15.0.0",
                "commands": r"c++",
                "args": r"",
                "linker args": r"",
            },
            "fortran": {
                "name": "gcc",
                "linker": r"ld64",
                "version": "13.3.0",
                "commands": r"gfortran",
                "args": r"",
                "linker args": r"",
            },
            "pythran": {
                "version": r"0.17.0",
                "include directory": r"../../../../../../private/var/folders/2s/h6hvv9ps03xgz_krkkstvq_r0000gn/T/pip-build-env-p7gx8hhw/overlay/lib/python3.11/site-packages/pythran"
            },
        },
        "Machine Information": {
            "host": {
                "cpu": r"aarch64",
                "family": r"aarch64",
                "endian": r"little",
                "system": r"darwin",
            },
            "build": {
                "cpu": r"aarch64",
                "family": r"aarch64",
                "endian": r"little",
                "system": r"darwin",
            },
            "cross-compiled": bool("False".lower().replace('false', '')),
        },
        "Build Dependencies": {
            "blas": {
                "name": "Accelerate",
                "found": bool("True".lower().replace('false', '')),
                "version": "unknown",
                "detection method": "extraframeworks",
                "include directory": r"unknown",
                "lib directory": r"unknown",
                "openblas configuration": r"unknown",
                "pc file directory": r"unknown",
            },
            "lapack": {
                "name": "Accelerate",
                "found": bool("True".lower().replace('false', '')),
                "version": "unknown",
                "detection method": "extraframeworks",
                "include directory": r"unknown",
                "lib directory": r"unknown",
                "openblas configuration": r"unknown",
                "pc file directory": r"unknown",
            },
            "pybind11": {
                "name": "pybind11",
                "version": "2.13.6",
                "detection method": "config-tool",
                "include directory": r"unknown",
            },
        },
        "Python Information": {
            "path": r"/private/var/folders/2s/h6hvv9ps03xgz_krkkstvq_r0000gn/T/cibw-run-4oaw7jjs/cp311-macosx_arm64/build/venv/bin/python",
            "version": "3.11",
        },
    }
)


def _check_pyyaml():
    import yaml

    return yaml


def show(mode=DisplayModes.stdout.value):
    """
    Show libraries and system information on which SciPy was built
    and is being used

    Parameters
    ----------
    mode : {`'stdout'`, `'dicts'`}, optional.
        Indicates how to display the config information.
        `'stdout'` prints to console, `'dicts'` returns a dictionary
        of the configuration.

    Returns
    -------
    out : {`dict`, `None`}
        If mode is `'dicts'`, a dict is returned, else None

    Notes
    -----
    1. The `'stdout'` mode will give more readable
       output if ``pyyaml`` is installed

    """
    if mode == DisplayModes.stdout.value:
        try:  # Non-standard library, check import
            yaml = _check_pyyaml()

            print(yaml.dump(CONFIG))
        except ModuleNotFoundError:
            import warnings
            import json

            warnings.warn("Install `pyyaml` for better output", stacklevel=1)
            print(json.dumps(CONFIG, indent=2))
    elif mode == DisplayModes.dicts.value:
        return CONFIG
    else:
        raise AttributeError(
            f"Invalid `mode`, use one of: {', '.join([e.value for e in DisplayModes])}"
        )
