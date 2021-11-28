import json
import xml.etree.ElementTree as ET
import numpy as np
import time
from scipy.spatial.transform import Rotation as R
import cv2


class PositionData:
    """
    Data type of point in space with orientation
    xyz - 3d vector with offset transformation
    rot - orientation transformation(after offset)
    t - timestamp of position(for future use)
    """

    def __init__(self, pos, rot, t=time.time()):
        self.xyz = pos
        self.rot = rot
        self.t = t

    @classmethod
    def from_robot_string(cls, s, t=time.time()):
        """! constructor for robot KRL format example:
        <Robot><Data><LastPos X="92.700218" Y="-49.260582" Z="512.477051" A="79.518661" B="-41.605556" C="22.007378"></LastPos></Data></Robot>

        :param s: str
            string for parsing
        :param t: time
            timestamp
        :return: PositionData
        """
        root = ET.fromstring(s)
        for pos in root.iter('LastPos'):
            rot = R.from_euler("zyx", np.array([float(pos.attrib['A']), float(pos.attrib['B']), float(pos.attrib['C'])]))
            return PositionData(np.array([float(pos.attrib['X']), float(pos.attrib['Y']), float(pos.attrib['Z'])]), rot, t=t)

    @classmethod
    def from_cv2(cls, tvec, rvec):
        """! constructor from OpenCV foramt

        :param tvec: 3d vector
            Transform vector
        :param rvec: 3d vector
            Rotation vector
        :return: PositionData
        """
        return PositionData(tvec[0], R.from_matrix(cv2.Rodrigues(rvec)[0]))

    def inv(self):
        return PositionData(-self.rot.inv().apply(self.xyz), self.rot.inv(), self.t)

    def apply(self, other):
        return PositionData(self.xyz+self.rot.apply(other.xyz), self.rot*other.rot)

    @classmethod
    def get_base(cls):
        return PositionData(np.array([0., 0., 0.]), R.from_matrix(np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])))

    @classmethod
    def from_base_str(cls, xyz, abc):
        return PositionData(np.array(xyz), R.from_euler("zyx", np.array(abc)))

    def __str__(self):
        return f"pos: {self.xyz}, rot: {self.rot.as_euler('zyx')}"

    def to_json_str(self):
        """! form json may restore later

        :return: str
        """
        res = dict()
        res['x'] = self.xyz[0]
        res['y'] = self.xyz[1]
        res['z'] = self.xyz[2]
        abc = self.rot.as_euler('zyx')
        res['a'] = abc[0]
        res['b'] = abc[1]
        res['c'] = abc[2]
        res['t'] = self.t
        return json.dumps(res)

    @classmethod
    def from_json_str(cls, s):
        """ constructor from json str

        :param s: str
            string to parse
        :return: PositionData
        """
        res = json.loads(s)
        return PositionData(np.array([res['x'], res['y'], res['z']]),
                            R.from_euler("zyx", np.array([res['a'], res['b'], res['c']])),
                            t=res['t'])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all() and (self.rot.as_matrix() == other.rot.as_matrix()).all()
