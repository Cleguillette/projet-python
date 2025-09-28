def test_add_task(client):
    # Send a POST request to the "/" route to add a new task
    response = client.post("/", data={"new_task": "Test pytest"})
    
    # Verify that the server responded with a 200 OK status
    assert response.status_code == 200
    
    # Check that the task was successfully added to the database
    from main import Task, db, app
    with app.app_context():
        task = Task.query.filter_by(name="Test pytest").first()
        assert task is not None
        assert task.status == "todo"


def test_delete_task(client):
    from main import Task, db, app

    # Create a task directly in the database
    with app.app_context():
        task = Task(name="Test pytest", status="todo")
        db.session.add(task)
        db.session.commit()

    # Send a POST request to delete the task
    response = client.post("/delete", data={"task": "Test pytest", "status": "todo"})
    assert response.status_code == 302  # redirect

    # Verify that the task has been removed from the database
    with app.app_context():
        task = Task.query.filter_by(name="Test pytest").first()
        assert task is None

def test_move_task(client):
    from main import Task, db, app
       
    # Create a task directly in the database
    with app.app_context():
        task = Task(name="Test pytest", status="todo")
        db.session.add(task)
        db.session.commit()

    # Send a POST request to move the task from "todo" to "in_progress"
    response = client.post("/move", data={"task": "Test pytest", 
                                          "status": "todo", 
                                          "destination" : "in_progress"})
    
    # Verify that the task's status has been updated
    with app.app_context():
        task = Task.query.filter_by(name="Test pytest", ).first()
        assert task is not None
        assert task.status == "in_progress"