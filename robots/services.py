import pandas as pd
from io import BytesIO
from django.db.models import Count
from .models import Robot


def generate_excel_report(start_date, end_date):
    robots = Robot.objects.filter(
        created__range=(start_date, end_date)
    ).values(
        'model', 'version'
    ).annotate(
        count=Count('id')
    ).order_by('model', 'version')

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df = pd.DataFrame(list(robots))

        if not df.empty:
            unique_models = df['model'].unique()
            for model in unique_models:
                model_data = df[df['model'] == model].copy()
                model_data.reset_index(drop=True, inplace=True)
                worksheet_data = pd.DataFrame({
                    'Модель': model_data['model'],
                    'Версия': model_data['version'],
                    'Количество за неделю': model_data['count']
                })
                worksheet_data.to_excel(
                    writer,
                    sheet_name=f"Model {model}",
                    index=False
                )
        else:
            pd.DataFrame({
                'Модель': [],
                'Версия': [],
                'Количество за неделю': []
            }).to_excel(
                writer,
                sheet_name="No Data",
                index=False
            )

    output.seek(0)
    return output
