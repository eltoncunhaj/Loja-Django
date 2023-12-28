from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages






def cadastrar(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_passord = request.POST['pass2']
        if password!=confirm_passord:
            messages.warning(request, "SENHA e Confirmação não corresponde!")
            return render(request,'auth1/cadastrar.html')
        
        try:
            if User.objects.get(username=email):
                messages.warning(request,"este email já existe")
                return render(request,'auth1/cadastrar.html')
        except Exception as identifier:
            pass

        myuser = User.objects.create_superuser(email,email,password)
        myuser.save()
        messages.info(request,"Cadastro realizado com sucesso, faça seu login!")
        return redirect('/sanauth/login')
    return render(request,'auth1/cadastrar.html')


    
    
    return render(request,'auth1/cadastrar.html')

def handlelogin(request):
    return render(request,'auth1/login.html')

