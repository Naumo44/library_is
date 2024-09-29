CREATE TABLE profiles (
    id int PRIMARY KEY, 
    profile_code varchar NOT NULL,
    profile_name varchar NOT NULL,
	profile_ed_program varchar NOT NULL
);

CREATE TYPE user_type_enum AS ENUM ('student', 'teacher', 'librarian');

CREATE TABLE users (
    id int PRIMARY KEY, 
    full_name varchar NOT NULL,
    profile_id int NOT NULL,
	contact_phone_number varchar NOT NULL,
	user_type user_type_enum,
    CONSTRAINT users_profiles_fk FOREIGN KEY (profile_id) REFERENCES profiles(id)
);

CREATE TABLE publishers (
    id int PRIMARY KEY, 
    publisher_name varchar NOT NULL
);

CREATE TYPE book_status_enum AS ENUM ('in operation', 'in the library');

CREATE TABLE books (
    id int PRIMARY KEY, 
    book_name varchar NOT NULL,
    profile_id int NOT NULL,
	publisher_id int NOT NULL,
	ISBN varchar NOT NULL,
	book_status book_status_enum NOT NULL,
	user_id int,
	
    CONSTRAINT books_profiles_fk FOREIGN KEY (profile_id) REFERENCES profiles(id),
	CONSTRAINT books_users_fk FOREIGN KEY (user_id) REFERENCES users(id)
);