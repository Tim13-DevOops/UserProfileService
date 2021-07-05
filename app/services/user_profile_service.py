from datetime import datetime
from flask import abort
from app.repository.user_profile import UserProfile
from app.repository.database import db
from app.rbac import rbac
import json


def get_user_profiles(page=1, page_size=10, filter_dict="{}"):
    page = int(page)
    page_size = int(page_size)

    filter_dict = json.loads(filter_dict)
    filter_dict["deleted"] = False

    filters = []

    for k, v in filter_dict.items():
        if type(v) == str:
            filters.append(UserProfile.__dict__[k].like(f"%{v}%"))
        else:
            filters.append(UserProfile.__dict__[k] == v)

    query = (
        UserProfile.query.filter(*filters)
        .order_by(UserProfile.timestamp.desc())
        .paginate(page=page, per_page=page_size)
    )
    total = query.total
    posts = query.items

    return posts


def get_user_profile(username):
    user_profile = UserProfile.query.filter_by(username=username).first()
    if user_profile is None:
        abort(404)
    return user_profile


def create_user_profile(user_profile_dict):
    """
    Create a new profile

    user_profile_dict:
        username: str
        name: str
        email: str
        phone_number: str
        birth_date: datetime
        biography: str
        website: str
    """
    user_profile_dict.pop("id", None)
    user_profile = UserProfile(**user_profile_dict)
    user_profile.timestamp = datetime.now()

    db.session.add(user_profile)
    db.session.commit()
    return user_profile


def update_user_profile(user_profile_dict):
    user = rbac.get_current_user()
    query = UserProfile.query.filter_by(username=user_profile_dict["username"])
    user_profile = query.first()

    if user.id is None:
        abort(403, "No user logged in")

    if user_profile_dict["username"] != user.username:
        abort(400, "Profile does not belong to this user")

    query.update(user_profile_dict)
    db.session.commit()
    return user_profile


def delete_user_profile(username):
    user = rbac.get_current_user()
    query = UserProfile.query.filter_by(username=username)
    user_profile = query.first()

    if user.id is None:
        abort(403, "No user logged in")

    if username != user.username:
        abort(400, "Profile does not belong to this user")

    query.update({"deleted": True})
    db.session.commit()
    return user_profile
