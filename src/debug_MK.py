from datetime import datetime, timedelta

def add_hours_to_datetime(dt, hours):
    days, remainder = divmod(hours, 24)
    new_datetime = dt + timedelta(days=days, hours=remainder)
    return new_datetime

# Assuming you have a datetime object
current_datetime = datetime.now()

# Number of hours to add
hours_to_add = 28  # Change this value as needed

# Adding the hours to the datetime object
updated_datetime = add_hours_to_datetime(current_datetime, hours_to_add)

print("Original Datetime:", current_datetime)
print(f"Updated Datetime (+{hours_to_add} hours):", updated_datetime)