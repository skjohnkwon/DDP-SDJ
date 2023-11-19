import requests

for i, x in enumerate(range(21)):

    int_to_str = str(i).zfill(4)

    # Correctly structured data as a dictionary
    data = {
        "username": f"user{int_to_str}",
        "email": f"{int_to_str}@email.com",
        "password": "123456789",
        "first_name": "user",
        "last_name": f"{int_to_str}"
    }

    print(data)

    # Using the json parameter to send the request
    response = requests.post('http://127.0.0.1:8000/register/', json=data)

    # Print the response
    print(response)