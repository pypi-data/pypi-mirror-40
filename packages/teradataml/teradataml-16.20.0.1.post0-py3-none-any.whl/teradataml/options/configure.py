"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: karthik.thelukuntla@teradata.com
Secondary Owner:

This file is for providing user configurable options.
"""

class _Configure(object):
    """
    Options to configure database related values.
    """

    def __init__(self, default_varchar_size=1024):
        self.default_varchar_size = default_varchar_size

        # internal configurations
        # These configurations are internal and should not be
        # exported to the user's namespace.

        self._validate_metaexpression = False  # See ELE-995 for more information

    @property
    def default_varchar_size(self):
        """
        It is required to mention size of varchar datatype in Teradata Vantage, the default size is 1024.
        User can configure this parameter using options.
        Example:
            teradataml.options.configure.default_varchar_size = 512
        """
        return self.__default_varchar_size

    @default_varchar_size.setter
    def default_varchar_size(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('default_varchar_size must be a positive int.')

        self.__default_varchar_size = value

configure = _Configure()
