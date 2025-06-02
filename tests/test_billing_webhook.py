import os
import json
import time
import hmac
import hashlib
from fastapi.testclient import TestClient

from api.main import app
from api.database import SessionLocal, engine, Base
from api.models import Subscription

Base.metadata.create_all(bind=engine)

client = TestClient(app)

os.environ['STRIPE_SECRET'] = 'whsec_testsecret'


def sign(payload: str, secret: str, timestamp: int) -> str:
    signed_payload = f"{timestamp}.{payload}".encode()
    signature = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={signature}"


def test_subscription_created_and_updated():
    payload = {
        "id": "evt_1",
        "type": "customer.subscription.created",
        "data": {"object": {"id": "sub_1", "customer": "cus_1", "status": "active"}},
    }
    body = json.dumps(payload)
    ts = int(time.time())
    sig = sign(body, os.environ['STRIPE_SECRET'], ts)
    res = client.post(
        "/billing/webhook",
        data=body,
        headers={"Stripe-Signature": sig, "Content-Type": "application/json"},
    )
    assert res.status_code == 200
    db = SessionLocal()
    sub = db.query(Subscription).filter_by(id="sub_1").first()
    assert sub is not None
    assert sub.status == "active"
    db.close()

    # send update event
    payload["type"] = "customer.subscription.updated"
    payload["data"]["object"]["status"] = "canceled"
    body = json.dumps(payload)
    ts = int(time.time())
    sig = sign(body, os.environ['STRIPE_SECRET'], ts)
    res = client.post(
        "/billing/webhook",
        data=body,
        headers={"Stripe-Signature": sig, "Content-Type": "application/json"},
    )
    assert res.status_code == 200
    db = SessionLocal()
    sub = db.query(Subscription).filter_by(id="sub_1").first()
    assert sub.status == "canceled"
    db.close()


def test_invalid_signature():
    payload = json.dumps({"hello": "world"})
    ts = int(time.time())
    sig = sign(payload, "wrong_secret", ts)
    res = client.post(
        "/billing/webhook",
        data=payload,
        headers={"Stripe-Signature": sig, "Content-Type": "application/json"},
    )
    assert res.status_code == 400
