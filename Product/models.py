from django.db import models

class item(models.Model):
	name = (
		('WOVEN NARROW FAB', 'WOVEN NARROW FAB'),
		('KNITTED NARROW FAB', 'KNITTED NARROW FAB'),
		)

	code = (
		('Elastic', 'Elastic'),
		('Velcro', 'Velcro'),
		)

	name=models.CharField(max_length=50, choices=name, default="WOVEN NARROW FAB")
	code=models.CharField(max_length=50, choices=code, default=None)
	description=models.CharField(max_length=100)

	def _get_y(self):
		if self.name == "WOVEN NARROW FAB":
			x = "5806"
			return x
		else:
			x = "6002"
			return x
	hsn=property(_get_y)

	def __str__(self):
		return self.code + " - " + self.name + " - " + self.description + " - " + self.hsn