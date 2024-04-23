from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,LoginForm,Taskform
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator


def signin_required(fn):

     def wrapper(request,**kwargs):

          if not request.user.is_authenticated:

               return redirect('signin')
          
          else:

               return fn(request,**kwargs)
          
     return wrapper


def mylogin(fn):
     def wrapper(request,**kwargs):
          id=kwargs.get('pk')
          obj=Taskmodel.objects.get(id=id)

          if obj.user!=request.user:

               return redirect('signin')
          else:
               return fn(request,**kwargs)
          
     return wrapper

class Registration(View):
     def get(self,request,**kwargs):
          
          form=Register()
          return render(request,"register.html",{'form':form})
     


     def post(self,request,**kwargs):
          print(request.POST)
          form=Register(request.POST)
           
          if form.is_valid():
               #form.cleaned_data
               User.objects.create_user(**form.cleaned_data)
               # modelname.objects.create(form.cleaned_data)
               form=Register()
          return redirect('signin')
     



class Signin(View):
      def get(self,request,**kwargs):
           
           form=LoginForm()
           return render(request,'login.html',{'form':form})
      

      def post(self,request,**kwargs):
           
           form=LoginForm(request.POST)

           if form.is_valid():   #username and password
                
                print(form.cleaned_data)

                u_name=form.cleaned_data.get("username")   
                
                                                            #getting username from cleaned_data
                pwd=form.cleaned_data.get("password")

                user_obj=authenticate(username=u_name,password=pwd)

                if user_obj:
                     
                   print('Valid credentials.')
                   login(request,user_obj)
                   return redirect('task')
                else:
                    print("incorrect credential")
                    return redirect("signin")
            

@method_decorator(signin_required,name='dispatch')
class Add_task(View):

     def get(self,request,**kwargs):

          form=Taskform()
          data=Taskmodel.objects.filter(user=request.user).order_by('completed')       #there is a method all()(including other users) to display whole tasks.

          return render(request,"index.html",{"form":form,"data":data})
     
     def post(self,request,**kwargs):

          form=Taskform(request.POST)

          if form.is_valid():
               form.instance.user=request.user
               form.save()
               form=Taskform()
               messages.success(request,"Task added successfully.")
          data=Taskmodel.objects.filter(user=request.user).order_by('completed')
          return render(request,"index.html",{"form":form,'data':data})
                

@method_decorator(signin_required,name='dispatch')
@method_decorator(mylogin,name='dispatch')
class Delete_task(View):

     def get(self,request,**kwargs):

          id=kwargs.get('pk')

          Taskmodel.objects.get(id=id).delete()

          return redirect('task')
     


class Task_edit(View):

     def get(self,request,*args,**kwargs):

          id=kwargs.get('pk')
          obj = Taskmodel.objects.get(id=id)
          if obj.completed == False:
               obj.completed=True
               obj.save()
          return redirect('task')
     


class Signout(View):

     def get(self,request):

          logout(request)

          return redirect('signin') 
     


class User_del(View):

     def get(self,request,**kwargs):

          id=kwargs.get('pk')
          User.objects.get(id=id).delete()
          return redirect('signin')


class Update_user(View):

     def get(self,request,**kwargs):

          id=kwargs.get('pk')

          data=User.objects.get(id=id)

          form=Register(instance=data)

          return render(request,'register.html',{'form':form})
     


     def post(self,request,**kwargs):

          id=kwargs.get('pk')

          data=User.objects.get(id=id)

          form=Register(request.POST,instance=data)

          if form.is_valid():

               form.save()

               return render(request,'register.html')