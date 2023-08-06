import six
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class ObjectDetector():
    """
    Abstract class used to wrapper object detector
    """
    @abstractmethod
    def detect(self, image_obj):
        """

        [abstract method] need to implement detection method which return DetectionResult obj

        Parameters
        ----------
        image_obj: eyewitness.image_util.Image

        Returns
        -------
        DetectionResult: DetectionResult
            the detected result of given image
        """
        pass
