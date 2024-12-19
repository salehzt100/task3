import re


def custom_response_error(error_message):
    # Define the regex patterns to capture the required fields
    patterns = [
        r'\(psycopg2\.errors\.(?P<error_type>ForeignKeyViolation)\) insert or update on table "(?P<table>[^"]+)" violates foreign key constraint "(?P<constraint>[^"]+)"\nDETAIL:  Key \((?P<field>[^)]+)\)=\((?P<value>\d+)\) is not present in table "(?P<related_table>[^"]+)"\.\n\n\[SQL: (?P<sql_query>.+?)\]\n\[parameters: {.+?}\]',
        r'\(psycopg2\.errors\.(?P<error_type>ForeignKeyViolation)\) insert or update on table "(?P<table>[^"]+)" violates foreign key constraint "(?P<constraint>[^"]+)"\nDETAIL:  Key \((?P<field>[^)]+)\)=\((?P<value>[^)]+)\) is not present in table "(?P<related_table>[^"]+)"\.\n\n\[SQL: (?P<sql_query>.+?)\]\n\[parameters: {.+?}\]'
    ]

    for pattern in patterns:
        match = re.search(pattern, error_message, re.DOTALL)
        if match:
            error_type = match.group('error_type')  # This will now be just 'ForeignKeyViolation'
            field = match.group('field')
            value = match.group('value')
            table = match.group('table')

            return f"Error Type: {error_type}, Field: {field}, Value: {value}, Table: {table}"

    return "No match found."

