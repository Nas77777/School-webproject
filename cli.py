""""import click
from flask.cli import with_appcontext
from datetime import datetime, timedelta
from app import db


@click.command('init-slots')
@with_appcontext
def init_slots_command():

    # Clear existing slots
    Slot.query.delete()

    # Create slots for the next 7 days
    start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    for day in range(7):
        current_date = start_date + timedelta(days=day)
        
        # Create 8 slots per day (9:00 - 17:00)
        for hour in range(8):
            slot_start = current_date + timedelta(hours=hour)
            slot_end = slot_start + timedelta(hours=1)
            
            slot = Slot(
                start_time=slot_start,
                end_time=slot_end,
                capacity=1,
                is_available=True
            )
            db.session.add(slot)
    
    db.session.commit()
        click.echo('Created test slots.')
    """