from typing import Tuple

import h5py
import numpy
import pandas

from . import tools


def read_output(
        path: str
) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    is_hdf5, path, interior_path = tools.is_hdf5_path(path)
    if is_hdf5:
        return read_output_hdf5(path, interior_path)

    return read_output_ascii(path)


def read_output_ascii(
        path
) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Read an output file (raw ASCII format)

    Args:
       path (str): path to the file

    Return:
       list: The contents of the output file as a :py:class:`list` containing
          four :py:class:`numpy.ndarray` instances. The first one contains all
          simulation times. The other entries contain the norm, energy and
          maximum SPF overlap of the wave function at all times.
    """
    df = pandas.read_csv(
        path, sep=r"\s+", names=["time", "norm", "energy", "overlap"])
    return (df["time"].values, df["norm"].values, df["energy"].values,
            df["overlap"].values, )


def read_output_hdf5(
        path: str, interior_path: str="/"
) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    with h5py.File(path, "r") as fp:
        return (fp[interior_path]["time"][:], fp[interior_path]["norm"][:],
                fp[interior_path]["energy"][:],
                fp[interior_path]["overlap"][:], )


def write_output_hdf5(path: str,
                      data: Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray,
                                  numpy.ndarray]):
    with h5py.File(path, "w") as fp:
        dset = fp.create_dataset(
            "time", data[0].shape, dtype=data[0].dtype, compression="gzip")
        dset[:] = data[0]

        dset = fp.create_dataset(
            "norm", data[1].shape, dtype=data[1].dtype, compression="gzip")
        dset[:] = data[1]

        dset = fp.create_dataset(
            "energy", data[2].shape, dtype=data[2].dtype, compression="gzip")
        dset[:] = data[2]

        dset = fp.create_dataset(
            "overlap", data[3].shape, dtype=data[3].dtype, compression="gzip")
        dset[:] = data[3]
