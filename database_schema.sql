-- PostgreSQL Database Schema for betterEngineer Newsletter
-- Execute this SQL in your PostgreSQL database

-- Create the subscribers table
CREATE TABLE IF NOT EXISTS subscribers (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    branch TEXT NULL,
    frequency TEXT NOT NULL DEFAULT 'weekly' CHECK (frequency IN ('daily', 'weekly', 'monthly')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'unsubscribed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_subscribers_email ON subscribers(email);
CREATE INDEX IF NOT EXISTS idx_subscribers_status ON subscribers(status);
CREATE INDEX IF NOT EXISTS idx_subscribers_created_at ON subscribers(created_at);
CREATE INDEX IF NOT EXISTS idx_subscribers_frequency ON subscribers(frequency);

-- Create a view for active subscribers only
CREATE OR REPLACE VIEW active_subscribers AS
SELECT id, email, branch, frequency, created_at
FROM subscribers
WHERE status = 'active'
ORDER BY created_at DESC;

-- Function to unsubscribe by email
CREATE OR REPLACE FUNCTION unsubscribe_by_email(subscriber_email TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    rows_affected INTEGER;
BEGIN
    UPDATE subscribers 
    SET status = 'unsubscribed' 
    WHERE email = subscriber_email AND status = 'active';
    
    GET DIAGNOSTICS rows_affected = ROW_COUNT;
    RETURN rows_affected > 0;
END;
$$ LANGUAGE plpgsql;

-- Function to get subscriber statistics
CREATE OR REPLACE FUNCTION get_subscriber_stats()
RETURNS TABLE(
    total_active BIGINT,
    total_unsubscribed BIGINT,
    total_all BIGINT,
    daily_count BIGINT,
    weekly_count BIGINT,
    monthly_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) FILTER (WHERE status = 'active') as total_active,
        COUNT(*) FILTER (WHERE status = 'unsubscribed') as total_unsubscribed,
        COUNT(*) as total_all,
        COUNT(*) FILTER (WHERE status = 'active' AND frequency = 'daily') as daily_count,
        COUNT(*) FILTER (WHERE status = 'active' AND frequency = 'weekly') as weekly_count,
        COUNT(*) FILTER (WHERE status = 'active' AND frequency = 'monthly') as monthly_count
    FROM subscribers;
END;
$$ LANGUAGE plpgsql;

-- Sample data for testing (uncomment to use)
-- INSERT INTO subscribers (email, branch, frequency) VALUES 
-- ('test@example.com', 'CSE', 'weekly'),
-- ('john.doe@example.com', 'ECE', 'daily'),
-- ('jane.smith@example.com', NULL, 'monthly')
-- ON CONFLICT (email) DO NOTHING;
