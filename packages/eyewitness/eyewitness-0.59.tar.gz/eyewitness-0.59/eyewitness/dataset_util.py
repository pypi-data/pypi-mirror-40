from __future__ import print_function
import os
import glob
import random
from shutil import copyfile

from lxml import etree
from eyewitness.utils import make_path
from eyewitness.models.db_proxy import DATABASE_PROXY
from eyewitness.models.feedback_models import FalseAlertFeedback
from eyewitness.models.detection_models import BboxDetectionResult


def add_filename_prefix(filename, prefix):
    return "%s_%s" % (prefix, filename)


def create_bbox_dataset_from_eyewitness(
        database, valid_classes, output_dataset_folder, dataset_name):
    """
    generate bbox dataset from eyewitness

    - remove images with false-alert feedback

    - get images with selected classes objects
    """
    anno_folder = os.path.join(output_dataset_folder, 'Annotations')
    jpg_images_folder = os.path.join(output_dataset_folder, 'JPEGImages')
    main_folder = os.path.join(output_dataset_folder, 'ImageSets', 'Main')

    # mkdir if not exist
    make_path(anno_folder)
    make_path(jpg_images_folder)
    make_path(main_folder)

    DATABASE_PROXY.initialize(database)
    # filter false alert, and valid_classes
    false_alert_query = FalseAlertFeedback.select(
        FalseAlertFeedback.image_id).where(FalseAlertFeedback.is_false_alert)
    valid_objects = BboxDetectionResult.select().where(
        BboxDetectionResult.image_id.not_in(false_alert_query),
        BboxDetectionResult.label.in_(valid_classes))

    # get valid_images with raw_image_path
    valid_images = set(i.image_id for i in valid_objects if i.image_id.raw_image_path)

    # generate etree obj for each images
    for valid_image in valid_images:
        if (valid_image.file_format != 'jpg' or not os.path.exists(valid_image.raw_image_path)):
            # TODO: support other file_format
            continue

        ori_image_file = valid_image.raw_image_path
        dest_image_file = os.path.join(jpg_images_folder, "%s.jpg" % valid_image.image_id)
        copyfile(ori_image_file, dest_image_file)

        # prepare anno_file
        anno_file = os.path.join(anno_folder, "%s.xml" % valid_image.image_id)
        detected_objects = list(BboxDetectionResult.select().where(
            BboxDetectionResult.image_id == valid_image,
            BboxDetectionResult.label.in_(valid_classes)))
        if detected_objects:  # make sure there is detected objects
            etree_obj = generate_etree_obj(valid_image, detected_objects, dataset_name)
            etree_obj.write(anno_file, pretty_print=True)


def generate_etree_obj(valid_image, detected_objects, dataset_name):
    root = etree.Element("annotation")
    filename = etree.SubElement(root, "filename")
    source = etree.SubElement(root, "source")
    databases = etree.SubElement(source, "database")

    filename.text = valid_image.image_id
    databases.text = dataset_name
    for obj in detected_objects:
        object_ = etree.SubElement(root, "object")
        name = etree.SubElement(object_, "name")
        name.text = obj.label
        pose = etree.SubElement(object_, "pose")
        pose.text = "Unspecified"
        truncated = etree.SubElement(object_, "truncated")
        truncated.text = "0"
        difficult = etree.SubElement(object_, "difficult")
        difficult.text = "0"
        # bounded box
        bndbox = etree.SubElement(object_, "bndbox")
        xmin_ = etree.SubElement(bndbox, "xmin")
        ymin_ = etree.SubElement(bndbox, "ymin")
        xmax_ = etree.SubElement(bndbox, "xmax")
        ymax_ = etree.SubElement(bndbox, "ymax")
        xmin_.text = str(obj.x1)
        ymin_.text = str(obj.y1)
        xmax_.text = str(obj.x2)
        ymax_.text = str(obj.y2)
    return etree.ElementTree(root)


