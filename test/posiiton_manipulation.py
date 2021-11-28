import pytest
from data_manipulation.data_types import PositionData
import numpy as np


test_data = [
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([0., 1., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([1., 1., 0.], [0., 0., 0.]), id="base transform"),
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([-1., 0., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([0., 0., 0.], [0., 0., 0]), id="base transform2"),
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([0., 0., 0.], [0., np.pi, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., np.pi, 0]), id="transform, next rotation"),
    pytest.param(PositionData.from_base_str([0., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., 0., 0.]),
                 PositionData.from_base_str([0., 0., -1.], [0., np.pi / 2, 0]), id="rotation, next transform"),
    pytest.param(PositionData.from_base_str([0., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([0., 0., -1.], [0., np.pi, 0]), id="rotation, next transform and rotation"),
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]).inv(),
                 PositionData.from_base_str([0., 0., 0.], [0., 0, 0]), id="manipulation + invert - 1"),
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., -1.], [0., np.pi, 0]), id="manipulation + manipulation - 1"),# errored
    pytest.param(PositionData.from_base_str([1., 0., 0.], [0., np.pi / 2, 0.]),
                 PositionData.from_base_str([0., 0., 0.], [0., -np.pi / 2, 0.]),
                 PositionData.from_base_str([1., 0., 0.], [0., 0, 0]), id="manipulation + manipulation - 2"),
]


@pytest.mark.parametrize("v1,v2,v3", test_data)
def test_data_manipulation(v1, v2, v3):
    res = v1.apply(v2)
    np.set_printoptions(precision=3, suppress=True)
    eps = 0.0001
    assert np.max(np.abs(res.xyz - v3.xyz)) < eps, f"need equal \n{res.xyz}-\n{v3.xyz}"
    assert np.max(np.abs(res.rot.as_matrix() - v3.rot.as_matrix())) < eps, f"need equal \n{res.rot.as_matrix()}------\n{v3.rot.as_matrix()}"
