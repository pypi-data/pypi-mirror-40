from logging_config.components.default_logging_components import DefaultComponents


class LogConfiguration:

    """
    Base class for creating logging configuration.
    """

    def __init__(self, log_root):
        self.log_root = log_root
        self.filters = DefaultComponents.get_filters()
        self.formatters = DefaultComponents.get_formatters()
        self.handlers = DefaultComponents.get_handlers(log_root)
        self.loggers = DefaultComponents.get_loggers()

    def get(self):
        """
        :returns default configuration:
        """
        config = {
            'version': 1,
            'disable_existing_loggers': True,

            'filters': self.get_filters(),
            'formatters': self.get_formatters(),
            'handlers': self.get_handlers(),
            'loggers': self.get_loggers()
        }
        return config

    def get_filters(self):
        """
        Method can be overridden to add custom filters
        e.g. self.filters.update({'custom_filter_name': {}})
        :returns filters:
        """
        return self.filters

    def get_formatters(self):
        """
        Method can be overridden to add custom formatters
        e.g. self.formatters.update({'custom_formatter_name': {}})
        :return formatters:
        """
        return self.formatters

    def get_handlers(self):
        """
        Method can be overridden to add custom handlers
        e.g. self.handlers.update({'custom_handler_name': {}})
        :return handlers:
        """
        return self.handlers

    def get_loggers(self):
        """
        Method can be overridden to add custom loggers
        e.g. self.loggers.update({'custom_logger_name': {}})
        :return:
        """
        return self.loggers







