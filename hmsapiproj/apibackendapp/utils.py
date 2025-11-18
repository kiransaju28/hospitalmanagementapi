def generate_id(prefix, model, field_name):
    """
    Generate a unique ID with the given prefix.
    
    Args:
        prefix (str): The prefix for the ID (e.g., 'LT' for LabTest)
        model: The Django model class
        field_name (str): The name of the ID field in the model
    
    Returns:
        str: A unique ID like 'LT001', 'LT002', etc.
    """
    # Get the last object ordered by the ID field, descending
    last_obj = model.objects.all().order_by(f'-{field_name}').first()
    
    if last_obj:
        # Extract the numeric part from the last ID
        last_id = getattr(last_obj, field_name)
        # Remove prefix and convert to int
        try:
            number = int(last_id[len(prefix):])
        except (ValueError, IndexError):
            number = 0
    else:
        number = 0
    
    # Increment and format with leading zeros
    new_number = number + 1
    return f"{prefix}{new_number:03d}"
