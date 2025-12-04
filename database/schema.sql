-- Create database schema for fitness tracker

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    age INTEGER,
    weight DECIMAL(5, 2),
    height DECIMAL(5, 2),
    gender VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Workouts table
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    workout_type VARCHAR(50),
    duration INTEGER,
    calories_burned DECIMAL(8, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercises table
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    sets INTEGER,
    reps INTEGER,
    weight DECIMAL(6, 2),
    distance DECIMAL(6, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nutrition logs table
CREATE TABLE nutrition_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    meal_type VARCHAR(50),
    food_name VARCHAR(255) NOT NULL,
    calories DECIMAL(8, 2),
    protein DECIMAL(6, 2),
    carbs DECIMAL(6, 2),
    fats DECIMAL(6, 2),
    serving_size VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goals table
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal_type VARCHAR(50),
    target_value DECIMAL(10, 2),
    current_value DECIMAL(10, 2),
    target_date TIMESTAMP,
    is_achieved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_workouts_user_id ON workouts(user_id);
CREATE INDEX idx_workouts_created_at ON workouts(created_at);
CREATE INDEX idx_exercises_workout_id ON exercises(workout_id);
CREATE INDEX idx_nutrition_logs_user_id ON nutrition_logs(user_id);
CREATE INDEX idx_nutrition_logs_created_at ON nutrition_logs(created_at);
CREATE INDEX idx_goals_user_id ON goals(user_id);
