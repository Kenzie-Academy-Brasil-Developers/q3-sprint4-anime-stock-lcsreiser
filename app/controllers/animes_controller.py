from http import HTTPStatus
from flask import request
from app.models.animes_models import Animes
from psycopg2.errors import UniqueViolation
from xml.dom import NotFoundErr

keys = ["id", "anime", "seasons", "released_date"]
keys_acceptable = ["anime", "seasons", "released_date"]
keys_str = ", ".join(keys_acceptable)


# CREATE TABLE
def table_controller():
    return Animes.table_models()


# CREATE
def create_controller():
    try:
        table_controller()
        data = request.get_json()

        if len(data) > 3:
            return {
                "error": f"You are sending 4 or more datas, the acceptable are: {keys_str}"
            }

        payload = Animes(**data)

        created_animes = Animes.create_animes(payload)

        animes = dict(zip(keys, created_animes))

        animes["released_date"] = animes["released_date"].strftime("%d/%m/%Y")

        return animes, HTTPStatus.CREATED

    except UniqueViolation:
        return {"error": "This anime has already been added"}, HTTPStatus.CONFLICT

    except:
        keys_user_send = list(data.keys())

        wrong_key = []
        for key in keys_user_send:
            if key not in keys:
                wrong_key.append(key)

        return {
            "error": f"The acceptable keys are: {keys_str}, and you sent a key/keys named {wrong_key} what not acceptable"
        }, HTTPStatus.UNPROCESSABLE_ENTITY


# GET ALL
def get_controller():
    try:
        table_controller()
        data = Animes.get_animes()

        if len(data) == 0:
            return {"data": (data)}, HTTPStatus.OK

        animes = []

        for anime in data:
            animes.append(dict(zip(keys, anime)))

        for anime in animes:
            anime["released_date"] = anime["released_date"].strftime("%d/%m/%Y")

        return {"data": (animes)}, HTTPStatus.OK

    except:
        return {"error": "Error"}, HTTPStatus.NOT_FOUND


# GET ID
def get_by_id_controller(anime_id):
    try:
        table_controller()
        data = Animes.get_by_id_animes(anime_id)

        animes = dict(zip(keys, data))

        animes["released_date"] = animes["released_date"].strftime("%d/%m/%Y")

        return {"data": (animes)}, HTTPStatus.OK

    except:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND


# PATCH ID
def patch_controller(anime_id):

    data = request.get_json()
    wrong_keys = [key for key in data.keys() if key not in keys_acceptable]
    anime = Animes.get_by_id_animes(anime_id)

    try:

        if wrong_keys:
            raise KeyError
        if not anime:
            raise NotFoundErr

        patch_anime = Animes.patch_anime(data, anime_id)

        animes = dict(zip(keys, patch_anime))

        animes["released_date"] = animes["released_date"].strftime("%d/%m/%Y")

        return {"data": (animes)}, HTTPStatus.OK

    except KeyError:
        return {
            "error": f"The acceptable keys are: {keys_str}, and you sent a key/keys named {wrong_keys} what not acceptable"
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except NotFoundErr:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND


# DELETE ID
def delete_controller(anime_id):
    anime = Animes.get_by_id_animes(anime_id)
    try:
        if not anime:
            raise NotFoundErr
        Animes.delete_anime(anime_id)
        return "", HTTPStatus.NO_CONTENT
    except NotFoundErr:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
