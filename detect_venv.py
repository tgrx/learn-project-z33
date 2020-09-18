import sys


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
    return get_base_prefix_compat() != sys.prefix


print(in_virtualenv())
