from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.conf import settings
from Beneficiary.models import recipient, transport
from Product.models import item
from Bill.models import temp, formatt, bill_details, order_item
from datetime import date
import static
import media
from num2words import num2words
import os
from django.template.loader import get_template
from xhtml2pdf import pisa
import locale
from django.contrib import messages
import pandas as pd
from io import BytesIO
import xlwt

locale.setlocale(locale.LC_MONETARY, 'en_IN')


def create(request):
	e = item.objects.filter(code="Elastic")
	v = item.objects.filter(code="Velcro")
	f = formatt.objects.get(id=1)
	TEMP = temp.objects.all()

	if request.method == "POST":
		it = request.POST.get('item')
		mtr = request.POST.get('mtr')
		qty = request.POST.get('qty')
		rate = request.POST.get('rate')
		box = request.POST.get('box')

		n,d = it.split(' - ')
		i1 = item.objects.filter(name=n)
		i2 = i1.get(description=d)

		t = temp(item=i2, mtr=mtr, qty=qty, rate=rate, box=box)
		t.save()

		return redirect('/Bill/Create/Select_Product')
	else:
		return render(request, "select_product.html", {'e':e, 'v':v, 'TEMP':TEMP, 'f':f})

def removep(request):
	p = request.POST.get('pid')
	i = temp.objects.get(id=p)
	i.delete()

	return redirect('/Bill/Create/Select_Product')

def updatebillno(request):
	bn = request.POST.get('billno')
	billno = int(bn)
	billno = "%s" %billno
	billno = billno.zfill(3)

	f = formatt.objects.get(id=1)
	f.invno = str(billno)
	f.save()

	return redirect('/Bill/Create/Select_Product')

def deletebill(request):
	bn = request.POST.get('bno')
	print(bn)

	b = bill_details.objects.get(bill_number=bn)
	o = order_item.objects.filter(bill_number=bn)

	for t in o:
		t.delete()
	b.delete()

	return redirect('/Bill/View')

def create_step2(request):
	if request.method == "POST":
		r = request.POST.get('recipient')
		t = request.POST.get('transport')

		n,d = r.split(' - ')
		r1 = recipient.objects.filter(name=n)
		r2 = r1.get(gstin=d)

		x,y = t.split(' - ')
		t1 = transport.objects.filter(name=x)
		t2 = t1.get(gstin=y)

		d1 = date.today()
		
		b = formatt.objects.get(id=1)

		d = request.POST.get('discount')
		f = request.POST.get('freight')

		TEMP = temp.objects.all()

		tbox = "0"
		total = "0"
		tawg = "0"
		tqty = "0"
		for t in TEMP:
			tbox = int(tbox) + int(t.box)
			total = float(total) + float(t.tamount)
			tawg = float(tawg) + float(t.amount)
			tqty = int(tqty) + int(t.qty)

			twithout = t.rate_without_gst
			tawg1 = float(twithout)
			tawg1 = locale.currency(tawg1, grouping=True)
			tawg1 = tawg1.replace('? ', '')
			tawg1 = str(tawg1)
			o = order_item(item=t.item, mtr=t.mtr, qty=t.qty, rate=t.rate, rate_without_gst=tawg1, amount=t.amount, tamount=t.tamount, box=t.box, bill_number=b.invno)
			o.save()
			t.delete()

		payment = request.POST.get('payment')

		tbox1 = int(tbox)
		tbox1 = "%s" %tbox1
		tbox = tbox1.zfill(2)
		round(total,2)

		round(tawg,2)
		tawg = float(tawg)
		tawg = locale.currency(tawg, grouping=True)
		tawg = tawg.replace("? ", '')

		total = locale.currency(total, grouping=True)
		total = total.replace("? ", '')
		total = str(total)
		tbox = str(tbox)
		tawg = str(tawg)
		tqty = str(tqty)

		bill = bill_details(bill_number=b.invno, recipient=r2, transport=t2, date=d1, total_amount=total, discount=d, freight_charges=f, payment_method=payment, total_box=tbox, tamount_without_gst=tawg, total_quantity=tqty)
		bill.save()

		t1 = int(b.invno)
		f1 = t1 + 1
		f2 = "%s" %f1
		b.invno = f2.zfill(3)
		b.save()

		return redirect('/Bill/Render_pdf')
	else:
		r = recipient.objects.all()
		t = transport.objects.all()
		return render(request, "select_beneficiary.html", {'r':r, 't':t})

