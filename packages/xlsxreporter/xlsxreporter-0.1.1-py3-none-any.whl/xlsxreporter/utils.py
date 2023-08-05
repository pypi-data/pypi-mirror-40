import functools

from xlsxwriter.utility import xl_rowcol_to_cell as cell

__all__ = ["cell", "row_renderer"]


def row_renderer(func):
    """
    Outer decorator. Func should accept a context, and any other arbitrary arguments
    passed at call time.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        """
        Function returned to the call site.
        """

        def renderer_func(*, ctx, add_format):
            """
            The function thunk to pass to the renderer, which takes a context in
            addition to the user-defined arguments.
            """

            return func(*args, ctx=ctx, add_format=add_format, **kwargs)

        return renderer_func

    return inner
