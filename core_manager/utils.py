import datetime


def validate_and_extract_national_id(national_id):
    """
    Validate an Egyptian national ID and extract birthdate, governorate code, and gender if valid.
    Returns a dict with is_valid, error message, and extracted data (if valid).
    """
    if not national_id or not national_id.isdigit() or len(national_id) != 14:
        return {'is_valid': False, 'error': 'National ID must be 14 digits.', 'data': None}
    try:
        century_map = {'2': 1900, '3': 2000}
        century = century_map.get(national_id[0])
        if not century:
            return {'is_valid': False, 'error': 'Invalid century digit.', 'data': None}
        year = int(national_id[1:3])
        month = int(national_id[3:5])
        day = int(national_id[5:7])
        birth_year = century + year
        birthdate = datetime.date(birth_year, month, day)
        governorate_code = national_id[7:9]
        serial = national_id[9:13]
        gender = 'male' if int(serial) % 2 == 1 else 'female'
        data = {
            'birthdate': birthdate.isoformat(),
            'governorate_code': governorate_code,
            'gender': gender,
        }
        return {'is_valid': True, 'error': None, 'data': data}
    except Exception as e:
        return {'is_valid': False, 'error': 'Invalid national ID format.', 'data': None}
