from app import create_app, db
from app.models.user import User, UserRole
from app.models.event import Event

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Check 1: Password hashing/unhashing logic integrity
    user = User(username='testadmin', email='admin@test.com', role=UserRole.Admin)
    user.set_password('AdminPas$123')
    db.session.add(user)
    db.session.commit()
    
    # Assert
    assert user.password_hash != 'AdminPas$123', "Password should not be plaintext"
    assert user.check_password('AdminPas$123') == True, "Password check failed"
    assert user.check_password('wrongpass') == False, "Password check should fail for wrong pass"
    print("Check 1 Passed: Password hashing")

    from datetime import date, datetime
    # Check 4: Database relationships (User -> Events) correctly established
    event = Event(
        title="Test Event",
        description="Just a test",
        event_date=date(2026, 4, 1),
        start_time=datetime(2026, 4, 1, 10, 0, 0),
        end_time=datetime(2026, 4, 1, 12, 0, 0),
        venue="Room A",
        created_by=user.id
    )
    db.session.add(event)
    db.session.commit()
    
    assert user.events[0].title == "Test Event", "Relationship User -> Event failed"
    assert event.creator.username == 'testadmin', "Relationship Event -> User failed"
    print("Check 4 Passed: Database relationships")

    print("Phase 3 Models & Database Setup ok")
