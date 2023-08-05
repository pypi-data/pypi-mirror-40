import json
import six
from abc import ABCMeta, abstractmethod
from collections import namedtuple

from eyewitness.config import BBOX
from eyewitness.image_id import ImageId


BoundedBoxObject = namedtuple(
    'BoundedBoxObject', ['x1', 'y1', 'x2', 'y2', 'label', 'score', 'meta'])
Type_Serialization_Mapping = {BBOX: BoundedBoxObject}


class DetectionResult(object):
    """
    represent detection result of a image.
    """

    def __init__(self, image_dict):
        """
        Parameters
        ----------
        image_dict: dict
            - detection_method: detection_method str

            - detected_objects: List[tuple], list of detected obj (optional)

            - drawn_image_path: str, path of drawn image (optional)

            - image_id: image_id obj
        """
        # get detection method
        self.detection_method = image_dict.get('detection_method', BBOX)
        self.detection_type = Type_Serialization_Mapping[self.detection_method]
        self.image_dict = image_dict

    @property
    def image_id(self):
        """ImageId: image_id obj"""
        return self.image_dict['image_id']

    @property
    def drawn_image_path(self):
        """str: drawn_image_path"""
        return self.image_dict.get('drawn_image_path', '')

    @property
    def detected_objects(self):
        """List[object]: List of detected objects in the image"""
        detected_objects = self.image_dict.get('detected_objects', [])
        return [self.detection_type(*i) for i in detected_objects]

    @classmethod
    def from_json(cls, json_str):
        img_json_dict = json.loads(json_str)
        img_json_dict['image_id'] = ImageId.from_str(img_json_dict['image_id'])
        return cls(img_json_dict)

    def to_json_dict(self):
        """
        Returns
        -------
        image_dict: dict
            the dict repsentation of detection_result
        """
        json_dict = dict(self.image_dict)
        json_dict['image_id'] = str(json_dict['image_id'])
        return json_dict


@six.add_metaclass(ABCMeta)
class DetectionResultHandler():
    """a abstract class design to handle detection result
    need to implement:

    - function: _handle(self, detection_result)

    - property: detection_method
    """
    @abstractmethod
    def _handle(self, detection_result):
        """abstract method for handle DetectionResult

        Parameters
        ----------
        detection_result: DetectionResult
        """
        pass

    def handle(self, detection_result):
        """wrapper of _handle function with the check of detection_method with detection_result.

        Parameters
        ----------
        detection_result: DetectionResult
        """
        assert self.detection_method == detection_result.detection_method
        self._handle(detection_result)

    @property
    def detection_method(self):
        raise NotImplementedError
