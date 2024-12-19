from datetime import datetime


def validate_robot_data(data):
    errors = []

    required_fields = ['model', 'version', 'created']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if errors:
        return {'is_valid': False, 'errors': errors}

    # Validate model and version length
    if len(data['model']) != 2:
        errors.append("Model must be exactly 2 characters")
    if len(data['version']) != 2:
        errors.append("Version must be exactly 2 characters")

    try:
        datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        errors.append("Invalid date format. Use YYYY-MM-DD HH:MM:SS")

    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }
