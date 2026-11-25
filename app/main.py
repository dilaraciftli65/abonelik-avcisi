from datetime import date
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Abonelik Avcısı")


class BillingCycle(str, Enum):
    monthly = "monthly"
    yearly = "yearly"


class SubscriptionIn(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    billing_cycle: BillingCycle
    next_renewal: date


class Subscription(SubscriptionIn):
    id: int


# Basitlik için veriler bellekte tutulur
subscriptions: list[Subscription] = []


@app.get("/")
def root():
    return {"mesaj": "Abonelik Avcısı çalışıyor"}


@app.post("/subscriptions", response_model=Subscription, status_code=201)
def add_subscription(data: SubscriptionIn):
    sub = Subscription(id=len(subscriptions) + 1, **data.model_dump())
    subscriptions.append(sub)
    return sub


@app.get("/subscriptions", response_model=list[Subscription])
def list_subscriptions():
    return subscriptions


@app.get("/subscriptions/summary")
def summary():
    monthly_total = sum(
        s.price if s.billing_cycle == BillingCycle.monthly else s.price / 12
        for s in subscriptions
    )
    return {
        "subscription_count": len(subscriptions),
        "monthly_total": round(monthly_total, 2),
        "yearly_total": round(monthly_total * 12, 2),
    }