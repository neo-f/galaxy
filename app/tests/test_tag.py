import asyncio

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from app.models import Tag

faker = Faker()


@pytest.mark.parametrize(
    "model_class, url, create_params, update_params",
    [(Tag, "/tag", {"name": faker.name}, {"name": faker.name})],
)
def test_model_curd(
    client: TestClient, event_loop: asyncio.AbstractEventLoop, model_class, url, create_params, update_params
):  # pylint: disable=too-many-arguments
    # Test Create 1
    create_params1 = {k: v() for k, v in create_params.items()}
    response = client.post(url, json=create_params1)
    assert response.status_code == 200, response.text
    resp = response.json()
    for k, v in create_params1.items():
        assert resp[k] == v
    assert "id" in resp

    # Test Database Object
    async def get_obj(pk):
        return await model_class.filter(id=pk).first()

    obj = event_loop.run_until_complete(get_obj(resp["id"]))
    assert obj.id == resp["id"]

    # Test List

    create_params2 = {k: v() for k, v in create_params.items()}
    client.post(url, json=create_params2)
    response = client.get(url)
    assert response.status_code == 200, response.text
    resp = response.json()
    assert len(resp) == 2
    assert obj.id in [resp[0]["id"], resp[1]["id"]]

    # Test Update
    update_params = {k: v() for k, v in update_params.items()}
    response = client.put(f"{url}/{obj.id}", json=update_params)
    assert response.status_code == 200, response.text
    response = client.get(f"{url}/{obj.id}")
    assert response.status_code == 200, response.text
    for k, v in update_params.items():
        assert response.json()[k] == v
    assert response.json()["id"] == obj.id

    # Test Delete
    response = client.delete(f"{url}/{obj.id}")
    assert response.status_code == 200, response.text
    obj = event_loop.run_until_complete(get_obj(obj.id))
    assert obj is None

    assert len(client.get(url).json()) == 1
