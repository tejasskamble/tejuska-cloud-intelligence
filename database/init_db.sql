-- =============================================================================
-- TEJUSKA Cloud Intelligence
-- Database Initialisation Script
-- Standard: FinOps FOCUS 1.1 (Linux Foundation)
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Extensions
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ---------------------------------------------------------------------------
-- Tenants (Multi-Tenant SaaS)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name     TEXT NOT NULL,
    domain           TEXT UNIQUE NOT NULL,
    admin_email      TEXT NOT NULL,
    plan             TEXT NOT NULL DEFAULT 'free'
                         CHECK (plan IN ('free', 'pro', 'enterprise')),
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Subscriptions
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id            UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    plan                 TEXT NOT NULL CHECK (plan IN ('free', 'pro', 'enterprise')),
    status               TEXT NOT NULL DEFAULT 'active'
                             CHECK (status IN ('active', 'past_due', 'cancelled', 'trialing')),
    stripe_customer_id   TEXT,
    stripe_subscription_id TEXT,
    razorpay_order_id    TEXT,
    current_period_start TIMESTAMPTZ,
    current_period_end   TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- FOCUS 1.1 Consolidated Billing Table
-- Reference: https://focus.finops.org
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS consolidated_billing (
    -- Identity
    row_id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id               UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,

    -- FOCUS 1.1 Required Columns
    billing_account_id      TEXT NOT NULL,
    billing_account_name    TEXT,
    billing_period_start    TIMESTAMPTZ NOT NULL,
    billing_period_end      TIMESTAMPTZ NOT NULL,
    charge_period_start     TIMESTAMPTZ NOT NULL,
    charge_period_end       TIMESTAMPTZ NOT NULL,

    -- Cost columns (all in USD)
    billed_cost             NUMERIC(18,6) NOT NULL DEFAULT 0,
    effective_cost          NUMERIC(18,6) NOT NULL DEFAULT 0,
    list_cost               NUMERIC(18,6),
    list_unit_price         NUMERIC(18,10),
    contracted_cost         NUMERIC(18,6),
    contracted_unit_price   NUMERIC(18,10),

    -- Currency
    billing_currency        TEXT NOT NULL DEFAULT 'USD',

    -- Provider / Service
    provider_name           TEXT NOT NULL,       -- e.g. AWS, GCP, Azure
    publisher_name          TEXT,
    service_name            TEXT NOT NULL,        -- e.g. Amazon EC2
    service_category        TEXT,                 -- e.g. Compute, Storage, Network
    resource_id             TEXT,
    resource_name           TEXT,
    resource_type           TEXT,

    -- Region
    region_id               TEXT,
    region_name             TEXT,
    availability_zone       TEXT,

    -- Charge metadata
    charge_type             TEXT NOT NULL        -- Usage, Purchase, Tax, Adjustment
                                CHECK (charge_type IN ('Usage', 'Purchase', 'Tax', 'Adjustment', 'Credit')),
    charge_category         TEXT,
    charge_description      TEXT,
    charge_frequency        TEXT DEFAULT 'Usage-Based',

    -- Pricing
    pricing_category        TEXT,
    pricing_quantity        NUMERIC(18,6),
    pricing_unit            TEXT,

    -- Usage
    consumed_quantity        NUMERIC(18,6),
    consumed_unit            TEXT,

    -- Commitment discounts
    commitment_discount_id   TEXT,
    commitment_discount_name TEXT,
    commitment_discount_type TEXT,

    -- Tags (JSONB for flexibility)
    tags                     JSONB DEFAULT '{}',

    -- Ingestion metadata
    ingested_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file              TEXT
);

-- ---------------------------------------------------------------------------
-- AI Recommendations Audit Log
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_recommendations (
    recommendation_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id           UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    resource_id         TEXT,
    recommendation_type TEXT NOT NULL,   -- e.g. Rightsize, Terminate, Reserve
    estimated_savings   NUMERIC(18,6),
    confidence_score    NUMERIC(5,4),
    status              TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending', 'approved', 'rejected', 'executed')),
    reasoning           TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    executed_at         TIMESTAMPTZ
);

-- ---------------------------------------------------------------------------
-- Notification Log
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notification_log (
    notification_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id         UUID REFERENCES tenants(tenant_id) ON DELETE SET NULL,
    channel           TEXT NOT NULL CHECK (channel IN ('slack', 'email', 'sms')),
    recipient         TEXT NOT NULL,
    subject           TEXT,
    body              TEXT,
    status            TEXT NOT NULL DEFAULT 'sent'
                          CHECK (status IN ('sent', 'failed')),
    error_message     TEXT,
    sent_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Indexes for performance
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_billing_tenant         ON consolidated_billing(tenant_id);
CREATE INDEX IF NOT EXISTS idx_billing_period         ON consolidated_billing(billing_period_start, billing_period_end);
CREATE INDEX IF NOT EXISTS idx_billing_provider       ON consolidated_billing(provider_name);
CREATE INDEX IF NOT EXISTS idx_billing_service        ON consolidated_billing(service_name);
CREATE INDEX IF NOT EXISTS idx_billing_resource       ON consolidated_billing(resource_id);
CREATE INDEX IF NOT EXISTS idx_billing_charge_type    ON consolidated_billing(charge_type);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tenant   ON subscriptions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_tenant ON ai_recommendations(tenant_id);

-- ---------------------------------------------------------------------------
-- Updated-at trigger function
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER set_updated_at_tenants
    BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

CREATE OR REPLACE TRIGGER set_updated_at_subscriptions
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
