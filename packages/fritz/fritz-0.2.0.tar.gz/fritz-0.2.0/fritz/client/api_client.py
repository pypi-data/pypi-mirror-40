"""
fritz.client.api_client
~~~~~~~~~~~~~~~~~~~~~~~
This module contains the FritzClient for interacting with the Fritz API.
"""

import json
import io
import os

import requests


class FritzClientBase(object):
    """Fritz Client to interact with Fritz API."""

    _ALLOWED_MODEL_EXTENSIONS = ['.tflite', '.mlmodel', '.pb']

    def __init__(self, api_key, base_url):
        """
        Args:
            api_key (str): Account API Key for Fritz API.
            base_url (str): URL base of Fritz API.
        """
        self._api_key = api_key
        self._base_url = base_url

    @staticmethod
    def _create_streamable_mlmodel(model):
        """Convert mlmodel model into BytesIO object ready for streaming.

        Args:
            model (coremltools.models.MLModel): Model to upload
        """
        serialized_spec = model.get_spec().SerializeToString()
        return io.BytesIO(serialized_spec)

    def _check_valid_model_extension(self, model_path):
        """Verifies model path is valid to upload.

        Args:
            model_path (str): Model path to validate.

        Raises:
            ValueError if model extension not valid.
        """
        _, extension = os.path.splitext(model_path)
        if extension not in self._ALLOWED_MODEL_EXTENSIONS:
            message = ("Extension of model must be "
                       "{valid_extensions}, not {extension}")
            raise ValueError(
                message.format(
                    valid_extensions=', '.join(self._ALLOWED_MODEL_EXTENSIONS),
                    extension=extension
                )
            )

    def _upload_model(self,
                      model_uid,
                      model_name,
                      data,
                      set_active,
                      metadata):
        """Uploads model to Fritz API.

        Args:
            model_uid (str): model_uid to update.
            model_name (str): Basename of model to upload.
            data (BinaryIO): File object containing model data to upload.
            set_active (bool): If True, will set active version of model to
                newly uploaded model.
            metadata (Optional[Dict]): Dictionary of metadata about model.

        Returns: Dict of response data.
        """
        path = os.path.join(
            self._base_url,
            'client/v1/model/{model_uid}/version'.format(model_uid=model_uid)
        )
        response = requests.post(
            path,
            headers={
                'Authorization': self._api_key,
            },
            data={
                'metadata_json': json.dumps(metadata or {}),
                'set_active': set_active,
            },
            files={'file': (model_name, data)}
        )

        data.close()
        return response.json()

    def upload_new_version_from_file(self,
                                     model_uid,
                                     model_path,
                                     set_active=False,
                                     metadata=None):
        """Upload new version of a model from a model stored on disk.

        Use to upload new versions of Core ML, TensorFlow Lite, or TensorFlow
        Mobile models. Can choose if you want to deploy the model to all
        devices or just upload to the webapp.

        Args:
            model_uid (str): Model Identifier to update.
            model_path (str): Path to saved model. If model is not provided,
                model will be loaded from this path. Must be a Core ML,
                TensorFlow Lite, or TensorFlow Mobile model.
            set_active (bool): If True, will set active version of model to
                newly uploaded model.
            metadata (Dict): Dictionary of JSON serializable metadata about
                model.

        Returns: Model and ModelVersion of uploaded model.

        Raises: ValueError if model_path does not have a valid extension.
        """
        self._check_valid_model_extension(model_path)
        data = open(model_path, 'rb')
        return self._upload_model(
            model_uid,
            os.path.basename(model_path),
            data,
            set_active,
            metadata
        )

    def upload_new_version(self,
                           model_uid,
                           uploaded_model_name,
                           model,
                           set_active=False,
                           metadata=None):
        """Upload new version of a model from an instantiated model in memory.

        Use to upload new versions of Core ML, TensorFlow Lite, or TensorFlow
        Mobile models. You can choose if you want to deploy the model to all
        devices or just upload to the webapp.

        If you are using a TensorFlow Lite model, make sure that the model is
        the output from the converter.  This should be a `bytes` object of a
        flat buffer.

        Args:
            model_uid (str): Model Identifier to update.
            uploaded_model_name (str): Name of model to save (must contain
                model extension, e.g. `mymodel.mlmodel`).
            model (Union[coremltools.models.MLModel, bytes]): Model file to
                upload. Must be an instantiated Core ML, TensorFlow Lite, or
                TensorFlow Mobile model.
            set_active (bool): If True, will set active version of model to
                newly uploaded model.
            metadata (Dict): Dictionary of JSON serializable metadata about
                model.

        Returns: Model and ModelVersion of uploaded model.

        Raises:
            ValueError: `model_name` does not have the correct extension or
                `model` is not the correct type.
        """
        self._check_valid_model_extension(uploaded_model_name)

        if isinstance(model, bytes):
            data = io.BytesIO(model)
        # Very hacky way to check if model is a Core ML Model. However, I
        # don't want to add a dependency on coremltools for the client,
        # so adding a simple check.
        elif 'MLModel' in str(type(model)):
            data = self._create_streamable_mlmodel(model)
        else:
            msg = "Provided model was {type}, must be {allowed_types}"
            raise ValueError(
                msg.format(
                    type=type(model),
                    allowed_types=', '.join(
                        ['`coremltools.models.MLModel`', '`bytes`']
                    )
                )
            )

        return self._upload_model(
            model_uid,
            uploaded_model_name,
            data,
            set_active,
            metadata
        )


class FritzClient(FritzClientBase):
    """Client used to interact with the Fritz API."""

    API_PATH = 'https://api.fritz.ai'

    def __init__(self, api_key):
        super(FritzClient, self).__init__(api_key, self.API_PATH)
