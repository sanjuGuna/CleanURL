# 🔗 URL Shortener – SaaS Web App

A full-stack **URL Shortener SaaS application** that allows users to convert long URLs into short, shareable links. It also tracks how many times each short URL is clicked. This project is fully built using **React (Vite)** for the frontend, **FastAPI** for the backend, and **MySQL** for persistent storage.

---

## 📌 Features

- ✂️ Shorten long URLs to compact links
- 🔁 Redirect automatically to the original URL on click
- 📊 Track and display number of clicks
- 🔐 Uses SHA-256 with Base64 encoding for short URLs
- 🧠 Designed to be extended into a full SaaS product

---

## 🧰 Tech Stack

| Layer       | Technology        |
|------------|-------------------|
| Frontend    | React + Vite      |
| Backend     | FastAPI (Python)  |
| Database    | MySQL             |
| Hashing     | SHA-256 + Base64  |

---

## 🛢️ MySQL Database Schema

```sql
CREATE TABLE url_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_url VARCHAR(10) UNIQUE NOT NULL,
    clicks INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
