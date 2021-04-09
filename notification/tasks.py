from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from tecwatch.settings import EMAIL_HOST_USER
from singhealth.models import Complaint
import datetime


@background(schedule = 5 * 60)
def send_notification():
    for tenant in User.objects.filter(groups__name='Tenant'):
        complaints = Complaint.objects.filter(tenant = tenant, status = 'Open').count()
        if complaints > 0:
            message = "Dear " + tenant.username + ",\n\nYou have " + str(complaints) + " unresolved complaints. \n\nPlease log onto the Singhealth retail management app to submit your rectification. \n\nThank you."
            subject = "Notification on Unresolved Complaints"
            mail_id = tenant.email
            email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
            email.content_subjtype = 'html'
            email.send()
            
        expired = Complaint.objects.filter(tenant=tenant, status = 'Expired')
        if expired.count() > 0:
            for e in expired:
                message = "Dear " + e.staff.username + ", \n\nThe complaint you had previously made against " + tenant.username + " has expired, and a rectification has not been made. \n\nYou may log onto the Singhealth retail management app to view the relevant details. \n\nThank you."
                subject = "Notification on Expired Complaint"
                mail_id = e.staff.email
                email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
                email.content_subjtype = 'html'
                email.send()
                
@background(schedule = 5 * 60)
def check_deadline():
    for complaint in Complaint.objects.filter(status='Open'):
        today = datetime.date.today()
        if today > complaint.deadline:
            complaint.status = "Expired"
            complaint.save()
            
@background()            
def update_notification(action, complaintid):
    complaint = Complaint.objects.get(id = complaintid)
    if action == "resolved":
        message = "Dear " + complaint.tenant.username + ", \n\nA complaint with subject: " + complaint.subject + " has been resolved. \n\nThank you for your timely rectification."
        subject = "Notification on Resolved Complaint"
        mail_id = complaint.tenant.email
        email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
        email.content_subjtype = 'html'
        email.send()
        
    elif action == "rectification":
        message = "Dear " + complaint.staff.username + ", \n\n" + complaint.tenant.username + " has uploaded a rectification for complaint with subject: " + complaint.subject + ". \n\nYou may log onto the Singhealth retail management app to view the rectification details. \n\nThank you."
        subject = "Notification on Uploaded Rectification"
        mail_id = complaint.staff.email
        email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
        email.content_subjtype = 'html'
        email.send()
        
    
            
#python manage.py process_tasks