def copy_image_to_output_dataset(filename, src_dataset, jpg_images_folder, anno_folder, file_fp):
    filename_with_prefix = add_filename_prefix(filename, src_dataset.dataset_name)

    # copy image file
    ori_image_file = os.path.join(src_dataset.jpg_images_folder, "%s.jpg" % filename)
    dest_image_file = os.path.join(jpg_images_folder, "%s.jpg" % filename_with_prefix)
    copyfile(ori_image_file, dest_image_file)

    # copy annotation file
    ori_anno_file = os.path.join(src_dataset.anno_folder, "%s.xml" % filename)
    dest_anno_file = os.path.join(anno_folder, "%s.xml" % filename_with_prefix)
    copyfile(ori_anno_file, dest_anno_file)

    # print filename to the filename list file
    print(filename_with_prefix, file=file_fp)


class BboxDataSet(object):
    """
    generate DataSet with same format as VOC object detections:

    <dataset_folder>/Annotations/<image_name>.xml

    <dataset_folder>/JPEGImages/<image_name>.jpg

    <dataset_folder>/ImageSets/Main/trainval.txt

    <dataset_folder>/ImageSets/Main/test.txt

    """
    def __init__(self, dataset_folder, dataset_name):
        self.anno_folder = os.path.join(dataset_folder, 'Annotations')
        self.jpg_images_folder = os.path.join(dataset_folder, 'JPEGImages')
        self.main_folder = os.path.join(dataset_folder, 'ImageSets', 'Main')
        self.trainval_file = os.path.join(self.main_folder, 'trainval.txt')
        self.test_file = os.path.join(self.main_folder, 'test.txt')
        self.dataset_name = dataset_name

    @property
    def training_and_validation_set(self):
        with open(self.trainval_file) as f:
            for i in f:
                yield i.strip()

    @property
    def testing_set(self):
        with open(self.test_file) as f:
            for i in f:
                yield i.strip()

    def generate_train_test_list(self, overwrite=True, train_ratio=0.9):
        if not overwrite and os.path.exists(self.trainval_file) and os.path.exists(self.test_file):
            return
        else:
            anno_files = glob.glob('%s/*.xml' % self.anno_folder)
            image_ids_anno = set(
                anno_file.rsplit('/', 1)[1].replace('.xml', '') for anno_file in anno_files)
            jpg_files = glob.glob('%s/*.jpg' % self.jpg_images_folder)
            image_ids_jpg = set(
                jpg_file.rsplit('/', 1)[1].replace('.jpg', '') for jpg_file in jpg_files)
            image_ids = image_ids_jpg.intersection(image_ids_anno)

            # write to training set
            training_set = random.sample(image_ids, int(len(image_ids) * train_ratio))
            with open(self.trainval_file, 'w') as f:
                for train_id in training_set:
                    print(train_id, file=f)

            testing_set = image_ids.difference(training_set)
            with open(self.test_file, 'w') as f:
                for test_id in testing_set:
                    print(test_id, file=f)

    @classmethod
    def union_bbox_datasets(cls, datasets, output_dataset_folder, dataset_name):
        """
        union bbox datasets and copy files to the given output_dataset
        """
        anno_folder = os.path.join(output_dataset_folder, 'Annotations')
        jpg_images_folder = os.path.join(output_dataset_folder, 'JPEGImages')
        main_folder = os.path.join(output_dataset_folder, 'ImageSets', 'Main')

        # mkdir if not exist
        make_path(anno_folder)
        make_path(jpg_images_folder)
        make_path(main_folder)

        # write train, test list out
        trainval_file = os.path.join(main_folder, 'trainval.txt')
        test_file = os.path.join(main_folder, 'test.txt')
        with open(trainval_file, 'w') as train_fp, open(test_file, 'w') as test_fp:
            for dataset in datasets:
                for train_file in dataset.training_and_validation_set:
                    copy_image_to_output_dataset(
                        train_file, dataset, jpg_images_folder, anno_folder, train_fp)

                for test_file in dataset.testing_set:
                    copy_image_to_output_dataset(
                        test_file, dataset, jpg_images_folder, anno_folder, test_fp)

        return cls(output_dataset_folder, dataset_name)
