import hmac
import hashlib
import json
import os
import time
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Subscription

router = APIRouter()


def verify_signature(payload: bytes, sig_header: str) -> dict:
    secret = os.environ.get('STRIPE_SECRET')
    if not secret:
        raise ValueError('Missing STRIPE_SECRET')
    try:
        parts = dict(item.split('=', 1) for item in sig_header.split(','))
        timestamp = parts['t']
        signature = parts['v1']
    except Exception as e:
        raise ValueError('Malformed Stripe-Signature header') from e

    signed_payload = f"{timestamp}.{payload.decode()}".encode()
    expected_sig = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, signature):
        raise ValueError('Invalid signature')
    event = json.loads(payload.decode())
    return event


def upsert_subscription(db: Session, sub_obj: dict):
    sub = db.get(Subscription, sub_obj['id'])
    if sub is None:
        sub = Subscription(id=sub_obj['id'])
    sub.customer_id = sub_obj.get('customer')
    sub.status = sub_obj.get('status')
    db.add(sub)
    db.commit()


@router.post('/billing/webhook')
async def billing_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    if not sig_header:
        raise HTTPException(status_code=400, detail='Missing signature')
    try:
        event = verify_signature(payload, sig_header)
    except Exception:
        raise HTTPException(status_code=400, detail='Signature verification failed')

    if event.get('type') in (
        'customer.subscription.created',
        'customer.subscription.updated',
    ):
        upsert_subscription(db, event['data']['object'])

    return {'received': True}
