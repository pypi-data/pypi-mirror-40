import os
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple, Type, Union, Callable

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.wsgi import WSGIResponder
from starlette.testclient import TestClient
from starlette.websockets import WebSocketClose
from uvicorn.main import get_logger, run
from uvicorn.reloaders.statreload import StatReload

from .app_types import ASGIApp, ASGIAppInstance, WSGIApp, Scope
from .compat import call_async
from .constants import DEFAULT_CORS_CONFIG
from .error_handlers import ErrorHandler, error_to_text
from .events import EventsMixin
from .exceptions import HTTPError
from .media import Media
from .meta import DocsMeta
from .middleware import Dispatcher
from .recipes import RecipeBase
from .redirection import Redirection
from .request import Request
from .response import Response
from .routing import RoutingMixin, RouteMatch, WebSocketRouteMatch
from .staticfiles import static
from .templates import TemplatesMixin
from .websockets import WebSocket


class API(TemplatesMixin, RoutingMixin, EventsMixin, metaclass=DocsMeta):
    """The all-mighty API class.

    This class implements the [ASGI](https://asgi.readthedocs.io) protocol.

    # Example

    ```python
    >>> import bocadillo
    >>> api = bocadillo.API()
    ```

    # Parameters

    templates_dir (str):
        The name of the directory where templates are searched for,
        relative to the application entry point.
        Defaults to `"templates"`.
    static_dir (str):
        The name of the directory containing static files, relative to
        the application entry point. Set to `None` to not serve any static
        files.
        Defaults to `"static"`.
    static_root (str):
        The path prefix for static assets.
        Defaults to `"static"`.
    allowed_hosts (list of str, optional):
        A list of hosts which the server is allowed to run at.
        If the list contains `"*"`, any host is allowed.
        Defaults to `["*"]`.
    enable_cors (bool):
        If `True`, Cross Origin Resource Sharing will be configured according
        to `cors_config`. Defaults to `False`.
        See also [CORS](../guides/http/middleware.md#cors).
    cors_config (dict):
        A dictionary of CORS configuration parameters.
        Defaults to `dict(allow_origins=[], allow_methods=["GET"])`.
    enable_hsts (bool):
        If `True`, enable HSTS (HTTP Strict Transport Security) and automatically
        redirect HTTP traffic to HTTPS.
        Defaults to `False`.
        See also [HSTS](../guides/http/middleware.md#hsts).
    enable_gzip (bool):
        If `True`, enable GZip compression and automatically
        compress responses for clients that support it.
        Defaults to `False`.
        See also [GZip](../guides/http/middleware.md#gzip).
    gzip_min_size (int):
        If specified, compress only responses that
        have more bytes than the specified value.
        Defaults to `1024`.
    media_type (str):
        Determines how values given to `res.media` are serialized.
        Can be one of the supported media types.
        Defaults to `"application/json"`.
        See also [Media](../guides/http/media.md).
    """

    _error_handlers: List[Tuple[Type[Exception], ErrorHandler]]

    def __init__(
        self,
        templates_dir: str = "templates",
        static_dir: Optional[str] = "static",
        static_root: Optional[str] = "static",
        allowed_hosts: List[str] = None,
        enable_cors: bool = False,
        cors_config: dict = None,
        enable_hsts: bool = False,
        enable_gzip: bool = False,
        gzip_min_size: int = 1024,
        media_type: Optional[str] = Media.JSON,
    ):
        super().__init__(templates_dir=templates_dir)

        self._error_handlers = []
        self.add_error_handler(HTTPError, error_to_text)

        self._extra_apps: Dict[str, Any] = {}

        self.client = self.build_client()

        if static_dir is not None:
            if static_root is None:
                static_root = static_dir
            self.mount(static_root, static(static_dir))

        self._media = Media(media_type=media_type)

        self._middleware = []
        self._asgi_middleware = []

        if allowed_hosts is None:
            allowed_hosts = ["*"]
        self.add_asgi_middleware(
            TrustedHostMiddleware, allowed_hosts=allowed_hosts
        )

        if enable_cors:
            if cors_config is None:
                cors_config = {}
            cors_config = {**DEFAULT_CORS_CONFIG, **cors_config}
            self.add_asgi_middleware(CORSMiddleware, **cors_config)

        if enable_hsts:
            self.add_asgi_middleware(HTTPSRedirectMiddleware)

        if enable_gzip:
            self.add_asgi_middleware(GZipMiddleware, minimum_size=gzip_min_size)

    def build_client(self, **kwargs) -> TestClient:
        return TestClient(self, **kwargs)

    def get_template_globals(self):
        """Return global variables available to all templates.

        # Returns
        variables (dict): a mapping of variable names to their values.
        """
        return {"url_for": self.url_for}

    def mount(self, prefix: str, app: Union[ASGIApp, WSGIApp]):
        """Mount another WSGI or ASGI app at the given prefix.

        # Parameters
        prefix (str): A path prefix where the app should be mounted, e.g. `"/myapp"`.
        app: An object implementing [WSGI](https://wsgi.readthedocs.io) or [ASGI](https://asgi.readthedocs.io) protocol.
        """
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        self._extra_apps[prefix] = app

    def recipe(self, recipe: RecipeBase):
        recipe.apply(self)

    @property
    def media_type(self) -> str:
        """The currently configured media type.

        When setting it to a value outside of built-in or custom media types,
        an `UnsupportedMediaType` exception is raised.
        """
        return self._media.type

    @media_type.setter
    def media_type(self, media_type: str):
        self._media.type = media_type

    @property
    def media_handlers(self) -> dict:
        """The dictionary of supported media handlers.

        You can access, edit or replace this at will.
        """
        return self._media.handlers

    @media_handlers.setter
    def media_handlers(self, media_handlers: dict):
        self._media.handlers = media_handlers

    def add_error_handler(
        self, exception_cls: Type[Exception], handler: ErrorHandler
    ):
        """Register a new error handler.

        # Parameters
        exception_cls (Exception class):
            The type of exception that should be handled.
        handler (callable):
            The actual error handler, which is called when an instance of
            `exception_cls` is caught.
            Should accept a `req`, a `res` and an `exc`.
        """
        self._error_handlers.insert(0, (exception_cls, handler))

    def error_handler(self, exception_cls: Type[Exception]):
        """Register a new error handler (decorator syntax).

        # Example
        ```python
        >>> import bocadillo
        >>> api = bocadillo.API()
        >>> @api.error_handler(KeyError)
        ... def on_key_error(req, res, exc):
        ...     pass  # perhaps set res.content and res.status_code
        ```
        """

        def wrapper(handler):
            self.add_error_handler(exception_cls, handler)
            return handler

        return wrapper

    def _find_handler(
        self, exception_cls: Type[Exception]
    ) -> Optional[ErrorHandler]:
        for cls, handler in self._error_handlers:
            if issubclass(exception_cls, cls):
                return handler
        return None

    async def _handle_exception(
        self, req: Request, res: Response, exception: Exception
    ) -> None:
        # Handle an exception raised during dispatch.
        # If no handler was registered for the exception, it is raised.
        handler = self._find_handler(exception.__class__)
        if handler is None:
            return await self._handle_exception(req, res, HTTPError(500))

        await call_async(handler, req, res, exception)
        if res.status_code is None:
            res.status_code = 500

    def redirect(
        self,
        *,
        name: str = None,
        url: str = None,
        permanent: bool = False,
        **kwargs,
    ):
        """Redirect to another route.

        # Parameters
        name (str): name of the route to redirect to.
        url (str): URL of the route to redirect to, required if `name` is omitted.
        permanent (bool):
            If `False` (the default), returns a temporary redirection (302).
            If `True`, returns a permanent redirection (301).
        kwargs (dict):
            Route parameters.

        # Raises
        Redirection: an exception that will be caught by #API.dispatch().

        # See Also
        - [Redirecting](../guides/http/redirecting.md)
        """
        if name is not None:
            url = self.url_for(name=name, **kwargs)
        else:
            assert url is not None, "url is expected if no route name is given"
        raise Redirection(url=url, permanent=permanent)

    def add_middleware(self, middleware_cls, **kwargs):
        """Register a middleware class.

        # Parameters

        middleware_cls (Middleware class):
            A subclass of `bocadillo.Middleware`.

        # See Also
        - [Middleware](../guides/http/middleware.md)
        """
        self._middleware.insert(0, (middleware_cls, kwargs))

    def add_asgi_middleware(self, middleware_cls, *args, **kwargs):
        """Register an ASGI middleware class.

        # Parameters
        middleware_cls (Middleware class):
            A class that complies with the ASGI specification.

        # See Also
        - [Middleware](../guides/http/middleware.md)
        - [ASGI](https://asgi.readthedocs.io)
        """
        self._asgi_middleware.insert(0, (middleware_cls, args, kwargs))

    def apply_asgi_middleware(self, app: ASGIApp) -> ASGIApp:
        """Wrap the registered ASGI middleware around an ASGI app.

        # Parameters
        app (ASGIApp): a callable complying with the ASGI specification.

        # Returns
        app_with_asgi_middleware (ASGIApp):
            The result `app = asgi(app, *args, **kwargs)` for
            each ASGI middleware class.

        # See Also
        - [add_asgi_middleware](#add-asgi-middleware)
        """
        for middleware_cls, args, kwargs in self._asgi_middleware:
            app: ASGIApp = middleware_cls(app, *args, **kwargs)
        return app

    async def dispatch(self, req: Request) -> Response:
        """Dispatch a request and return a response.

        # Parameters
        req (Request): an inbound HTTP request.

        # Returns
        response (Response): an HTTP response.

        # See Also
        - [How are requests processed?](../guides/http/routing.md#how-are-requests-processed) for the dispatch algorithm.
        """
        res = Response(req, media=self._media)

        try:
            match: RouteMatch = self._router.match(req.url.path)
            if match is None:
                raise HTTPError(status=404)

            try:
                await match.route(req, res, **match.params)
            except Redirection as redirection:
                res = redirection.response

        except Exception as e:
            await self._handle_exception(req, res, e)

        return res

    def _convert_exception_to_response(
        self, dispatch: Dispatcher
    ) -> Dispatcher:
        # Wrap call to `dispatch()` to always return an HTTP response.

        @wraps(dispatch)
        async def inner(req: Request) -> Response:
            try:
                res = await dispatch(req)
            except Exception as exc:
                res = Response(req, media=self._media)
                await self._handle_exception(req, res, exc)
            return res

        return inner

    async def get_response(self, req: Request) -> Response:
        """Return a response for an incoming request.

        # Parameters
        req (Request): a Request object.

        # Returns
        res (Response):
            a Response object, obtained by going down the middleware chain,
            calling `dispatch()` and going up the middleware chain.

        # See Also
        - [dispatch](#dispatch)
        - [Middleware](../guides/http/middleware.md)
        """
        convert = self._convert_exception_to_response
        dispatch = convert(self.dispatch)
        for cls, kwargs in self._middleware:
            middleware = cls(dispatch, **kwargs)
            dispatch = convert(middleware)
        return await dispatch(req)

    async def dispatch_websocket(self, scope: Scope, receive, send):
        match: WebSocketRouteMatch = self._router.match(
            scope["path"], websocket=True
        )
        if match is None:
            # Close with a 403 error code, as specified in the ASGI spec:
            # https://asgi.readthedocs.io/en/latest/specs/www.html#close
            await WebSocketClose(code=403)(receive, send)
        else:
            ws = WebSocket(scope, receive, send, **match.route.ws_kwargs)
            try:
                await match.route(ws, **match.params)
            except BaseException:
                await ws.ensure_closed(1011)
                raise

    def create_app(self, scope: Scope) -> ASGIAppInstance:
        """Build and return an instance of the `API`'s own ASGI application.

        # Parameters
        scope (dict): an ASGI connection scope.

        # Returns
        asgi (ASGIAppInstance):
            creates a `Request` and awaits the result of `get_response()`.
        """

        async def asgi(receive, send):
            nonlocal scope
            if scope["type"] == "websocket":
                await self.dispatch_websocket(scope, receive, send)
            else:
                assert scope["type"] == "http"
                req = Request(scope, receive)
                res = await self.get_response(req)
                await res(receive, send)

        return asgi

    def find_app(self, scope: Scope) -> ASGIAppInstance:
        """Return the ASGI application suited to the given ASGI scope.

        The application is chosen according to the following algorithm:

        - If `scope` has a `lifespan` type, the lifespan handler is returned.
        This occurs on server startup and shutdown.
        - If the scope's `path` begins with any of the prefixes of a mounted
        sub-app, said sub-app is returned (converting from WSGI to ASGI if
        necessary).
        - Otherwise, the `API`'s own ASGI application is returned.

        # Parameters
        scope (dict):
            An ASGI scope.

        # Returns
        app:
            An ASGI application instance.

        # See Also
        - [Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)
        - [ASGI connection scope](https://asgi.readthedocs.io/en/latest/specs/main.html#connection-scope)
        - [Events](../guides/agnostic/events.md)
        - [mount](#mount)
        - [create_app](#create-app)
        """
        if scope["type"] == "lifespan":
            return self.handle_lifespan(scope)

        path: str = scope["path"]

        # Return a sub-mounted extra app, if found
        for prefix, app in self._extra_apps.items():
            if not path.startswith(prefix):
                continue
            # Remove prefix from path so that the request is made according
            # to the mounted app's point of view.
            scope["path"] = path[len(prefix) :]
            try:
                return app(scope)
            except TypeError:
                return WSGIResponder(app, scope)

        return self.apply_asgi_middleware(self.create_app)(scope)

    def run(
        self,
        host: str = None,
        port: int = None,
        debug: bool = False,
        log_level: str = "info",
        _run: Callable = None,
        **kwargs,
    ):
        """Serve the application using [uvicorn](https://www.uvicorn.org).

        # Parameters

        host (str):
            The host to bind to.
            Defaults to `"127.0.0.1"` (localhost).
            If not given and `$PORT` is set, `"0.0.0.0"` will be used to
            serve to all known hosts.
        port (int):
            The port to bind to.
            Defaults to `8000` or (if set) the value of the `$PORT` environment
            variable.
        debug (bool):
            Whether to serve the application in debug mode. Defaults to `False`.
        log_level (str):
            A logging level for the debug logger. Must be a logging level
            from the `logging` module. Defaults to `"info"`.
        kwargs (dict):
            Extra keyword arguments that will be passed to the Uvicorn runner.

        # See Also
        - [Configuring host and port](../guides/api.md#configuring-host-and-port)
        - [Debug mode](../guides/api.md#debug-mode)
        - [Uvicorn settings](https://www.uvicorn.org/settings/) for all
        available keyword arguments.
        """
        if _run is None:  # pragma: no cover
            _run = run

        if "PORT" in os.environ:
            port = int(os.environ["PORT"])
            if host is None:
                host = "0.0.0.0"

        if host is None:
            host = "127.0.0.1"

        if port is None:
            port = 8000

        if debug:
            reloader = StatReload(get_logger(log_level))
            reloader.run(
                run,
                {
                    "app": self,
                    "host": host,
                    "port": port,
                    "log_level": log_level,
                    "debug": debug,
                    **kwargs,
                },
            )
        else:
            _run(self, host=host, port=port, **kwargs)

    def __call__(self, scope: Scope) -> ASGIAppInstance:
        return self.find_app(scope)
