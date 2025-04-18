# 🎬 MovieLens Data Analysis and Visualization System

A Django + MongoDB based web application for querying and analyzing movie data from the MovieLens dataset. It supports keyword search, user rating lookup, and popular movie ranking with a clean HTML front-end.

---

## 📦 Requirements

Ensure Python ≥ 3.8 is installed along with MongoDB.

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Advanced-Database-master/
│
├── ADatabase/
│   ├── templates/
│   │   ├── index.html
│   │   ├── result1.html
│   │   ├── result2.html
│   │   └── result3.html
│   ├── view.py
│   ├── database.py
│   ├── search.py
│   └── ...
├── import_to_mongo.py
├── manage.py
└── requirements.txt
```

---

## 🚀 How to Run

1. Install MongoDB and start the service:

```bash
sudo apt update
sudo apt install mongodb -y
sudo systemctl start mongodb
```

2. Import MovieLens dataset using the import script:

```bash
python3 import_to_mongo.py
```

3. Start the Django development server:

```bash
cd ADatabase
python3 manage.py runserver 0.0.0.0:8000
```

4. Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🔍 Usage Examples

- Keyword search: `Comedy`, `Action`, `Drama`
- User rating lookup: use user IDs like `1`, `92259`, `106782`

---

## ❗ Common Issues

| Issue | Solution |
|-------|----------|
| `No module named 'mongoengine'` | Not needed; remove or `pip install mongoengine` |
| Empty result | Check if data was successfully imported into MongoDB |
| CSS or JS not loading | Make sure static resources are correctly mapped |

---

## 🧩 Suggestions for Improvement

- Docker container deployment
- Add user authentication and collection features
- Integrate a movie recommendation engine