def viewbill(request):
	if request.user.is_superuser:
		b = bill_details.objects.all()
	else:
		tempn = request.user.username
		tempp = request.user.first_name

		u = recipient.objects.filter(name=tempn)
		u = u.get(gstin=tempp)
		b = bill_details.objects.filter(recipient=u)
	return render(request, "view_bills.html", {'b':b})

def render_pdf(request):
	f = formatt.objects.get(id=1)

	if request.method == "POST":
		n = request.POST.get('bno')
	else:
		no1 = int(f.invno)
		no1 = no1 - 1
		no1 = "%s" %no1
		n = no1.zfill(3)
	
	b = bill_details.objects.get(bill_number=n)

	template_path = 'format.html'

	o = order_item.objects.filter(bill_number=n)

	p = b.tamount_without_gst
	p = p.replace(',' , '')
	tamount = float(p)
	tamount = locale.currency(tamount, grouping=True)
	tamount = tamount.replace("? ", '')

	row = o.count()
	h1 = 245
	h2 = 49

	h3 = h1 - (h2 * int(row))

	p1 = b.total_amount.replace(',' , '')
	g = float(p1) - float(p)
	fc = float(b.freight_charges) / 1.05
	fc = float(b.freight_charges) - fc
	g = g + fc

	total = float(p1) + float(b.freight_charges) - float(b.discount)
	ta1 = 'Rs. ' + num2words(str(total)).capitalize() + ' Only'
	total = locale.currency(total, grouping=True)
	total = total.replace("? ", '')

	ta1 = ta1.replace(",", '')
	h=""
	hh=""
	if b.recipient.gst == "I-GST":
		h+="<td colspan='2' rowspan='2' style='border: none;'>I-GST @ 5%</td>"
		hh+="<td style='border: none; text-align:center' rowspan='2'>"+str(round(g,2))+"0</td>"
	else:
		g=float(g)/2
		h+="<td colspan='2' rowspan='2' style='border: none;'>S-GST @ 2.5%<br>C-GST @ 2.5%</td>"
		hh+="<td style='border: none; text-align:center' rowspan='2'>"+str(round(g,2))+"0<br>"+str(round(g,2))+"0</td>"

	context = {'b':b, 'f':f, 'ta':ta1, 'total':total, 'o':o, 'h':h3, 'tamount':tamount, 'h1':h, 'h2':hh}
    # Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"' - to download the file

    #to view only:
	filename= b.bill_number + " " + b.recipient.name + ".pdf"
	response['Content-Disposition'] = 'filename="%s"' %(filename)
    # find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

    # create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
	if pisa_status.err:
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

def extract_data(request):
	if request.user.is_superuser:
		r = recipient.objects.all()
		t = transport.objects.all()

		response = HttpResponse(content_type='application/vnd.ms-excel') 
		response['Content-Disposition'] = 'attachment;filename=Beneficiary.xls'

		work_book = xlwt.Workbook(encoding = 'utf-8') 
		recipient_sheet = work_book.add_sheet('Recipient')
		transport_sheet = work_book.add_sheet('Transport')

		style_head_row = xlwt.easyxf("""    
	    align:
	      wrap off,
	      vert center,
	      horiz center;
	    borders:
	      left THIN,
	      right THIN,
	      top THIN,
	      bottom THIN;
	    font:
	      name Arial,
	      colour_index white,
	      bold on,
	      height 0xA0;
	    pattern:
	      pattern solid,
	      fore-colour 0x19;
	    """
	    )

		style_data_row = xlwt.easyxf("""
	    align:
	      wrap on,
	      vert center,
	      horiz left;
	    font:
	      name Arial,
	      bold off,
	      height 0XA0;
	    borders:
	      left THIN,
	      right THIN,
	      top THIN,
	      bottom THIN;
	    """
	  	)

		style_data_row.num_format_str = 'MM/DD/YYYY'

		recipient_sheet.write(0,0, 'S.No.', style_head_row)
		recipient_sheet.write(0,1, 'NAME', style_head_row)
		recipient_sheet.write(0,2, 'GSTIN', style_head_row)
		recipient_sheet.write(0,3, 'ADDRESS 1', style_head_row)
		recipient_sheet.write(0,4, 'ADDRESS 2', style_head_row)
		recipient_sheet.write(0,5, 'PHONE', style_head_row)

		transport_sheet.write(0,0, 'S.No', style_head_row)
		transport_sheet.write(0,1, 'NAME', style_head_row)
		transport_sheet.write(0,2, 'GSTIN', style_head_row)
		transport_sheet.write(0,3, 'ADDRESS', style_head_row)
		transport_sheet.write(0,4, 'LOCATION', style_head_row)
		transport_sheet.write(0,5, 'PHONE', style_head_row)

		rrow = 1
		trow = 1
		for r in r:
			recipient_sheet.write(rrow,0, str(rrow), style_data_row)
			recipient_sheet.write(rrow,1, str(r.name), style_data_row)
			recipient_sheet.write(rrow,2, str(r.gstin), style_data_row)
			recipient_sheet.write(rrow,3, str(r.add1), style_data_row)
			recipient_sheet.write(rrow,4, str(r.add2), style_data_row)
			recipient_sheet.write(rrow,5, str(r.phone), style_data_row)
			rrow = rrow + 1

		for t in t:
			transport_sheet.write(trow,0, str(trow), style_data_row)
			transport_sheet.write(trow,1, str(t.name), style_data_row)
			transport_sheet.write(trow,2, str(t.gstin), style_data_row)
			transport_sheet.write(trow,3, str(t.add), style_data_row)
			transport_sheet.write(trow,4, str(t.location), style_data_row)
			transport_sheet.write(trow,5, str(t.phone), style_data_row)
			trow = trow + 1

		output = BytesIO()
		work_book.save(output)
		output.seek(0)

		response.write(output.getvalue())		
		return response

	else:
		return redirect('/')

