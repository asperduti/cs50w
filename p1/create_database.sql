CREATE TABLE "books" (
	"id"	SERIAL PRIMARY KEY,
	"isbn"	TEXT NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	"author"	TEXT NOT NULL,
	"year"	INTEGER NOT NULL
);
CREATE TABLE "users" (
	"id"	SERIAL PRIMARY KEY,
	"username"	TEXT NOT NULL,
	"hash"	TEXT NOT NULL
);
CREATE TABLE "reviews" (
	"id"	SERIAL PRIMARY KEY,
	"user_id"	INTEGER NOT NULL,
	"book_id"	INTEGER NOT NULL,
	"score"	REAL NOT NULL,
	"review"	TEXT,
	FOREIGN KEY("user_id") REFERENCES "users",
	FOREIGN KEY("book_id") REFERENCES "books"
);