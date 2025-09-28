# Task Organizer - Flask App

A simple task organizer web application built with Flask and SQLite. Users can add tasks, move them between statuses (To Do, In Progress, Done), and delete them.

## Features

- Add new tasks
- Move tasks between "To Do", "In Progress", and "Done"
- Delete tasks
- Simple web interface using HTML forms and Flask templates

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Cleguillette/projet-python.git
cd projet-python
```

2. Create and activate the Conda environment from the provided environment.yml:

```bash
conda env create -f environment.yml
conda activate projet-python
```

3. Run the application:

```bash
python main.py
```

## Usage

- Open your browser and go to `http://127.0.0.1:5000/`
- Add a new task in the input field and click "Add"
- Move tasks between columns using the ✅ and ↩️ buttons
- Delete tasks using the 🗑️ button

## Running Tests

All tests use an in-memory SQLite database and will not affect your main database.

```bash
pip install pytest
pytest
```

## Project Structure

```text
├── README.md
├── environment.yml
├── main.py
├── templates/
│   └── index.html
├── tests/
│   ├── conftest.py
│   └── test_app.py
```

## Technologies

- Python 3.13.5
- Flask
- SQLAlchemy
- SQLite
- Jinja2 templates
- pytest for testing