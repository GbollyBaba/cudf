import cupy as cp
import numpy as np
import pandas as pd
import pytest

import cudf
from cudf.tests.utils import assert_eq
from cudf.utils import dtypes as dtypeutils


@pytest.mark.parametrize(
    "data",
    [
        [1000000, 200000, 3000000],
        [1000000, 200000, None],
        [],
        [None],
        [None, None, None, None, None],
        [12, 12, 22, 343, 4353534, 435342],
        [0.3534, 12, 22, 343, 43.53534, 4353.42],
        np.array([10, 20, 30, None, 100]),
        cp.asarray([10, 20, 30, 100]),
    ],
)
@pytest.mark.parametrize("dtype", dtypeutils.TIMEDELTA_TYPES)
def test_timedelta_series_create(data, dtype):
    if dtype not in ("timedelta64[ns]"):
        pytest.skip(
            "Bug in pandas" "https://github.com/pandas-dev/pandas/issues/35465"
        )
    psr = pd.Series(
        cp.asnumpy(data) if isinstance(data, cp.ndarray) else data, dtype=dtype
    )
    gsr = cudf.Series(data, dtype=dtype)

    assert_eq(psr, gsr)


@pytest.mark.parametrize(
    "data",
    [
        [1000000, 200000, 3000000],
        [12, 12, 22, 343, 4353534, 435342],
        [0.3534, 12, 22, 343, 43.53534, 4353.42],
        cp.asarray([10, 20, 30, 100]),
    ],
)
@pytest.mark.parametrize("dtype", dtypeutils.TIMEDELTA_TYPES)
@pytest.mark.parametrize("cast_dtype", ["int64", "category", "object"])
def test_timedelta_from_typecast(data, dtype, cast_dtype):
    if dtype not in ("timedelta64[ns]"):
        pytest.skip(
            "Bug in pandas" "https://github.com/pandas-dev/pandas/issues/35465"
        )
    psr = pd.Series(
        cp.asnumpy(data) if isinstance(data, cp.ndarray) else data, dtype=dtype
    )
    gsr = cudf.Series(data, dtype=dtype)

    assert_eq(psr.astype(cast_dtype), gsr.astype(cast_dtype))


@pytest.mark.parametrize(
    "data",
    [
        [1000000, 200000, 3000000],
        [12, 12, 22, 343, 4353534, 435342],
        [0.3534, 12, 22, 343, 43.53534, 4353.42],
        cp.asarray([10, 20, 30, 100]),
    ],
)
@pytest.mark.parametrize("cast_dtype", dtypeutils.TIMEDELTA_TYPES)
def test_timedelta_to_typecast(data, cast_dtype):
    psr = pd.Series(cp.asnumpy(data) if isinstance(data, cp.ndarray) else data)
    gsr = cudf.Series(data)

    assert_eq(psr.astype(cast_dtype), gsr.astype(cast_dtype))


@pytest.mark.parametrize(
    "data",
    [
        [1000000, 200000, 3000000],
        [1000000, 200000, None],
        [],
        [None],
        [None, None, None, None, None],
        [12, 12, 22, 343, 4353534, 435342],
        [0.3534, 12, 22, 343, 43.53534, 4353.42],
        np.array([10, 20, 30, None, 100]),
        cp.asarray([10, 20, 30, 100]),
    ],
)
@pytest.mark.parametrize("dtype", dtypeutils.TIMEDELTA_TYPES)
def test_timedelta_from_pandas(data, dtype):
    psr = pd.Series(
        cp.asnumpy(data) if isinstance(data, cp.ndarray) else data, dtype=dtype
    )
    gsr = cudf.from_pandas(psr)

    assert_eq(psr, gsr)
