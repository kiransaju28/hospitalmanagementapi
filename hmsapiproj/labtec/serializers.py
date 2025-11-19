from rest_framework import serializers
from .models import (
    LabTestCategory, LabTestParameter, LabReport, LabReportResult, LabBill, LabBillItem
)

# --- Child Serializers ---

class LabTestParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestParameter
        fields = ['id', 'parameter_key', 'label', 'normal_range']

class LabReportResultSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source='parameter.label', read_only=True)
    class Meta:
        model = LabReportResult
        fields = ['id', 'lab_report', 'parameter', 'parameter_name', 'value']

class LabBillItemSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.category_name', read_only=True)

    class Meta:
        model = LabBillItem
        # We remove 'bill' from fields because the parent serializer handles the link
        fields = ['id', 'test', 'test_name', 'price'] 

# --- Parent Serializers ---

class LabTestCategorySerializer(serializers.ModelSerializer):
    parameters = LabTestParameterSerializer(many=True, read_only=True)
    class Meta:
        model = LabTestCategory
        fields = ['id', 'category_name', 'price', 'parameters']

class LabReportSerializer(serializers.ModelSerializer):
    results = LabReportResultSerializer(many=True, read_only=True)
    class Meta:
        model = LabReport
        fields = '__all__'

# --- THE UPDATED BILL SERIALIZER ---
class LabBillSerializer(serializers.ModelSerializer):
    # Allow writing items directly inside the bill
    items = LabBillItemSerializer(many=True) 
    
    class Meta:
        model = LabBill
        fields = ['id', 'appointment', 'patient', 'bill_date', 'total_amount', 'items']
        # The user CANNOT set total_amount manually. The computer calculates it.
        read_only_fields = ['total_amount', 'bill_date'] 

    def create(self, validated_data):
        # 1. Extract the items from the JSON
        items_data = validated_data.pop('items')
        
        # 2. Create the Bill (Header) first (start with 0 total)
        bill = LabBill.objects.create(total_amount=0, **validated_data)
        
        running_total = 0
        
        # 3. Loop through items and save them
        for item_data in items_data:
            # Create the item linked to this bill
            LabBillItem.objects.create(bill=bill, **item_data)
            # Add price to total
            running_total += item_data['price']
            
        # 4. Update the final total on the Bill
        bill.total_amount = running_total
        bill.save()
        
        return bill