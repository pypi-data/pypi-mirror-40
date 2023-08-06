import logging
from copy import deepcopy

from seveno_pyutil import is_blank


class AppContextLoggingFilter(logging.Filter):
    """
    +-------------------------------------+-----------------------------------+
    | placeholder                         | description                       |
    +-------------------------------------+-----------------------------------+
    | %(filter_commander_context)s        | See bellow.                       |
    +-------------------------------------+-----------------------------------+

    These are some examples of rendering that placeholder::

        "[order_id: 42, query_id: abcdef42] "
        "[order_id: 42] "

    In case log record has no data, empty string ``""`` is rendered.

    To handle spacing between this placeholder and subsequent log message use
    it in `logging.Formatter` strings like this (notice there is not space
    between it and following message)::

        "%(filter_commander_context)s%(message)s"
    """

    KEY_ORDER_ID = "order_id"
    KEY_QUERY_ID = "query_id"

    EMPTY_CONTEXT = {KEY_ORDER_ID: None, KEY_QUERY_ID: None}

    def filter(self, record):
        data = [
            "{}: {}".format(attr_name, str(getattr(record, attr_name)).strip())
            for attr_name in [self.KEY_ORDER_ID, self.KEY_QUERY_ID]
            if (
                not is_blank(getattr(record, attr_name, None))
                or getattr(record, attr_name, None) == 0
            )
        ]

        record.filter_commander_context = (
            "[{}] ".format(", ".join(data)) if data else ""
        )

        return True


class AppLoggingContext:
    """
    Encapsulates logging context needed for loggers with
    `.AppContextLoggingFilter` and adapts `logging.Logger` instance to use
    that context.

    Can be used alone or as context manger. If used as context manager, it will
    clean logging context on __exit__.

    Example::

        import logging
        import sys

        from m3p_filter_commander import AppContextLoggingFilter
        from m3p_filter_commander import AppLoggingContext

        handler = logging.StreamHandler(sys.stdout)
        handler.addFilter(AppContextLoggingFilter())
        handler.setFormatter(
            logging.Formatter('%(filter_commander_context)s%(message)s')
        )
        logger = logging.getLogger('foo')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        free_ctx = AppLoggingContext(logger)

        with free_ctx(order_id=42) as ctx:
            ctx.logger.info("ZOMG!")
        # [order_id: 42] ZOMG!

        free_ctx.logger.info("ZOMG!")
        # ZOMG!

        with AppLoggingContext(logger, order_id=42) as ctx:
            ctx.logger.info("ZOMG!")
        # [order_id: 42] ZOMG!

        ctx.logger.info("ZOMG!")
        # ZOMG!
    """

    def __init__(self, logger_or_name, order_id=None, query_id=None):
        self._logging_ctx = deepcopy(AppContextLoggingFilter.EMPTY_CONTEXT)
        self._logger = logging.LoggerAdapter(
            (
                logger_or_name
                if isinstance(logger_or_name, logging.Logger)
                else logging.getLogger(logger_or_name)
            ),
            self._logging_ctx,
        )
        self.order_id = order_id
        self.query_id = query_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self._clear_log_ctx()
        return False

    def __call__(self, order_id=None, query_id=None):
        self.order_id = order_id
        self.query_id = query_id
        return self

    @property
    def order_id(self):
        return self._logging_ctx[AppContextLoggingFilter.KEY_ORDER_ID]

    @order_id.setter
    def order_id(self, rv):
        self._logging_ctx[AppContextLoggingFilter.KEY_ORDER_ID] = rv

    @property
    def query_id(self):
        return self._logging_ctx[AppContextLoggingFilter.KEY_QUERY_ID]

    @query_id.setter
    def query_id(self, rv):
        self._logging_ctx[AppContextLoggingFilter.KEY_QUERY_ID] = rv

    @property
    def logger(self):
        return self._logger

    def _clear_log_ctx(self):
        for k in self._logging_ctx.keys():
            self._logging_ctx[k] = None
