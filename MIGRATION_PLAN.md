# AssetTrack Migration Plan: Vue 2 + Flask → Next.js + FastAPI

## Overview

AssetTrack currently runs on Vue.js 2 (EOL) and Flask with pickle-based storage. This document outlines the plan to migrate to a modern, production-ready stack: **Next.js (React) + FastAPI + SQLite** (upgradeable to PostgreSQL).

The codebase is small (~1,400 lines of actual code), making this a well-scoped migration with clear boundaries.

---

## Current Stack vs Target Stack

| Concern | Current | Target |
|---|---|---|
| Frontend framework | Vue 2.6 (EOL) | Next.js 15 (React 19) |
| Styling | Bootstrap-Vue + jQuery | Tailwind CSS |
| Charts | Chart.js 2 + vue-chartjs | Recharts |
| HTTP client | Axios 0.19 | Native `fetch` (or Axios 1.x) |
| Language | JavaScript | TypeScript |
| Backend framework | Flask + Gevent WSGI | FastAPI + Uvicorn |
| Data persistence | Pickle files | SQLite via SQLAlchemy (async) |
| API docs | None | Auto-generated OpenAPI (Swagger UI) |
| Input validation | None | Pydantic v2 |
| Error codes | 500 for everything | Proper 4xx/5xx |
| Authentication | Hardcoded email | JWT (future phase) |

---

## Phased Delivery Plan

### Phase 1 — Backend Foundation (Week 1–2)

**Goal:** Functional FastAPI app with parity to the current Flask API.

#### 1.1 Project Setup
```
backend/
├── app/
│   ├── main.py            # FastAPI app factory
│   ├── config.py          # Settings via pydantic-settings
│   ├── database.py        # Async SQLAlchemy engine + session
│   ├── models/
│   │   ├── db.py          # ORM table definitions
│   │   └── schemas.py     # Pydantic request/response schemas
│   ├── routers/
│   │   └── portfolio.py   # All /api/* endpoints
│   └── services/
│       └── portfolio.py   # Business logic (totals, net worth)
├── alembic/               # DB migrations
├── tests/
└── requirements.txt
```

#### 1.2 Pydantic Schemas (replacing custom Python classes)

The existing `models.py` classes map cleanly to Pydantic models:

```python
# app/models/schemas.py
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class Currency(str, Enum):
    GBP = "GBP"
    USD = "USD"
    EUR = "EUR"
    INR = "INR"

class OtherItem(BaseModel):
    title: Optional[str] = None
    amount: float = 0

class CashAssets(BaseModel):
    checking_acs: float = 0
    savings_acs: float = 0
    money_market_accounts: float = 0
    savings_bonds: float = 0
    cds: float = 0
    life_insurance: float = 0
    other: OtherItem = OtherItem()

class InvestedAssets(BaseModel):
    brokerage: float = 0
    other_tax: OtherItem = OtherItem()
    ira: float = 0
    roth_ira: float = 0
    k401: float = 0
    sep_ira: float = 0
    keogh: float = 0
    pension: float = 0
    annuity: float = 0
    real_estate: float = 0
    sole_prop: float = 0
    partnership: float = 0
    c_corp: float = 0
    s_corp: float = 0
    limited_liability_company: float = 0
    other_business: OtherItem = OtherItem()

class UseAssets(BaseModel):
    principal_home: float = 0
    vacation_home: float = 0
    vehicles: float = 0
    home_furnishings: float = 0
    arts_and_antiques: float = 0
    jewelry_and_furs: float = 0
    other: OtherItem = OtherItem()

class CurrentLiabilities(BaseModel):
    credit_card_balance: float = 0
    income_tax_owed: float = 0
    other: OtherItem = OtherItem()

class LongTermLiabilities(BaseModel):
    home_mortgage: float = 0
    home_equity_loan: float = 0
    rent_properties_mortgage: float = 0
    car_loans: float = 0
    student_loans: float = 0
    life_insurance_policy_loans: float = 0
    other: OtherItem = OtherItem()

class Portfolio(BaseModel):
    currency: Currency
    cash_assets: CashAssets
    invested_assets: InvestedAssets
    use_assets: UseAssets
    current_liabilities: CurrentLiabilities
    long_term_liabilities: LongTermLiabilities

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
```

#### 1.3 SQLAlchemy ORM Models

