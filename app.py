from flask import Flask, jsonify, request
from services.calculator import calcular_total
from services.tasks import TaskService
from services.configuration import cargar_configuracion


def create_app():
    app = Flask(__name__)
    tasks = TaskService()

    @app.get("/health")
    def health():
        return jsonify(status="healthy"), 200

    @app.post("/calculate")
    def calculate():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="JSON object required"), 400
        try:
            total = calcular_total(payload.get("price"), payload.get("quantity"), payload.get("discount", 0))
        except (ValueError, TypeError):
            return jsonify(error="invalid calculation"), 400
        return jsonify(total=str(total)), 200

    @app.post("/tasks")
    def create_task():
        payload = request.get_json(silent=True)
        try:
            task = tasks.create(payload.get("title") if isinstance(payload, dict) else None)
        except ValueError:
            return jsonify(error="title required"), 400
        return jsonify(task), 201

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = tasks.get(task_id)
        return (jsonify(task), 200) if task else (jsonify(error="not found"), 404)

    @app.get("/config")
    def config():
        try:
            settings = cargar_configuracion("config/settings.json")
        except (OSError, ValueError):
            return jsonify(error="invalid configuration"), 500
        return jsonify(settings), 200

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080)
