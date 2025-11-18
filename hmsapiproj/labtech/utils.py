def generate_id(prefix, model, field_name):
    last_obj = model.objects.order_by(f"-{field_name}").first()
    if not last_obj:
        return f"{prefix}001"

    last_id = getattr(last_obj, field_name)
    try:
        number = int(last_id.replace(prefix, ""))
    except:
        number = 0

    return f"{prefix}{number + 1:03d}"
