# working_noban_data/services.py

import csv
import datetime
import math
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  # Adjust permissions as needed
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db import connections
from .serializers import CSVQuerySerializer, CustomQuerySerializer , BookingQuerySerializer

def paginate_data(data, page, items_per_page=10):
    total_count = len(data)
    total_pages = math.ceil(total_count / items_per_page)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_data = data[start:end]
    return paginated_data, total_pages

@extend_schema(
    description='Retrieve Doctors data from the nobaan database. Returns the data as JSON or CSV based on the "csv" parameter. '
                'If a "page" parameter is provided, the JSON response will be paginated (10 items per page) and include pagination details.',
    summary='Get doctors data with a hardcoded query',
    methods=['POST'],
    request=CSVQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_doctors(request):
    serializer = CSVQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        
        query = """SELECT *
FROM general_users
WHERE sd_status = 2
AND sd_kind = 3
AND sd_complete_file_status = 1 ; """
       
        try:
            with connections['nobaan'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response
            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({'return': True, 'data': data})
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})
    
    

@extend_schema(
    description='Retrieve clinics data from the nobaan database. Returns the data as JSON or CSV based on the "csv" parameter. '
                'If a "page" parameter is provided, the JSON response will be paginated (10 items per page) and include pagination details.',
    summary='Get clinics data with a hardcoded query',
    methods=['POST'],
    request=CSVQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_clinics(request):
    serializer = CSVQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        
        query = """SELECT *
FROM book_clinics
 """
       
        try:
            with connections['nobaan'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response
            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({'return': True, 'data': data})
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})
    
    
@extend_schema(
    description=(
        'Retrieve filtered booking data from the nobaan database. The query returns a custom set of columns '
        'from book_booking, general_members, and book_clinics (via book_clinics_doctors) with custom aliases. '
        'It accepts an optional "date" parameter (defaults to today) and returns only bookings with '
        'sd_nobat_status = 2, ordered by sd_date descending. '
        'The response includes the submitted request data and the total booking count for that day.'
    ),
    summary='Get filtered booking data with custom column names',
    methods=['POST'],
    request=BookingQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_bookings(request):
    serializer = BookingQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        # Use provided date or default to today
        date_param = serializer.validated_data.get('date') or datetime.date.today()
        
        # Build the query selecting only the desired columns with custom aliases.
        query = """
            SELECT 
                bb.sd_nobat_date_j AS booking_date_j,
                bb.sd_nobat_time AS booking_time,
                bb.sd_pay_visit AS pay_visit,
                bb.sd_date AS booking_date,
                bb.sd_update AS update_date,
                bb.sd_pay_insurance AS pay_insurance,
                bb.sd_rahgiri AS rahgiri_code,
                bb.sd_pay_doctor AS pay_doctor,
                bb.sd_bime AS bime,
                gm.sd_name AS member_name,
                gm.sd_family AS member_family,
                gm.sd_melicode AS member_melicode,
                gm.sd_mobile AS member_mobile,
                bc.sd_name AS doctor_name
            FROM book_booking bb
            INNER JOIN general_members gm ON bb.sd_uid = gm.sd_id
            INNER JOIN book_clinics_doctors bcd ON bb.sd_cd_id = bcd.sd_id
            LEFT JOIN book_clinics bc ON bcd.sd_cid = bc.sd_id
            WHERE DATE(bb.sd_date) = %s AND bb.sd_nobat_status = 2 
            ORDER BY bb.sd_date DESC
        """
        try:
            with connections['nobaan'].cursor() as cursor:
                # Format the date as YYYY-MM-DD for the query
                cursor.execute(query, [date_param.strftime('%Y-%m-%d')])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            # Format datetime values to match the table's format ("YYYY-MM-DD HH:MM:SS")
            for row in data:
                for key, value in row.items():
                    if isinstance(value, datetime.datetime):
                        row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            
            booking_count = len(data)
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response

            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'submitted_data': serializer.validated_data,
                        'booking_count': booking_count,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({
                        'return': True,
                        'submitted_data': serializer.validated_data,
                        'booking_count': booking_count,
                        'data': data
                    })
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})
    
    
    
