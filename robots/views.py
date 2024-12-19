import json
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from robots.models import Robot
from .validators import validate_robot_data
from .services import generate_excel_report


@csrf_exempt
@require_http_methods(["POST"])
def create_robot(request):
    try:
        data = json.loads(request.body)

        validation_result = validate_robot_data(data)
        if not validation_result['is_valid']:
            return JsonResponse({
                'error': validation_result['errors']
            }, status=400)

        robot = Robot.objects.create(
            model=data['model'],
            version=data['version'],
            created=datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S')
        )

        return JsonResponse({
            'id': robot.id,
            'serial': f"{robot.model}-{robot.version}"
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