```python
# app/models/db.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    portfolio = relationship("Portfolio", back_populates="user", uselist=False)

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    currency = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="portfolio")
    cash_assets = relationship("CashAssets", back_populates="portfolio", uselist=False)
    invested_assets = relationship("InvestedAssets", back_populates="portfolio", uselist=False)
    use_assets = relationship("UseAssets", back_populates="portfolio", uselist=False)
    current_liabilities = relationship("CurrentLiabilities", back_populates="portfolio", uselist=False)
    long_term_liabilities = relationship("LongTermLiabilities", back_populates="portfolio", uselist=False)

# ... one table per asset/liability group (same pattern)
```

#### 1.4 FastAPI Endpoints

All 7 existing endpoints are preserved with corrected HTTP semantics:

| Method | Path | Status codes | Notes |
|---|---|---|---|
| GET | `/` | 200 | Health check |
| POST | `/api/users` | 201, 409 | Duplicate → 409 (was 500) |
| GET | `/api/users/{email}` | 200, 404 | Path param instead of query param |
| PUT | `/api/users/{email}/portfolio` | 200, 404 | Idempotent update |
| GET | `/api/users/{email}/net-worth` | 200, 404 | Returns `{"net_worth": float \| null, "currency": str}` |
| GET | `/api/users/{email}/assets` | 200, 404 | Returns asset breakdown |
| GET | `/api/users/{email}/liabilities` | 200, 404 | Returns liability breakdown |

FastAPI generates interactive docs at `/docs` (Swagger) and `/redoc` automatically.

#### 1.5 Pickle → SQLite Migration Script

A one-time script reads `backend/storage/users.pck` and inserts rows into the new database:

```python
# scripts/migrate_pickle_to_db.py
import pickle
from app.database import SessionLocal
from app import models

with open("backend/storage/users.pck", "rb") as f:
    users = pickle.load(f)

db = SessionLocal()
for legacy_user in users:
    # Map legacy User object → new ORM rows
    ...
db.close()
```

---

### Phase 2 — Frontend Rebuild (Week 2–4)

**Goal:** Next.js app that matches current UI, talks to the new FastAPI backend.

#### 2.1 Project Setup

```
frontend/
├── app/
│   ├── layout.tsx         # Root layout (replaces App.vue + main.js)
│   ├── page.tsx           # Home/dashboard page
│   └── globals.css
├── components/
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── Dashboard.tsx      # Replaces Dashboard.vue
│   └── DonutChart.tsx     # Replaces PieChart.js
├── lib/
│   └── api.ts             # Typed API client
├── types/
│   └── portfolio.ts       # TypeScript interfaces mirroring Pydantic schemas
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

#### 2.2 Key Component Migrations

**`App.vue` → `app/layout.tsx`**

The root layout provides the navbar and footer shell that wraps all pages. Global CSS imports move here.

**`Dashboard.vue` → `components/Dashboard.tsx`**

```tsx
"use client";
import { useEffect, useState } from "react";
import { getNetWorth, getAssets, getLiabilities } from "@/lib/api";
import DonutChart from "./DonutChart";

const DEMO_EMAIL = "john.doe@gmail.com"; // temporary until auth is added

