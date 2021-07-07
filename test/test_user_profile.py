from app.app import app
from app.repository.database import db
from app.repository.user_profile import UserProfile
from datetime import datetime
import pytest
import json
from test.tokens import user1_token


def populate_db():
    user_profile = UserProfile(
        username="user1panda",
        name="TestName1",
        email="TestEmail1",
        phone_number="TestPhoneNumber1",
        birth_date=datetime(2000, 5, 5),
        biography="TestBiography1",
        website="TestWebsite1",
        public=False,
        deleted=False,
        taggable=False,
    )
    db.session.add(user_profile)
    db.session.commit()

    user_profile = UserProfile(
        username="TestUsername2",
        name="TestName2",
        email="TestEmail2",
        phone_number="TestPhoneNumber2",
        birth_date=datetime(2000, 5, 5),
        biography="TestBiography2",
        website="TestWebsite2",
        public=False,
        deleted=False,
        taggable=False,
    )
    db.session.add(user_profile)
    db.session.commit()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    populate_db()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_get_user_profiles_happy(client):
    result = client.get("/user_profile")

    assert len(result.json) == 2


def test_get_user_profile_happy(client):
    result = client.get("/user_profile/user1panda")

    assert result.json["username"] == "user1panda"
    assert result.json["name"] == "TestName1"
    assert result.json["email"] == "TestEmail1"
    assert result.json["phone_number"] == "TestPhoneNumber1"
    assert result.json["birth_date"] is not None
    assert result.json["biography"] == "TestBiography1"
    assert result.json["website"] == "TestWebsite1"
    assert not result.json["public"]
    assert not result.json["deleted"]
    assert not result.json["taggable"]


def test_get_user_profile_sad(client):
    result = client.get("/user_profile/FailUsername1")

    assert result.status_code == 404


def test_create_user_profile_happy(client):
    user_profile = {
        "username": "TestUsername3",
        "name": "TestName3",
        "email": "TestEmail3",
        "phone_number": "TestPhoneNumber3",
        "birth_date": str(datetime(2000, 5, 5)),
        "biography": "TestBiography3",
        "website": "TestWebsite3",
    }

    result = client.post(
        "/user_profile", data=json.dumps(user_profile), content_type="application/json"
    )

    assert result.json["username"] == user_profile["username"]
    assert result.json["name"] == user_profile["name"]
    assert result.json["email"] == user_profile["email"]
    assert result.json["phone_number"] == user_profile["phone_number"]
    assert result.json["birth_date"]
    assert result.json["biography"] == user_profile["biography"]
    assert result.json["website"] == user_profile["website"]
    assert not result.json["public"]
    assert not result.json["deleted"]
    assert not result.json["taggable"]


def test_create_user_sad(client):
    user_profile = {
        "username": "TestUsername3",
        "name": "TestName3",
        "email": "TestEmail3",
        "phone_number": "TestPhoneNumber3",
        "birth_date": str(datetime(2000, 5, 5)),
        "biography": "TestBiography3",
        "website": "TestWebsite3",
        "non-valid-field": "Value",
    }

    result = client.post(
        "/user_profile", data=json.dumps(user_profile), content_type="application/json"
    )
    assert result.status_code == 500


def test_update_user_profile_happy(client):
    user_profile = {
        "username": "user1panda",
        "name": "TestNameChanged",
        "email": "TestEmailChanged",
    }
    result = client.put(
        "/user_profile",
        data=json.dumps(user_profile),
        content_type="application/json",
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert result.json["name"] == "TestNameChanged"
    assert result.json["email"] == "TestEmailChanged"


def test_update_user_profile_sad(client):
    user_profile = {
        "username": "user1panda",
        "name": "TestNameChanged",
        "email": "TestEmailChanged",
    }
    result = client.put(
        "/user_profile",
        data=json.dumps(user_profile),
        content_type="application/json",
    )
    assert result.status_code == 403


def test_delete_user_profile_happy(client):
    result = client.delete(
        "/user_profile/user1panda",
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert result.status_code == 200


def test_delete_user_profile_sad(client):
    result = client.delete(
        "/user_profile/user1panda",
    )
    print(result)
    print(result.json)
    assert result.status_code == 403
