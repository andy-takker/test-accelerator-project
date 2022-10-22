import pytest


@pytest.mark.parametrize(
    argnames=["limit", "offset", "status_code", "msg"],
    argvalues=(
        (50, 0, 200, None),
        (50, None, 200, "field required"),
        (50.1, None, 422, "value is not a valid integer"),
        (101, 10, 422, "ensure this value is less than or equal to 100"),
    ),
)
def test_get_all_users_various(test_client, limit, offset, status_code: int, msg: str):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    response = test_client.get("/users/", params=params)
    assert response.status_code == status_code
    json_data = response.json()
    if response.ok:
        for key in ["items", "limit", "offset", "total"]:
            assert key in json_data.keys()
        assert isinstance(json_data["items"], list)
        assert isinstance(json_data["limit"], int)
        assert isinstance(json_data["offset"], int)
        assert isinstance(json_data["total"], int)

    else:
        json_data["detail"][0]["msg"] == msg
