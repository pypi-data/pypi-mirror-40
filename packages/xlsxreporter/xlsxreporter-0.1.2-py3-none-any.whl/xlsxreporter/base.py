import enum
import io

import xlsxwriter

from .utils import row_renderer


class BaseReport:
    class Orientation(enum.Enum):
        PORTRAIT = enum.auto()
        LANDSCAPE = enum.auto()

    class Paper(enum.Enum):
        DEFAULT = 0
        A3 = 8
        A4 = 9

    class Format(enum.Enum):
        def __or__(self, other):
            return {**self.value, **other.value}

    title = "Untitled report"
    orientation = Orientation.LANDSCAPE
    paper = Paper.A4

    num_header_rows = None
    print_columns = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def render(self, workbook, *, title):
        """
        The main render function, which adds a Worksheet to the given Workbook,
        rendering it row by row using generate_rows.
        """

        def add_format(fmt):
            return self.add_format(workbook, fmt)

        worksheet = workbook.add_worksheet(title)
        worksheet.set_paper(self.paper)

        if self.orientation == self.Orientation.LANDSCAPE:
            worksheet.set_landscape()

        # Run through generated rows, passing the sheet with the current row index
        worksheet.row = 0
        for renderer in self.generate_rows(**self.kwargs):
            row_delta = renderer(ctx=worksheet, add_format=add_format)
            worksheet.row += row_delta if row_delta is not None else 1

        if self.print_columns is not None:
            worksheet.print_area(0, 0, worksheet.row - 1, self.print_columns - 1)
            worksheet.fit_to_pages(1, 0)

        if self.num_header_rows:
            worksheet.repeat_rows(0, self.num_header_rows - 1)

    def add_format(self, workbook, fmt):
        """
        Adds the given format definition to the workbook, returning a Format object
        for use in rendering.
        """

        fmt_def = fmt.value if isinstance(fmt, self.Format) else fmt
        return workbook.add_format(fmt_def)

    def generate_rows(self, **kwargs):
        """
        Subclasses should implement a generator generating function thunks conforming
        to the interface defined by the row_renderer decorator.
        """

        raise NotImplementedError

    @row_renderer
    def render_empty(self, *, ctx, add_format):
        """
        Renders an empty row.
        """


class ReportContext(object):
    """
    Base wrapper model handling Workbook objects and IO.

    Usage:

    >>> context = ReportContext("foo.xlsx")
    >>> with context:
    ...     context.add_report(SomeReport())
    >>> instanceof(context.data, io.BytesIO)
    True
    """

    def __init__(self, filename="report.xlsx", outfile=None, **kwargs):

        self.report_titles = set()

        self.filename = filename

        # If provided, writes data to the given file descriptor
        self.outfile = outfile

        # Passed on to the Workbook instance
        wb_options = kwargs.get("wb_options", {})

        # Force running in-memory to speed things up
        wb_options.update({"in_memory": True})

        # After calling close, data will be populated with XLSX data
        self.data = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.data, wb_options)

    ####################
    # Report rendering #
    ####################

    def get_report_title(self, report):
        """
        Ensures a unique report title by appending a number in case of duplicates.
        """

        max_length = 31

        report_title = report.title[:max_length]
        i = 2
        while report_title in self.report_titles:
            report_title = f"{report_title[:max_length-4]} ({i})"
            i += 1

        return report_title

    def add_report(self, report):
        """
        Renders a report into a new worksheet in the workbook.
        """

        report_title = self.get_report_title(report)

        report.render(self.workbook, title=report_title)

        self.report_titles.add(report_title)

    ###################
    # Context manager #
    ###################

    def close(self):
        if self.workbook:
            self.workbook.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        """
        Closes the workbook and rewinds the BytesIO data instance, preparing it for
        reading.

        If an outfile is provided, the data is flushed to it.
        """

        self.close()
        self.data.seek(0)

        if self.outfile:
            self.outfile.write(self.data.getvalue())
