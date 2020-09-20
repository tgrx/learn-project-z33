import os
import sys


def get_dynaconf_env():
    var_name = "ENV_FOR_DYNACONF"
    default_env = "development"

    try:
        from dynaconf import settings
        env = settings.get(var_name)
    except ImportError:
        env = os.getenv(var_name)

    return env or default_env


def get_base_prefix_compat():
    """
    Get base/real prefix, or sys.prefix if there is none.
    """

    prefix = (
            getattr(sys, "base_prefix", None)
            or getattr(sys, "real_prefix", None)
            or sys.prefix
    )

    return prefix


def in_virtualenv():
    env = get_dynaconf_env()
    if env == "heroku":
        return True
    return get_base_prefix_compat() != sys.prefix


print(in_virtualenv())
