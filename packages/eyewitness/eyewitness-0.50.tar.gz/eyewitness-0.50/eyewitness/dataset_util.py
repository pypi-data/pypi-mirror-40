import os
from shutil import copyfile

from eyewitness.utils import make_path


def add_filename_prefix(filename, prefix):
    return "%s_%s" % (prefix, filename)


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
    print(filename, file=file_fp)


class BboxDataSet(object):
    """
    generate DataSet with same format as VOC object detections:

    <DataSet>/Annotations/<image_name>.xml
    <DataSet>/JPEGImages/<image_name>.jpg
    <DataSet>/ImageSets/Main/trainval.txt
    <DataSet>/ImageSets/Main/test.txt

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
