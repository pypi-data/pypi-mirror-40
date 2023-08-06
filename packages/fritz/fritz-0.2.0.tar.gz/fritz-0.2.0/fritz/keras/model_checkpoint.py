"""
fritz.keras.model_checkpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains a Keras callback to upload new versions of a
model to Fritz.
"""


import os
import keras
from fritz.client import FritzClient


class _SupportedMobileModelTypes(object):
    """Mobile models supported in Fritz."""

    TENSORFLOW_LITE = 'tensorflow_lite'
    TENSORFLOW_MOBILE = 'tensorflow_mobile'
    CORE_ML = 'core_ml'

    EXTENSIONS_BY_TYPE = {
        TENSORFLOW_LITE: '.tflite',
        TENSORFLOW_MOBILE: '.pb',
        CORE_ML: '.mlmodel',
    }

    @classmethod
    def get_extension(cls, model_type):
        """Returns file extension for model_type

        Args:
            model_type (str): Mobile model type to get extension for.

        Returns: File Extension for mobile model.
        """
        return cls.EXTENSIONS_BY_TYPE[model_type]


class _FritzModelCheckpointBase(keras.callbacks.Callback):
    """Saves current Keras model as a new model in Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 mobile_model_type,
                 keras_filename,
                 convert_function,
                 period=1,
                 deploy=False):
        """Save a checkpoint to Fritz.

        Args:
            fritz_api_key (str): Fritz client API key.
            model_uid (str): Fritz Model UID to add new versions to.
            mobile_model_type (str): Type of mobile model to convert to.
            keras_filename (str): Name of Keras model output filename.
            convert_function (func): Function used to convert Keras model
                to mobile model.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(_FritzModelCheckpointBase, self).__init__()
        self._client = FritzClient(fritz_api_key)
        self._model_uid = model_uid
        self._model_extension = (
            _SupportedMobileModelTypes.get_extension(mobile_model_type)
        )
        self._keras_filename = keras_filename
        self._period = period
        self._deploy = deploy
        self._convert_func = convert_function

    def add_model_metadata(self, logs):  # noqa pylint: disable=unused-argument,no-self-use
        """Adds additional metadata about the model to be stored in Fritz.

        Optionally override this method returning custom information.

        Args:
            logs (dict): Includes values such as `acc` and `loss`.

        Returns: Dict of model metadata.
        """
        return {}

    def on_epoch_end(self, epoch, logs=None):
        """Saves model to Fritz on epoch end.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        # Adding one so that the very first run does not trigger an upload.
        # If you specify period to be 3, the first upload will be on the 3rd
        # epoch.
        if (epoch + 1) % self._period != 0:
            return

        converted_model = self._convert_func(self.model)

        metadata = {
            'epoch': epoch,
            'keras_model_path': self._keras_filename,
        }
        metadata.update(logs or {})
        metadata.update(self.add_model_metadata(logs))

        mlmodel_filename = os.path.splitext(
            os.path.basename(self._keras_filename)
        )[0] + '.' + self._model_extension.lstrip('.')
        self._client.upload_new_version(self._model_uid,
                                        mlmodel_filename,
                                        converted_model,
                                        set_active=self._deploy,
                                        metadata=metadata)

    def on_train_end(self, logs=None):
        """Saves model to Fritz at end of training run.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        converted_model = self._convert_func(self.model)

        metadata = {
            'keras_model_path': self._keras_filename,
        }
        metadata.update(logs or {})
        metadata.update(self.add_model_metadata(logs))

        mlmodel_filename = os.path.splitext(
            os.path.basename(self._keras_filename)
        )[0] + '.' + self._model_extension.lstrip('.')
        self._client.upload_new_version(self._model_uid,
                                        mlmodel_filename,
                                        converted_model,
                                        set_active=self._deploy,
                                        metadata=metadata)


class FritzMLModelCheckpoint(_FritzModelCheckpointBase):
    """Saves current Keras model as a new MLModel in Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 keras_filename,
                 convert_function,
                 period=1,
                 deploy=False):
        """Save a checkpoint to Fritz.

        Args:
            fritz_api_key (str): Fritz client API key.
            model_uid (str): Fritz Model UID to add new versions to.
            keras_filename (str): Name of Keras model output filename.
            convert_function (func): Function used to convert Keras model
                to mobile model.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(FritzMLModelCheckpoint, self).__init__(
            fritz_api_key,
            model_uid,
            _SupportedMobileModelTypes.CORE_ML,
            keras_filename,
            convert_function,
            period=period,
            deploy=deploy)


class FritzTFMobileModelCheckpoint(_FritzModelCheckpointBase):
    """Saves current Keras model as a new TensorFlow Mobile model in Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 keras_filename,
                 convert_function,
                 period=1,
                 deploy=False):
        """Save a checkpoint to Fritz.

        Args:
            fritz_api_key (str): Fritz client API key.
            model_uid (str): Fritz Model UID to add new versions to.
            keras_filename (str): Name of Keras model output filename.
            convert_function (func): Function used to convert Keras model
                to mobile model.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(FritzTFMobileModelCheckpoint, self).__init__(
            fritz_api_key,
            model_uid,
            _SupportedMobileModelTypes.TENSORFLOW_MOBILE,
            keras_filename,
            convert_function,
            period=period,
            deploy=deploy)


class FritzTFLiteModelCheckpoint(_FritzModelCheckpointBase):
    """Saves current Keras model as a new TensorFlow Lite model in Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 keras_filename,
                 convert_function,
                 period=1,
                 deploy=False):
        """Save a checkpoint to Fritz.

        Args:
            fritz_api_key (str): Fritz client API key.
            model_uid (str): Fritz Model UID to add new versions to.
            keras_filename (str): Name of Keras model output filename.
            convert_function (func): Function used to convert Keras model
                to mobile model.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(FritzTFLiteModelCheckpoint, self).__init__(
            fritz_api_key,
            model_uid,
            _SupportedMobileModelTypes.TENSORFLOW_LITE,
            keras_filename,
            convert_function,
            period=period,
            deploy=deploy)
