"""
Events Blueprint - Phase 2
Handles event creation, submission, and confirmation.
"""
from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, current_app, request
)
from app import db
from app.models.event import Event, EventStatus
from app.forms.event_form import EventSubmissionForm
from flask_login import login_required, current_user
from app.utils.decorators import role_required

events_bp = Blueprint('events', __name__, template_folder='../templates')


@events_bp.route('/create', methods=['GET'])
@login_required
@role_required('Student')
def create_event():
    """GET /events/create — Render the empty event submission form."""
    form = EventSubmissionForm()
    return render_template('events/create.html', form=form)


@events_bp.route('/submit', methods=['POST'])
@login_required
@role_required('Student')
def submit_event():
    """
    POST /events/submit — Validate and persist a new event.

    Workflow:
    1. Bind form data and validate.
    2. Instantiate Event model with form values.
    3. Commit inside a try/except (rollback on failure).
    4. Log the action and flash a user-facing message.
    5. Redirect to the confirmation page on success.
    """
    form = EventSubmissionForm()

    if form.validate_on_submit():
        try:
            event = Event(
                # Basic Info
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                event_type=form.event_type.data,
                venue=form.venue.data.strip(),
                event_date=form.event_date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                # Audience
                audience_type=form.audience_type.data,
                audience_size=form.audience_size.data,
                is_external_audience=form.is_external_audience.data,
                # Technical
                requires_projector=form.requires_projector.data,
                requires_microphone=form.requires_microphone.data,
                requires_live_streaming=form.requires_live_streaming.data,
                technical_requirements=(
                    form.technical_requirements.data.strip()
                    if form.technical_requirements.data else None
                ),
                # Security
                requires_security=form.requires_security.data,
                security_requirements=(
                    form.security_requirements.data.strip()
                    if form.security_requirements.data else None
                ),
                # Budget
                budget=form.budget.data,
                budget_breakdown=(
                    form.budget_breakdown.data.strip()
                    if form.budget_breakdown.data else None
                ),
                # Status & Ownership
                status=EventStatus.Pending_Faculty,
                created_by=current_user.id
            )

            db.session.add(event)
            db.session.commit()

            current_app.logger.info(
                'Event submitted successfully: "%s" (ID: %d, Ref: %s)',
                event.title, event.id, event.reference_id
            )
            flash(
                f'Your event proposal "{event.title}" has been submitted '
                f'successfully! Reference: {event.reference_id}',
                'success'
            )
            return redirect(url_for('events.confirmation', event_id=event.id))

        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(
                'Database error while submitting event: %s', str(exc)
            )
            flash(
                'An unexpected error occurred while saving your event. '
                'Please try again.',
                'danger'
            )

    else:
        # Form validation failed — log field errors for debugging
        current_app.logger.warning(
            'Event form validation failed: %s', form.errors
        )

    # Re-render with validation errors intact
    return render_template('events/create.html', form=form)


@events_bp.route('/confirmation/<int:event_id>')
def confirmation(event_id):
    """GET /events/confirmation/<id> — Show submission success details."""
    event = Event.query.get_or_404(event_id)
    return render_template('events/confirmation.html', event=event)
