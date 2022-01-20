from django.db import models
from Product.models import item
from django.db.models import Model
from django.db.models import Q
from Beneficiary.models import recipient, transport

# Create your models here.
class temp(models.Model):	
	item = models.ForeignKey(item, null=True, on_delete=models.DO_NOTHING)
	mtr=models.CharField(max_length=50)
	rate=models.CharField(max_length=100)
	qty=models.CharField(max_length=100)
	box=models.CharField(max_length=100, default="01")

	def _get_y(self):
		c = "1.05"
		x = float(self.rate) / float(c)
		x1 = round(x,2)
		return x1
	rate_without_gst=property(_get_y)

	def _get_z(self):
		y = float(self.rate_without_gst) * float(self.qty)
		y1 = round(y,2)
		return y1
	amount=property(_get_z)

	def _get_t(self):
		t = float(self.rate) * float(self.qty)
		t1 = round(t,2)
		return t1
	tamount=property(_get_t)

class order_item(models.Model):
	item = models.ForeignKey(item, null=True, on_delete=models.DO_NOTHING)
	mtr=models.CharField(max_length=50)
	rate=models.CharField(max_length=100)
	rate_without_gst=models.CharField(max_length=100)
	amount=models.CharField(max_length=100)
	tamount=models.CharField(max_length=100)
	qty=models.CharField(max_length=100)
	box=models.CharField(max_length=100)
	bill_number=models.CharField(max_length=100)

	def __str__(self):
		return self.bill_number + " - " + self.tamount + " - " + self.item.description + " @ " + self.qty + "PCS"

class bill_details(models.Model):
	pmethod = (
		('NEFT', 'NEFT'),
		('CASH', 'CASH'),
		)

	bill_number = models.CharField(max_length=100)
	recipient = models.ForeignKey(recipient, null=True, on_delete=models.DO_NOTHING)
	transport = models.ForeignKey(transport, null=True, on_delete=models.DO_NOTHING)
	date = models.DateField(blank=True)
	total_amount = models.CharField(max_length=100)
	discount = models.CharField(max_length=100, default="0")
	freight_charges = models.CharField(max_length=100, default="0")
	payment_method = models.CharField(max_length=50, choices=pmethod)
	total_box = models.CharField(max_length=100)
	tamount_without_gst = models.CharField(max_length=100)
	ewaybill_number = models.CharField(max_length=100, default="-----------")
	total_quantity = models.CharField(max_length=100, default="0")

	def __str__(self):
		return self.bill_number + " " + self.recipient.name + " - " + self.total_amount

class formatt(models.Model):
	img=models.ImageField(upload_to='pics', blank=True)
	invno=models.CharField(max_length=50, blank=True)
	stamp=models.ImageField(upload_to='pics', blank=True)

	def __str__(self):
		return self.invno
