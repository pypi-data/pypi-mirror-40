import json
from typing import Any, Callable, Dict, Union

from .exceptions import UnsupportedMediaType

MediaHandler = Callable[[Any], str]


def handle_json(value: Union[dict, list]) -> str:
    """Serialize a value to a JSON string using `json.dumps()`.

    # Parameters
    value (list or dict): the value to serialize.

    # Returns
    json (str): the serialized value.
    """
    return json.dumps(value)


def handle_text(value: Any) -> str:
    """Serialize a value to plain text using `str()`.

    # Parameters
    value (any): the value to serialize.

    # Returns
    text (str): the serialized value.
    """
    return str(value)


def get_default_handlers() -> dict:
    """Return the built-in media handlers.

    # Returns
    handlers (dict): a mapping of media types to their media handler.
    """
    return {
        Media.JSON: handle_json,
        Media.PLAIN_TEXT: handle_text,
        Media.HTML: handle_text,
    }


class Media:
    """Registry of media handlers.

    # Parameters
    media_type (str):
        The media type that will be used when serializing values.
    handlers (dict):
        A mapping of media types to `(Any) -> str` callables.
        Defaults to built-in media handlers.

    # Attributes
    JSON (str): `application/json`
    PLAIN_TEXT (str): `text/plain`
    HTML (str): `text/html`
    """

    JSON = "application/json"
    PLAIN_TEXT = "text/plain"
    HTML = "text/html"

    def __init__(
        self, media_type: str, handlers: Dict[str, MediaHandler] = None
    ):
        if handlers is None:
            handlers = get_default_handlers()
        self.handlers = handlers
        self.type = media_type

    def serialize(self, value: Any, media_type: str):
        """Serialize a value using the given media type.

        # Parameters
        value (any): the value to be serialized.
        media_type (str):
            The media type of the given value. Determines which media handler
            is used.
        """
        handler = self.handlers[media_type]
        return handler(value)

    @property
    def type(self) -> str:
        """Get or set the configured media type.

        # Parameters
        media_type (str): an HTTP content type.

        # Raises
        UnsupportedMediaType :
            If no handler exists for the given media type.
        """
        return self._default_type

    @type.setter
    def type(self, media_type: str):
        """Set the configured media type."""
        if media_type not in self.handlers:
            raise UnsupportedMediaType(
                media_type, available=list(self.handlers)
            )
        self._default_type = media_type
