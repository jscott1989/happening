"""Member user profile additions."""
from happening import configuration


class CustomProperties(configuration.CustomProperties):

    """The custom properties added on the admin panel."""

    configuration_variable = "members.configuration.ProfileProperties"
