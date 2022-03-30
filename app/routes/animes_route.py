from app.controllers import animes_controller
from flask import Blueprint

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.post("")(animes_controller.create_controller)
bp.get("")(animes_controller.get_controller)
bp.get("/<int:anime_id>")(animes_controller.get_by_id_controller)
bp.patch("/<int:anime_id>")(animes_controller.patch_controller)
bp.delete("/<int:anime_id>")(animes_controller.delete_controller)
