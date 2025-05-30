# 📚 Xamely – Exam Management System

**Xamely** is a full-featured web-based Exam Management System built using **HTML, CSS, JavaScript, Python (Flask)**, and integrated with a **MySQL database via SQL Workbench**. Designed to support schools, colleges, universities, and online learning platforms, Xamely simplifies exam creation, administration, and evaluation.

---

## 🌐 Features

* 🔐 User Authentication (Admin, Teacher, Student)
* ⏰ Timed Online Exams
* 📊 Result Calculation & Analytics
* 📁 Question Bank Management
* 📱 Responsive User Interface

---

## 🛠️ Tech Stack

| Layer    | Technology                |
| -------- | ------------------------- |
| Frontend | HTML, CSS, JavaScript     |
| Backend  | Python (Flask)            |
| Database | MySQL (via SQL Workbench) |
| Tools    | VS Code, SQL Workbench    |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Flask (`pip install flask`)
* MySQL Server with SQL Workbench
* Web Browser

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone [https://github.com/Ayushmann13479/Xamely-Exam-Management-System.git]
   cd xamely
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required Python packages**


4. **Set up the MySQL database**

   * Open SQL Workbench.
   * Import the SQL script from the `/sql` folder to create tables and insert initial data.

5. **Configure environment variables** (optional)
   Create a `.env` file and add your DB credentials:

   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=xamely_db
   ```

6. **Run the Flask application**

   ```bash
   flask run
   ```

7. Open your browser and go to `http://localhost:5000`.

---

## 🧠 Use Cases

* Educational Institutions (schools, colleges, universities)
* Online Course Platforms (MOOCs, certification providers)
* Corporate Training & Assessment

---


## 👥 Contributors

* **Ayushmann** – Full Stack Developer


---


