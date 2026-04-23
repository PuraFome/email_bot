CREATE SCHEMA IF NOT EXISTS marketing;

CREATE TABLE IF NOT EXISTS marketing."Enterprise_Meling" (
    enterprise_meling_id UUID PRIMARY KEY,
    name TEXT,
    fantasy_name TEXT,
    whatsapp TEXT,
    ddd TEXT,
    email TEXT,
    coontact_valid BOOLEAN,
    open_date TIMESTAMP,
    main_activity_code TEXT,
    main_activity_description TEXT,
    cnpj TEXT,
    situation TEXT,
    country TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    region TEXT,
    share_capital TEXT,
    state TEXT
);

CREATE TABLE IF NOT EXISTS marketing.runner (
    runner_id UUID PRIMARY KEY,
    runner TEXT NOT NULL,
    platform TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS marketing.models (
    model_id UUID PRIMARY KEY,
    html TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS marketing."Sending" (
    sending_id UUID PRIMARY KEY,
    enterprise_meling_id UUID NOT NULL,
    runner_id UUID NOT NULL,
    sended_email BOOLEAN NOT NULL,
    sended_email_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sended_token TEXT,
    sended_token_used BOOLEAN NOT NULL DEFAULT FALSE,
    model_id UUID,
    CONSTRAINT "Sending_enterprise_meling_id_fkey" FOREIGN KEY (enterprise_meling_id) REFERENCES marketing."Enterprise_Meling"(enterprise_meling_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Sending_runner_id_fkey" FOREIGN KEY (runner_id) REFERENCES marketing.runner(runner_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS marketing."Email_Return_Information" (
    email_return_information_id UUID PRIMARY KEY,
    sending_id UUID NOT NULL,
    email_opned BOOLEAN NOT NULL DEFAULT FALSE,
    email_opned_date TIMESTAMP,
    CONSTRAINT "Email_Return_Information_sending_id_fkey" FOREIGN KEY (sending_id) REFERENCES marketing."Sending"(sending_id) ON DELETE CASCADE
);
