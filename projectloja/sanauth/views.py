import email
from logging import exception


from email import message
from email.message import EmailMessage
from multiprocessing import current_process
from webbrowser import get
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
 #from django.utils.encoding import force_bytes, force_text,DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.views.generic import View
import threading
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.core import mail
from django.core.mail import BadHeaderError,send_mail
from django.core.mail.message import EmailMessage
from django.urls import NoReverseMatch,reverse
from .utils import TokenGenerator
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator






class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)


    def run(self):
        self.email_message.send()

    

def cadastrar(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_passord=request.POST['pass2']
        if password!=confirm_passord:
            messages.warning(request, "SENHA e Confirmação não corresponde!")
            return render(request,'auth1/cadastrar.html')
        
        try:
            if User.objects.get(username=email):
               messages.warning(request,"este email já existe")
               return render(request,'auth1/cadastrar.html')
        
        except Exception as identifier:
            pass

        user = User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        current_site = get_current_site(request)
        email_subject = "Ativar sua conta"
        message=render_to_string ('auth1/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"Foi enviado um email para você ativar sua conta")
        return redirect('/sanauth/login/')
    
    return render(request,'auth1/cadastrar.html')

class ActivateContaView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Sua conta foi ativada com sucesso!")
            return redirect('/sanauth/login/')
    
        return render(request,"auth1/activatefalha.html")





def handlelogin(request):
    if request.method=="POST": 


        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"login com sucesso")
            return render(request,'index.html')
        
        else:
            messages.error(request,"Senha ou email não correspondem")
            return redirect('/sanauth/login/')
        
    return render(request,'auth1/login.html')



def handlelogout(request):
    logout(request)
    messages.success(request,"Saindo do sistema com sucessso")
    return redirect('/sanauth/login/')


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'auth1/request-reset-email.html')
    

    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            get_current_site = get_current_site(request)
            email_subject='[recupere sua senha]'
            message=render_to_string('auth1/reset-user-password.html',{
            
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token':PasswordResetTokenGenerator().make_token(user[0])
        })
            
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"Verifique seu email com as instruções de recuperação senha ")
        return redirect('/sanauth/login/')
    
    #return render(request,'auth1/reset-user-password.html')


class SetNovaSenhaView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
        }

        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator.check_token(user,token):
                messages.warning(request,"Senha e link não são validos")
                return render(request,'auth1/sanauth/login/')
        
        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request, 'auth1/set-novo-password.html',context)
        
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
        }
        password=request.POST['pass1']
        confirm_passord=request.POST['pass2']
        if password!=confirm_passord:
            messages.warning(request, "SENHA e Confirmação não corresponde!")
            return render(request,'auth1/set-novo-password.html',context)   
        
        
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Su senha foi recuperada com sucesso, faça seu login")
            return redirect(request,'sanauth/login/')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"aconteceu algo errado")
            return render(request,'auth1/set-novo-password.html',context)
        return render(request,'auth1/set-novo-password.html',context)

