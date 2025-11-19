from django.db import models

class Medicine(models.Model):
    # From tblmedicine
    medicine_name = models.CharField(max_length=30)
    manufacture_name = models.CharField(max_length=30)
    dosage = models.CharField(max_length=10) # e.g., "500mg"
    quantity_in_stock = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage})"

class pharmacistBill(models.Model):
    # This is the "Header" of your tblpharmacist_Bill
    # The medicine_id is REMOVED from here
    bill_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    patient = models.ForeignKey(
        'reception.Patient', 
        on_delete=models.CASCADE
    )
    consultation = models.ForeignKey(
        'doctor.Consultation', 
        on_delete=models.SET_NULL, 
        null=True
    )

    def __str__(self):
        return f"Bill {self.id} for {self.patient.patient_name}"

class pharmacistBillItem(models.Model):
    # This is the new "Lines" table that holds the individual medicines for a bill
    bill = models.ForeignKey(
        pharmacistBill, 
        on_delete=models.CASCADE, 
        related_name="items" # Lets you get all items for a bill
    )
    medicine = models.ForeignKey(
        Medicine, 
        on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    price_at_time_of_sale = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.medicine_name} for Bill {self.bill.id}"