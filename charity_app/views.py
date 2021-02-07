from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Sum
from django.contrib.auth.models import User
from charity_app.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request, msg=0):
        num_of_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        num_of_foundations = len(set([f.institution.name for f in Donation.objects.all()]))
        foundations = Institution.objects.filter(type=1)
        non_gov_orgs = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        return render(request, 'index.html', {'num_of_bags': num_of_bags,
                                              'num_of_foundations': num_of_foundations,
                                              'foundations': foundations,
                                              'non_gov_orgs': non_gov_orgs,
                                              'local_collections': local_collections
                                              })


class AddDonation(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all().order_by('-type')
            in_cat_ids = []
            for institution in institutions:
                in_cat_ids.append(institution.category_ids())
            return render(request, 'form.html', {'categories': categories,
                                                 'institutions': institutions,
                                                 'in_cat_ids': in_cat_ids
                                                 })
        return HttpResponseRedirect('register/')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('register/')


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('password2')
        if password == re_password and len(password) > 0:
            User.objects.create_user(username=email, password=password, first_name=name, last_name=surname)
            return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('register/')


class Donations(View):
    def get(self,request):
        donations = Donation.objects.filter(user=request.user)
        return render(request, 'donations.html', {'donations':donations})


class FormConfirmation(View):
    def get(self,request):
        return render(request,'form-confirmation.html')

    def post(self, request):
        quantity = int(request.POST.get('bags'))
        categories = request.POST.getlist('categories')
        institution = Institution.objects.get(id=request.POST.get('organization'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user

        categories_objects = []
        for category in categories:
            categories_objects.append(Category.objects.get(id=int(category)))
        categories_objects = tuple(categories_objects)
        new_donation = Donation()
        new_donation.quantity = quantity

        new_donation.institution = institution
        new_donation.address = address
        new_donation.phone_number = phone_number
        new_donation.city = city
        new_donation.zip_code = zip_code
        new_donation.pick_up_date = pick_up_date
        new_donation.pick_up_time = pick_up_time
        new_donation.pick_up_comment = pick_up_comment
        new_donation.user = user
        new_donation.save()
        new_donation.categories.add = categories_objects
        new_donation.save()

        return HttpResponseRedirect('confirmation/')


class Profile(View):
    def get(self,request):
        return render(request,'profile.html')


class MyDonations(View):
    def get(self,request):
        donations = Donation.objects.filter(user=request.user)
        return render(request,'donations.html',{'donations':donations})