export default function Dashboard() {
  const [netWorth, setNetWorth] = useState<number | null>(null);
  const [currency, setCurrency] = useState("£");

  useEffect(() => {
    getNetWorth(DEMO_EMAIL).then((data) => {
      setNetWorth(data.net_worth);
      setCurrency(data.currency === "GBP" ? "£" : data.currency);
    });
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold">
        Net Worth: {currency}{netWorth?.toLocaleString() ?? "—"}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <DonutChart type="assets" email={DEMO_EMAIL} />
        <DonutChart type="liabilities" email={DEMO_EMAIL} />
      </div>
    </div>
  );
}
```

**`PieChart.js` → `components/DonutChart.tsx`**

Replace `vue-chartjs` Doughnut with `recharts` `PieChart`:

```tsx
"use client";
import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { getAssets, getLiabilities } from "@/lib/api";

const ASSET_COLORS = ["#41B883", "#E46651", "#cc65fe"];
const LIABILITY_COLORS = ["#41B883", "#E46651"];

export default function DonutChart({ type, email }: { type: "assets" | "liabilities"; email: string }) {
  const [data, setData] = useState<{ name: string; value: number }[]>([]);

  useEffect(() => {
    if (type === "assets") {
      getAssets(email).then((d) => {
        if (!d) return;
        setData([
          { name: "Cash", value: d.cash },
          { name: "Personal Use", value: d.use },
          { name: "Invested", value: d.invested },
        ]);
      });
    } else {
      getLiabilities(email).then((d) => {
        if (!d) return;
        setData([
          { name: "Current", value: d.current },
          { name: "Long-Term", value: d.long },
        ]);
      });
    }
  }, [type, email]);

  const colors = type === "assets" ? ASSET_COLORS : LIABILITY_COLORS;

  return (
    <PieChart width={300} height={300}>
      <Pie data={data} cx={150} cy={150} innerRadius={60} outerRadius={100} dataKey="value">
        {data.map((_, i) => <Cell key={i} fill={colors[i % colors.length]} />)}
      </Pie>
      <Tooltip formatter={(v: number) => v.toFixed(2)} />
      <Legend />
    </PieChart>
  );
}
```

**`lib/api.ts` — Typed API Client**

```typescript
const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getNetWorth(email: string) {
  const res = await fetch(`${BASE}/api/users/${email}/net-worth`);
  if (!res.ok) throw new Error("Failed to fetch net worth");
  return res.json() as Promise<{ net_worth: number | null; currency: string }>;
}

export async function getAssets(email: string) {
  const res = await fetch(`${BASE}/api/users/${email}/assets`);
  if (!res.ok) throw new Error("Failed to fetch assets");
  return res.json() as Promise<{ cash: number; invested: number; use: number } | null>;
}

export async function getLiabilities(email: string) {
  const res = await fetch(`${BASE}/api/users/${email}/liabilities`);
  if (!res.ok) throw new Error("Failed to fetch liabilities");
  return res.json() as Promise<{ current: number; long: number } | null>;
}
```

#### 2.3 Dependency Comparison

| Removed | Replacement |
|---|---|
| `vue@2.6` | `next@15`, `react@19` |
| `bootstrap-vue@2`, `jquery` | `tailwindcss` |
| `chart.js@2.9`, `vue-chartjs@3` | `recharts@2` |
| `axios@0.19` | Native `fetch` |
| `@vue/cli-service` | Next.js built-in (Turbopack) |
| `eslint-plugin-vue` | `eslint-config-next` |

---

### Phase 3 — Testing & Cleanup (Week 4–5)

#### 3.1 Backend Tests

The existing test suite in `backend/tests/` covers models, datastore, and server. Migrate to:

- **pytest** with `httpx.AsyncClient` for FastAPI endpoint tests (replaces Flask test client)
- Keep the same logical test cases; update assertions for new HTTP status codes and response shapes
- Add **pytest-asyncio** for async database tests

#### 3.2 Frontend Tests

- **Vitest** for unit tests on API client and utility functions
- **React Testing Library** for component tests
- **Playwright** for end-to-end (happy path: view dashboard, update portfolio)

#### 3.3 Key Issues Fixed in Migration

| Current Bug/Limitation | Fix |
|---|---|
| All errors return 500 | Proper 400/404/409 status codes |
| No input validation | Pydantic validates all request bodies |
| Hardcoded `john.doe@gmail.com` | Email passed as route param (auth-ready) |
| No API documentation | FastAPI auto-generates OpenAPI docs at `/docs` |
| Pickle storage not portable | SQLite (or PostgreSQL) with Alembic migrations |
| `axios@0.19` (known CVE) | Native fetch or Axios 1.x |
| Vue 2 (EOL Dec 2023) | Next.js 15 / React 19 (actively maintained) |

---

### Phase 4 — Containerization (Week 5)

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./storage/assettrack.db
    volumes:
      - ./backend/storage:/app/storage

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

---

## What Is Not In Scope

- **Authentication / user accounts** — The current app has none (hardcoded demo user). Adding JWT auth is a separate initiative; this migration preserves the same demo behavior until that work is done.
- **PostgreSQL** — SQLite is used during migration for zero-ops setup. Switching to PostgreSQL later requires changing only `DATABASE_URL`.
- **New features** — The migrated app is functionally identical to the current app.

---

## Summary Timeline

| Week | Deliverable |
|---|---|
| 1 | FastAPI app with all endpoints, Pydantic schemas, SQLite via SQLAlchemy |
| 2 | Pickle → DB migration script, Alembic setup, backend tests passing |
| 3 | Next.js project, Dashboard and DonutChart components, API client |
| 4 | Frontend tests, end-to-end tests, bug fixes |
| 5 | Docker Compose setup, final review |
