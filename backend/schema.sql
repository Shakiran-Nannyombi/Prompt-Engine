-- Application schema for Prompt Engine

-- Table to store user-defined tasks and their refinements
CREATE TABLE IF NOT EXISTS prompt_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id TEXT NOT NULL,
    original_task TEXT NOT NULL,
    refined_prompt TEXT,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table to store custom frameworks or templates
CREATE TABLE IF NOT EXISTS framework_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    structure JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by thread_id
CREATE INDEX IF NOT EXISTS idx_prompt_history_thread_id ON prompt_history(thread_id);