def extract_bill_data(request):
	if request.user.is_superuser:
		b = bill_details.objects.all()

		response = HttpResponse(content_type='application/vnd.ms-excel') 
		response['Content-Disposition'] = 'attachment;filename=Bill Details.xls'

		work_book = xlwt.Workbook(encoding = 'utf-8') 
		work_sheet = work_book.add_sheet('Bill Details')

		style_head_row = xlwt.easyxf("""    
	    align:
	      wrap off,
	      vert center,
	      horiz center;
	    borders:
	      left THIN,
	      right THIN,
	      top THIN,
	      bottom THIN;
	    font:
	      name Arial,
	      colour_index white,
	      bold on,
	      height 0xA0;
	    pattern:
	      pattern solid,
	      fore-colour 0x19;
	    """
	    )

		style_data_row = xlwt.easyxf("""
	    align:
	      wrap on,
	      vert center,
	      horiz left;
	    font:
	      name Arial,
	      bold off,
	      height 0XA0;
	    borders:
	      left THIN,
	      right THIN,
	      top THIN,
	      bottom THIN;
	    """
	  	)

		style_data_row.num_format_str = 'MM/DD/YYYY'

		work_sheet.write(0,0, 'S.No.', style_head_row)
		work_sheet.write(0,1, 'Bill Number', style_head_row)
		work_sheet.write(0,2, 'Recipient', style_head_row)
		work_sheet.write(0,3, 'Recipient GSTIN', style_head_row)
		work_sheet.write(0,4, 'Transport', style_head_row)
		work_sheet.write(0,5, 'E-way Bill Number', style_head_row)
		work_sheet.write(0,6, 'Total Amount', style_head_row)
		work_sheet.write(0,7, 'Total Box', style_head_row)
		work_sheet.write(0,8, 'Total Quantity', style_head_row)
		work_sheet.write(0,9, 'Discount', style_head_row)
		work_sheet.write(0,10, 'Freight Charges', style_head_row)
		work_sheet.write(0,11, 'Payment Method', style_head_row)

		row = 1
		for r in b:
			work_sheet.write(row,0, str(row), style_data_row)
			work_sheet.write(row,1, str(r.bill_number), style_data_row)
			work_sheet.write(row,2, str(r.recipient.name), style_data_row)
			work_sheet.write(row,3, str(r.recipient.gstin), style_data_row)
			work_sheet.write(row,4, str(r.transport.name), style_data_row)
			work_sheet.write(row,5, str(r.ewaybill_number), style_data_row)
			work_sheet.write(row,6, str(r.total_amount), style_data_row)
			work_sheet.write(row,7, str(r.total_box), style_data_row)
			work_sheet.write(row,8, str(r.total_quantity), style_data_row)
			work_sheet.write(row,9, str(r.discount), style_data_row)
			work_sheet.write(row,10, str(r.freight_charges), style_data_row)
			work_sheet.write(row,11, str(r.payment_method), style_data_row)
			row = row + 1

		output = BytesIO()
		work_book.save(output)
		output.seek(0)

		response.write(output.getvalue())		
		return response

	else:
		return redirect('/')