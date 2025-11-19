from rest_framework import serializers
from .models import Medicine, pharmacistBill, pharmacistBillItem


# =======================
# MEDICINE SERIALIZER
# =======================
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


# =======================
# pharmacist BILL ITEM
# =======================
class pharmacistBillItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)

    class Meta:
        model = pharmacistBillItem
        fields = [
            'id',
            'medicine',
            'medicine_name',
            'quantity',
            'price_at_time_of_sale',
            'subtotal'
        ]
        read_only_fields = ['price_at_time_of_sale', 'subtotal']


# =======================
# pharmacist BILL (MAIN)
# =======================
class pharmacistBillSerializer(serializers.ModelSerializer):
    items = pharmacistBillItemSerializer(many=True)

    class Meta:
        model = pharmacistBill
        fields = [
            'id',
            'bill_date',
            'total_amount',
            'patient',
            'consultation',
            'items'
        ]
        read_only_fields = ['bill_date', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Create bill header
        bill = pharmacistBill.objects.create(total_amount=0, **validated_data)

        total_amount = 0

        for item_data in items_data:
            medicine = item_data['medicine']
            quantity = item_data['quantity']

            # Stock check
            if medicine.quantity_in_stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {medicine.medicine_name}. "
                    f"Available: {medicine.quantity_in_stock}"
                )

            price = medicine.price_per_unit
            subtotal = price * quantity

            # Save item
            pharmacistBillItem.objects.create(
                bill=bill,
                medicine=medicine,
                quantity=quantity,
                price_at_time_of_sale=price,
                subtotal=subtotal
            )

            # Deduct stock
            medicine.quantity_in_stock -= quantity
            medicine.save()

            total_amount += subtotal

        bill.total_amount = total_amount
        bill.save()

        return bill
