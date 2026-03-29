from datetime import datetime, timezone
from app import db
from app.utils.ip_utils import get_client_ip

class AuditLog(db.Model):
    """
    AuditLog model to track security events as per Section 12.7.
    Tracks user actions, timestamps, and IP addresses.
    """
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resource_type = db.Column(db.String(50), nullable=True) # e.g., 'Event', 'User'
    resource_id = db.Column(db.Integer, nullable=True)

    # Relationship
    user = db.relationship('User', backref='audit_logs', lazy=True)

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id if self.user_id else "Guest"} on {self.timestamp}>'

    @staticmethod
    def create_log(action, request, user_id=None, resource_type=None, resource_id=None):
        """Helper to create audit log entry."""
        log = AuditLog(
            user_id=user_id,
            action=action,
            ip_address=get_client_ip(request),
            resource_type=resource_type,
            resource_id=resource_id
        )
        db.session.add(log)
        db.session.commit()
