def render_report_context_response(report_context):
    """
    Renders a HttpResponse with the given report context data.
    """

    from django.http import HttpResponse

    response = HttpResponse(
        report_context.data, content_type="application/vnd.ms-excel"
    )

    content_disp = f'attachment; filename="{report_context.filename}"'
    response["Content-Disposition"] = content_disp

    return response
