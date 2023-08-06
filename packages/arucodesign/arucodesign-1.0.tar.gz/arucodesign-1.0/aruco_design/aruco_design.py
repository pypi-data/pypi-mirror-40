#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from collections import namedtuple
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import cv2
import numpy as np

__all__ = ['DesignFromIllustrator', 'DesignFromIllustratorIterator']


class DesignFromIllustrator(object):

    def __init__(self, json_path: str) -> None:

        with open(json_path, 'r') as f:
            self.data = json.load(f)

    def list_obj_types(self) -> List[str]:
        data_types = np.array(list(map(lambda datum: datum.get('objectType'), self.data)))
        unique_data_types = np.unique(data_types)
        return list(unique_data_types)

    def query_with_obj_type(self, obj_type) -> List[Any]:
        data_filtered = filter(lambda datum: datum.get('objectType') == obj_type, self.data)
        return list(data_filtered)

    def query_markers_with_object(self, obj_id) -> List[Any]:
        data_filtered: List[Any] = []
        markers = filter(lambda datum: datum.get('objectType') == 'marker', self.data)
        for datum in markers:
            if datum.get('belongsTo') is None:
                continue

            id_parent = datum.get('belongsTo')
            if obj_id == id_parent:
                data_filtered.append(datum)

        return data_filtered

    def query_is_link_exists(self, obj_id1, obj_id2) -> bool:
        link_data = filter(lambda datum: datum.get('objectType') == 'link', self.data)
        link_found: bool = False
        for datum in link_data:
            id1 = datum.get('p1')
            id2 = datum.get('p2')
            if ((id1 == obj_id1) and (id2 == obj_id2)) or ((id2 == obj_id1) and (id1 == obj_id2)):
                link_found = True
                break

        return link_found

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return DesignFromIllustratorIterator(self.data)


class DesignFromIllustratorIterator(object):
    def __init__(self, data):
        self.data = data
        self._i = 0

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i == len(self.data):
            raise StopIteration()

        ret = self.data[self._i]
        self._i += 1
        return ret


MarkerReaderResult = namedtuple('MarkerReaderResult', ('corners', 'ids', 'rejectedImgPoints', 'drawn_frame'))
MarkerReader3DResult = namedtuple('MarkerReaderResult', ('corners', 'ids', 'rejectedImgPoints', 'drawn_frame', 'tvecs', 'rvecs'))


class MarkerReader(object):

    aruco_dictionary: Any = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    def __init__(self,
                 do_localization: bool = False,
                 camera_matrix: Optional[np.ndarray]=None,
                 camera_distortion: Optional[np.ndarray]=None,
                 marker_size: Optional[Union[float, Dict[int, float]]]=None) -> None:

        self.do_localization = do_localization
        if self.do_localization:
            assert camera_matrix is not None
            assert camera_distortion is not None
            assert marker_size is not None

            self.camera_matrix: np.ndarray = self.camera_matrix
            self.camera_distortion: np.ndarray = self.camera_distortion
            self.marker_size: np.ndarray = self.marker_size

    def read(self, frame: np.ndarray) -> Union[MarkerReaderResult, MarkerReader3DResult]:
        drawn_frame = np.copy(frame)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, self.aruco_dictionary)
        cv2.aruco.detectMarkers(drawn_frame, self.aruco_dictionary)
        if not self.do_localization:
            return MarkerReaderResult(corners, ids, rejectedImgPoints, drawn_frame)

        if isinstance(self.marker_size, float):
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.camera_distortion)
        else:
            rvecs_ = []
            tvecs_ = []
            for corner, aruco_id in zip(corners, ids.flatten()):
                marker_size = self.marker_size[aruco_id]
                rvecs_i, tvecs_i, _ = cv2.aruco.estimatePoseSingleMarkers(np.array([corner]), marker_size, self.camera_matrix, self.camera_distortion)
                rvecs_.append(rvecs_i[0])
                tvecs_.append(tvecs_i[0])

            rvecs = np.array(rvecs_)
            tvecs = np.array(tvecs_)

        for i in range(ids.size):
            cv2.aruco.drawAxis(drawn_frame, self.camera_matrix, self.camera_distortion, rvecs[i], tvecs[i], 0.1)

        return MarkerReader3DResult(corners, ids, rejectedImgPoints, drawn_frame, tvecs, rvecs)
