def test_create_user(
    test_client,
):
    test_user_data = {
        "username": "test_user",
        "age": 18,
    }

    response = test_client.post("/users/", data=test_user_data)
