from datetime import date, timedelta
from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from pathlib import Path

from fastapi.responses import FileResponse, RedirectResponse

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


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/ui")


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


@app.get("/upcoming", response_model=list[Subscription])
def upcoming(days: int = Query(7, ge=1, le=365)):
    today = date.today()
    limit = today + timedelta(days=days)
    result = [s for s in subscriptions if today <= s.next_renewal <= limit]
    return sorted(result, key=lambda s: s.next_renewal)


@app.get("/ui", include_in_schema=False)
def ui():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
