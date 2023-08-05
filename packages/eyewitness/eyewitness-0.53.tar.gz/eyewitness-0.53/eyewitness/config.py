# detection type
BBOX = 'bbox'

# Feedback type
FEEDBACK_BBOX = 'feedback_bbox'
FEEDBACK_FALSE_ALERT = 'feedback_false_alert'

# image producer type
POST_PATH = 'post_path'
POST_BYTES = 'post_bytes'
IN_MEMORY = 'in_memory'

# Line false_alert msg template
LINE_FALSE_ALERT_MSG_TEMPLATE = "false_alert_{image_id}_{meta}"
LINE_FALSE_ALERT_ANNOTATION_PATTERN = (
    r"false_alert_(?P<channel>.*)::(?P<timestamp>\d*)::(?P<file_format>.*)_(?P<meta>.*)")

# audience_platfrom
LINE_PLATFROM = 'line'

# image_info fields
RAW_IMAGE_PATH = 'raw_image_path'
IMAGE_ID = 'image_id'

# detected_result fields
DRAWN_IMAGE_PATH = 'drawn_image_path'
DETECTED_OBJECTS = 'detected_objects'
DETECTION_METHOD = 'detection_method'

# audience_info fields
AUDIENCE_ID = 'audience_id'
RECEIVE_TIME = 'receive_time'

# feedback infomation
FEEDBACK_METHOD = 'feedback_method'
FEEDBACK_MSG_OBJS = 'feedback_msg_objs'
FEEDBACK_META = 'feedback_meta'
IS_FALSE_ALERT = 'is_false_alert'
