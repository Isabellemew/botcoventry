DROP TABLE IF EXISTS bookings, rooms, clubs;

<<<<<<< HEAD
=======
-- Таблица клубов
>>>>>>> coventry-database
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    description TEXT
);

<<<<<<< HEAD
=======
-- Таблица аудиторий
>>>>>>> coventry-database
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL,
    floor INTEGER,
    name TEXT,
    capacity INTEGER,
    room_type VARCHAR(50),  -- Lecture Hall, PC Lab, Seminar Room, Office, Fitness, etc.
    available BOOLEAN DEFAULT TRUE
);

<<<<<<< HEAD
=======
-- Таблица бронирований
>>>>>>> coventry-database
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    room_id INTEGER REFERENCES rooms(id),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    purpose TEXT,
<<<<<<< HEAD
    booked_by VARCHAR(100) 
=======
    booked_by VARCHAR(100) -- добавлено
>>>>>>> coventry-database
);

SELECT * FROM bookings;

<<<<<<< HEAD
=======
-- Клубы
>>>>>>> coventry-database
INSERT INTO clubs (name, category, description) VALUES
('Media', 'Creative / Media', 'Photo, video, and content editing'),
('Advertisement', 'Marketing', 'Promotion and advertising activities'),
('Ink & Insights (Book)', 'Literature', 'Book club and discussion group'),
('Talent Wave', 'Creative Arts', 'Music, performance, and art showcases'),
('Game Dev / IT', 'Technology / IT', 'Game development and programming'),
('Chess', 'Intellectual', 'Chess competitions and strategy practice'),
('Volleyball', 'Sports', 'University volleyball team'),
('Debates Nexus', 'Academic', 'English-language debate club'),
('Model of UN', 'Academic', 'Simulation of United Nations sessions'),
('Psychology & Mental Health', 'Social / Wellness', 'Mental health support and awareness'),
('Enactus', 'Social / Business', 'Startup and social initiatives'),
('Basketball', 'Sports', 'University basketball team'),
('Football', 'Sports', 'University football (soccer) team'),
('Table Tennis', 'Sports', 'Table tennis club and training');

<<<<<<< HEAD
=======
-- Аудитории
>>>>>>> coventry-database
INSERT INTO rooms (room_number, floor, name, capacity, room_type, available) VALUES
-- 1st Floor
('103', 1, 'Medical Services', 10, 'Office', TRUE),
('105', 1, 'Admissions', 8, 'Office', TRUE),
('102', 1, 'Facilities Manager', 6, 'Office', TRUE),
('104', 1, 'Admissions', 8, 'Office', TRUE),

-- 2nd Floor
('203', 2, 'PC Lab', 25, 'PC Lab', TRUE),
('201', 2, 'Fitness', 20, 'Fitness', TRUE),
('202', 2, 'PC Lab', 25, 'PC Lab', TRUE),
('204', 2, 'Lecture Hall', 60, 'Lecture Hall', TRUE),
('209', 2, 'Head of Foundation', 6, 'Office', TRUE),
('208', 2, 'Wellbeing Center', 10, 'Office', TRUE),
('207', 2, 'Academic Support', 12, 'Office', TRUE),
('205', 2, 'Staff Lounge', 15, 'Lounge', TRUE),
('206', 2, 'Staff Lounge', 15, 'Lounge', TRUE),

-- 3rd Floor
('306', 3, 'Seminar Room', 20, 'Seminar Room', TRUE),
('305', 3, 'Seminar Room', 20, 'Seminar Room', TRUE),
('307', 3, 'PC Lab', 25, 'PC Lab', TRUE),
('308', 3, 'PC Lab', 25, 'PC Lab', TRUE),
('304', 3, 'Seminar Room', 20, 'Seminar Room', TRUE),
('303', 3, 'Lecture Hall', 60, 'Lecture Hall', TRUE),
('302', 3, 'Student Hall', 40, 'Lounge', TRUE),
('301', 3, 'Library', 50, 'Library', TRUE),

-- 4th Floor
('403', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('404', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('402', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('401', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('405', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('407', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('408', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('409', 4, 'Seminar Room', 20, 'Seminar Room', TRUE),
('406', 4, 'Lecture Hall', 60, 'Lecture Hall', TRUE),
('411', 4, 'Student Services', 10, 'Office', TRUE),
('410', 4, 'Register Office', 8, 'Office', TRUE);

SELECT * FROM rooms;


<<<<<<< HEAD
=======
-- Пример бронирования
>>>>>>> coventry-database
INSERT INTO bookings (room_id, booked_by, date, start_time, end_time, purpose)
VALUES (3, 'Tech Club', '2025-07-23', '15:00', '17:00', 'Weekly Tech Club Meeting');
