# Classes
from .image_sequence import ImageSequence
from .serializable import Serializable, SerializableList
from .configuration import Configuration, ConfigurationKlass
from .utilities import FrameRange

# Functions
from .utilities import \
  build_pattern_from_path

# Flags
QFILEDIALOG_IMAGE_SEQUENCE_FILTER = "OpenEXR Sequences (*.exr)"
QFILEDIALOG_CONFIGURATION_FILTER = "Gaze Tracking Files (*.vtmo)"
QFILEDIALOG_MATLAB_FILTER = 'Matlab Files (*.mat)'