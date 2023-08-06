import six
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class ObjectDetector():
    """
    Abstract class used to wrapper object detector
    """
    @abstractmethod
    def detect(self, image, image_id):
        """

        [abstract method] need to implement detection method which return DetectionResult obj

        Parameters
        ----------
        image: PIL.Image
            PIL.Image instance
        image_id: ImageId
            image_id obj

        Returns
        -------
        DetectionResult: DetectionResult
            the detected result of given image
        """
        pass
