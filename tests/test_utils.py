from fastapi import status


def create_table_configuration(client) -> dict:
    base_url = "/table-configurations/"
    response = client.post(
        base_url,
        json={
            "name": "sample_table",
            "years_to_collect": 5,
            "created_by": 1,
            "columns": [
                {
                    "name": "Sample Column 1",
                    "column_order": 1,
                    "column_constraint": {
                        "constraint_type": "PICKLIST",
                        "parameters": {"options": ["corn", "wheat", "barley", "hops"]},
                    },
                },
                {
                    "name": "Sample Column 2",
                    "column_order": 2,
                    "column_constraint": {
                        "constraint_type": "FLOAT",
                        "parameters": {"number": 3.14},
                    },
                },
                {
                    "name": "Sample Column 3",
                    "column_order": 3,
                    "column_constraint": {
                        "constraint_type": "RANGE",
                        "parameters": {"min": 1.0, "max": 10.0},
                    },
                },
                {
                    "name": "Sample Column 4",
                    "column_order": 4,
                    "column_constraint": {
                        "constraint_type": "REGEX",
                        "parameters": {"pattern": "^[a-zA-Z]+$"},
                    },
                },
                {
                    "name": "Sample Column 5",
                    "column_order": 5,
                    "column_constraint": {"constraint_type": "BOOL"},
                },
            ],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()
