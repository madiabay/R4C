from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .services import generate_excel_report


@require_http_methods(["GET"])
def download_report(request):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        excel_file = generate_excel_report(start_date, end_date)

        response = HttpResponse(
            excel_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=robot_production_report.xlsx'
        return response

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
