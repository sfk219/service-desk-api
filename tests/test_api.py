from fastapi.testclient import TestClient
from app import main
def test_create_update_delete(tmp_path,monkeypatch):
    monkeypatch.setattr(main,"DB",str(tmp_path/"tickets.db"))
    c=TestClient(main.app)
    r=c.post("/tickets",json={"title":"Fix staging alert","category":"platform","priority":"high"})
    assert r.status_code==201
    id=r.json()["id"]
    assert c.get(f"/tickets/{id}").json()["status"]=="open"
    assert c.patch(f"/tickets/{id}",json={"status":"resolved"}).json()["status"]=="resolved"
    assert c.delete(f"/tickets/{id}").status_code==204
    assert c.get(f"/tickets/{id}").status_code==404
