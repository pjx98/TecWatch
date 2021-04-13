from django.shortcuts import render, redirect
import xlwt
from checklist.decorators import *
from datetime import datetime
from django.urls import reverse

from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from tecwatch.settings import EMAIL_HOST_USER

from checklist.models import ChecklistItem, Checklist, ChecklistScore

# Create your views here.
def export_excel(request):
    
    if request.method == "POST":
        # Get audit id
        auditId = request.POST.get('auditId', -1)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Audits' + "_" + \
        str(datetime.today().strftime('%Y-%m-%d')) + '.xls'
        
    wb = xlwt.Workbook(encoding='utf-8')
    ws =  wb.add_sheet('Audits')
    #row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    rows=['Date of Audit','Tenant Involved', 'Satisfactory Fields', 'Unsatisfactory Fields', 'Total Score'] ##the header names of the column what should be exported?

    # Create Row 0
    for row_num in range(len(rows)):
        ws.write(row_num,0,rows[row_num],font_style )
        #writing the name of the contents into the column header  into the workbook in 135 
    
    font_style=xlwt.XFStyle()
    
    # Query model using the id
    
    audit = ChecklistScore.objects.get(id = int(auditId[0:len(auditId)-1]))
    
    # row, column, args
    # Input  values into the respective rows
    ws.write(0,1, str(audit.date_created))
    ws.write(1,1, str(audit.tenant.username))
    ws.write(2,1, str(audit.checked))
    ws.write(3,1, str(audit.unchecked))
    ws.write(4,1, str(audit.score))
    
        
    wb.save(response)
    return response

def go_to_email(request):
    context = {}
    
    if request.method == 'POST':
        tenantId = request.POST.get('tenantId', -1)
        tenant = User.objects.get(username=tenantId)
        context['tenant'] = tenant
        return render(request, 'email.html', context)

def send_mail_plain_with_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)

    email.send()
    return redirect(reverse("homestaff"))

    
    