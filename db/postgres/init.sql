CREATE TABLE IF NOT EXISTS chars_appearance (
            id SERIAL PRIMARY KEY,
            episode_date DATE NOT NULL,
            chars_count INT NOT NULL
        );
