-- ============================================================================
-- Team Task Manager - MySQL Database & User Setup
-- ============================================================================
-- Run this script as root or a user with GRANT privileges.
-- Windows PowerShell example:
--   mysql -u root -p < db/setup.sql
-- Or connect to MySQL and paste the commands below.

-- Create database
CREATE DATABASE IF NOT EXISTS team_task_manager;

-- Create dedicated application user with strong password
-- Change 'StrongPassword123!' to your own secure password
CREATE USER IF NOT EXISTS 'team_task_user'@'127.0.0.1' IDENTIFIED BY 'StrongPassword123!';

-- Grant all privileges on the team_task_manager database
GRANT ALL PRIVILEGES ON team_task_manager.* TO 'team_task_user'@'127.0.0.1';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify user and grants
SHOW GRANTS FOR 'team_task_user'@'127.0.0.1';

-- ============================================================================
-- After running this script:
-- 1. Update your .env file with:
--    DATABASE_URL=mysql+pymysql://team_task_user:StrongPassword123!@127.0.0.1:3306/team_task_manager
--    CREATE_TABLES_ON_STARTUP=true
-- 2. Restart the FastAPI server
-- 3. The app will automatically create all tables via SQLAlchemy
-- ============================================================================
