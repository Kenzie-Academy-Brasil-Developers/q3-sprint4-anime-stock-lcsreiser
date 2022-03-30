import psycopg2
import os
from psycopg2 import sql

HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


class Animes:
    def __init__(self, **kwargs):
        self.anime = kwargs["anime"].title()
        self.seasons = kwargs["seasons"]
        self.released_date = kwargs["released_date"]

    # CREATE TABLE
    def table_models():
        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        create_table = """
                CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                seasons INTEGER NOT NULL,
                released_date DATE NOT NULL
            );
            """

        cur = conn.cursor()

        cur.execute(create_table)

        conn.commit()

        cur.close()
        conn.close()

    # CREATE ANIME
    def create_animes(payload):
        data = payload.__dict__

        new_anime = (
            data["anime"],
            data["seasons"],
            data["released_date"],
        )

        query = """
            INSERT INTO animes (anime, seasons, released_date)
            VALUES (%s, %s, %s)
            RETURNING *
        """

        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        cur = conn.cursor()

        cur.execute(query, new_anime)

        conn.commit()

        created_animes = cur.fetchone()

        cur.close()
        conn.close()

        return created_animes

    # GET ALL
    def get_animes():
        query = "SELECT * FROM animes"

        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        cur = conn.cursor()

        cur.execute(query)

        data = cur.fetchall()

        cur.close()
        conn.close()

        return data

    # GET ID
    def get_by_id_animes(anime_id):
        query = f"SELECT * FROM animes WHERE id = {anime_id}"

        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        cur = conn.cursor()

        cur.execute(query)

        data = cur.fetchone()

        cur.close()
        conn.close()

        return data

    # PATCH ID
    def patch_anime(anime_data, anime_id):
        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        if anime_data.get("anime"):
            anime_data["anime"] = anime_data["anime"].title()

        columns = [sql.Identifier(key) for key in anime_data.keys()]
        values = [sql.Literal(value) for value in anime_data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = row({values})
                WHERE
                    id = {id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cur = conn.cursor()

        cur.execute(query)

        updated_anime = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        return updated_anime

    # DELETE ID
    @staticmethod
    def delete_anime(anime_id):
        conn = psycopg2.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD
        )

        query = "DELETE FROM animes WHERE id = %s"

        cur = conn.cursor()

        cur.execute(query, [anime_id])

        conn.commit()

        cur.close()
        conn.close()
