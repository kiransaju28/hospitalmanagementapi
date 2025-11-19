# apibackend/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Patient, Appointment, Doctor, Billing # Import all core models
from django.db.models import Q

def generate_id(prefix, model, field_name, length=3):
    """Generates the next sequential ID (e.g., 'P001', 'A00001')."""
    
    # Retrieve the last record based on the field name and prefix using Q for robustness
    last_record = model.objects.filter(
        Q(**{f'{field_name}__startswith': prefix})
    ).order_by(f'-{field_name}').first()
    
    if last_record:
        last_id = getattr(last_record, field_name)
        try:
            # Extract the numeric part (e.g., '001')
            current_num = int(last_id[len(prefix):])
            next_num = current_num + 1
        except ValueError:
            next_num = 1
    else:
        next_num = 1
    
    # Format the new ID with zero-padding
    return f'{prefix}{next_num:0{length}d}'


# --- SIGNAL RECEIVERS ---

@receiver(pre_save, sender=Patient)
def auto_id_patient(sender, instance, **kwargs):
    """Auto-generates patient_id before saving."""
    if not instance.patient_id:
        instance.patient_id = generate_id(
            prefix="P",
            model=Patient,
            field_name="patient_id",
            length=3 # P001, P002, etc.
        )

@receiver(pre_save, sender=Appointment)
def auto_id_appointment(sender, instance, **kwargs):
    """Auto-generates appointment_id before saving."""
    if not instance.appointment_id:
        instance.appointment_id = generate_id(
            prefix="APP",
            model=Appointment,
            field_name="appointment_id",
            length=5 # A00001, A00002, etc.
        )

@receiver(pre_save, sender=Doctor)
def auto_id_doctor(sender, instance, **kwargs):
    """Auto-generates doctor_id before saving."""
    if not instance.doctor_id:
        instance.doctor_id = generate_id(
            prefix="D",
            model=Doctor,
            field_name="doctor_id",
            length=3
        )
@receiver(pre_save, sender=Billing )
def auto_id_billing(sender, instance, **kwargs):
    """Auto-generates billing_id before saving."""
    if not instance.billing_id:
        instance.billing_id = generate_id(
            prefix="B",
            model=Billing,
            field_name="billing_id",
            length=3 # B0001, B0002, etc.
        )