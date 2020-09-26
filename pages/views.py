from django.shortcuts import render
from random import choice
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, send_mail

# Create your views here.

def main(request):
	if request.POST:
		subjects = [
			'A letter listing my concerns',
			'Concerns with the recent admissions proposal',
			"Some feedback on the Board's admissions proposal",
		]
		subject = choice(subjects)
		context = {
			'form':request.POST,
			'mailto': f'mailto:{",".join(request.POST.getlist("rep"))}?subject={subject}'
		}
		html_message = render_to_string('pages/email_template.html', context=context)
		plain_message = strip_tags(html_message)
		#recepient = request.POST.getlist('rep')
		recepient = ['rushilwiz@gmail.com', 'lettertofcps@gmail.com']
		sender = [request.POST.get('email')]
		email = EmailMultiAlternatives(
			subject, 
			plain_message, 
			EMAIL_HOST_USER, 
			recepient, 
			cc=sender,
			reply_to=sender
		)
		email.attach_alternative(html_message, "text/html")
		print("### EMAIL SENT ###")
		email.send(fail_silently=False)
		return render (request, "pages/email.html", context=context)
	return render(request, "pages/index.html")
