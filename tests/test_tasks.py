def test_http_health_status(client):
    assert client.get("/health").status_code == 200


def test_contrato_json_health(client):
    assert client.get("/health").get_json() == {"status": "healthy"}


def test_validacion_tarea_vacia(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
    assert response.get_json()["error"] == "title required"


def test_integracion_crear_y_consultar_tarea(client):
    creada = client.post("/tasks", json={"title": "Configurar CI"})
    assert creada.status_code == 201
    task_id = creada.get_json()["id"]
    consultada = client.get(f"/tasks/{task_id}")
    assert consultada.status_code == 200
    assert consultada.get_json()["title"] == "Configurar CI"