@extend_schema(
    description=(
        'Retrieve filtered booking data from the nobaan database. The query returns a custom set of columns '
        'from book_booking, general_members, and book_clinics (via book_clinics_doctors) with custom aliases. '
        'It accepts an optional "date" parameter (defaults to today) and returns only bookings with '
        'sd_nobat_status = 2, ordered by sd_date descending. '
        'The response includes the submitted request data and the total booking count for that day.'
    ),
    summary='Get filtered booking data with custom column names',
    methods=['POST'],
    request=BookingQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_esterdad(request):
    serializer = BookingQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        # Use provided date or default to today
        date_param = serializer.validated_data.get('date') or datetime.date.today()
        
        # Build the query selecting only the desired columns with custom aliases.
        query = """
                    SELECT 
            bb.sd_nobat_date_j AS booking_date_j,
            bb.sd_nobat_time AS booking_time,
            bb.sd_pay_visit AS pay_visit,
            bb.sd_date AS booking_date,
            bb.sd_update AS update_date,
            bb.sd_pay_insurance AS pay_insurance,
            bb.sd_rahgiri AS rahgiri_code,
            bb.sd_pay_doctor AS pay_doctor,
            bb.sd_bime AS bime,
            gm.sd_name AS member_name,
            gm.sd_family AS member_family,
            gm.sd_melicode AS member_melicode,
            gm.sd_mobile AS member_mobile,
            bc.sd_name AS doctor_name
        FROM book_booking bb
        INNER JOIN general_members gm ON bb.sd_uid = gm.sd_id
        INNER JOIN book_clinics_doctors bcd ON bb.sd_cd_id = bcd.sd_id
        LEFT JOIN book_clinics bc ON bcd.sd_cid = bc.sd_id
        WHERE DATE(bb.sd_date) = %s AND bb.sd_back_pos != 1
        ORDER BY bb.sd_date DESC;

        """
        try:
            with connections['nobaan'].cursor() as cursor:
                # Format the date as YYYY-MM-DD for the query
                cursor.execute(query, [date_param.strftime('%Y-%m-%d')])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            # Format datetime values to match the table's format ("YYYY-MM-DD HH:MM:SS")
            for row in data:
                for key, value in row.items():
                    if isinstance(value, datetime.datetime):
                        row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            
            booking_count = len(data)
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response

            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'submitted_data': serializer.validated_data,
                        'booking_count': booking_count,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({
                        'return': True,
                        'submitted_data': serializer.validated_data,
                        'booking_count': booking_count,
                        'data': data
                    })
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})
    
    
@extend_schema(
    description='Retrieve secretaries data from the nobaan database. Returns the data as JSON or CSV based on the "csv" parameter. '
                'If a "page" parameter is provided, the JSON response will be paginated (10 items per page) and include pagination details.',
    summary='Get secretaries data with a hardcoded query',
    methods=['POST'],
    request=CSVQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_secretary(request):
    serializer = CSVQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        
        query = """SELECT *
FROM general_users
WHERE sd_status = 2
AND sd_kind = 2
AND sd_complete_file_status = 1 ; """
       
        try:
            with connections['nobaan'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response
            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({'return': True, 'data': data})
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})

@extend_schema(
    description='Retrieve Users data from the nobaan database. Returns the data as JSON or CSV based on the "csv" parameter. '
                'If a "page" parameter is provided, the JSON response will be paginated (10 items per page) and include pagination details.',
    summary='Get users data with a hardcoded query',
    methods=['POST'],
    request=CSVQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_users(request):
    serializer = CSVQuerySerializer(data=request.data)
    if serializer.is_valid():
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        
        query = "SELECT * FROM general_members"
       
        try:
            with connections['nobaan'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response
            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({'return': True, 'data': data})
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})

@extend_schema(
    description='Retrieve data from the nobaan database using a custom SQL query provided by the user. '
                'Returns the data as JSON or CSV based on the "csv" parameter. If a "page" parameter is provided in the request, '
                'the JSON response will be paginated (10 items per page) and include pagination details.',
    summary='Get Nobaan data with a custom query',
    methods=['POST'],
    request=CustomQuerySerializer,
    responses={200: OpenApiResponse(description='Data retrieved successfully in JSON or CSV format')},
)
@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
def get_nobaan_data_custom(request):
    serializer = CustomQuerySerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data['query']
        csv_flag = serializer.validated_data.get('csv', False)
        page = serializer.validated_data.get('page', None)
        
        try:
            with connections['nobaan'].cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            
            if csv_flag:
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = 'attachment; filename="nobaan_booking_data.csv"'

                # Write the BOM for proper encoding in Excel
                response.write('\ufeff')

                writer = csv.DictWriter(response, fieldnames=columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                return response
            else:
                if page:
                    paginated_data, total_pages = paginate_data(data, page)
                    return JsonResponse({
                        'return': True,
                        'data': paginated_data,
                        'current_page': page,
                        'total_pages': total_pages,
                    })
                else:
                    return JsonResponse({'return': True, 'data': data})
        except Exception as e:
            return JsonResponse({'return': False, 'error': str(e)})
    else:
        return JsonResponse({'return': False, 'error': serializer.errors})
