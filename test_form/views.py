from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, ProfileSearchForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .news import emergency_info
from django.http import HttpResponse
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    title = 'COVID-19 Self-Assessment System'
    context = {
        "title": title,
    }
    return render(request, "home.html", context)


def profile(request):
    score = 0
    title = 'Profile'
    form = ProfileForm(request.POST or None, initial={'name': request.user})

    if form.is_valid():
        temperature = form.cleaned_data['body_temperature']
        print(temperature)
        score = 0
        if str(temperature) < '100.9':
            score += 0
        else:
            score += 2

        sd = form.cleaned_data['symptom']
        count = 0

        for symptom in sd:
            print(symptom)
            if str(symptom) == 'Breathing problem':
                score += 3
                count = 1
                print(score)
            elif str(symptom) == 'Dry cough' and count == 0:
                score += 3
                count = 1

            elif str(symptom) == 'Dry cough' and count != 0:
                score += 1

            elif str(symptom) == 'Sore throat' and count == 0:
                score += 3
                count = 1

            elif str(symptom) == 'Sore throat' and count != 0:
                score += 1

            elif str(symptom) == 'Weakness' and count == 0:
                score += 3
                count = 1

            elif str(symptom) == 'Weakness' and count != 0:
                score += 1

            elif str(symptom) == 'Runny nose' and count == 0:
                score += 3
                count = 1

            elif str(symptom) == 'Runny nose' and count != 0:
                score += 1
            print(score)

        ad = form.cleaned_data['additional']
        for additional in ad:
            print(additional)
            if str(
                    additional) == 'Abdominal pain' or 'Vomiting' or 'Diarrhoea' or 'Chest pain or pressure' or 'Muscle pain' or 'Loss of taste or smell' or 'Rash on skin' or 'discoloration of fingers or toes' or 'Loss of speech or movement':
                score += 2
                print(score)
            print(score)

        newForm = form.save(commit=False)

        if score < 5:
            newForm.result = 'Negative'
            newForm.advice = 'isolation and contact doctor and follow advice.'
            newForm.emergency_info = 'You can take treatment at home.'

        elif score == 5:
            newForm.result = 'Positive'
            newForm.advice = 'isolation and contact doctor and follow advice.'
            newForm.emergency_info = 'You can take treatment at home.'

        elif 5 < score < 7:
            newForm.result = 'Positive'
            newForm.advice = 'isolation and contact doctor immediately and follow advice.'
            newForm.emergency_info = emergency_info

        elif score >= 7:
            newForm.result = 'Positive'
            newForm.advice = 'isolation and contact doctor immediately and follow advice . Also highly recommended to ' \
                             'be Hospitalized. '
            newForm.emergency_info = emergency_info

        newForm.user = request.user
        newForm.score = score
        newForm.is_tested = True
        newForm.save()
        form._save_m2m()

        return redirect('profile_details')
        # return redirect('profile_list')

    context = {
        "title": title,
        "form": form,
    }
    return render(request, "profile.html", context)


def profile_details(request):
    title = 'Profile Details'
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = Profile.objects.get(user=user)

        except:
            error = "Test First"
            return render(request, 'error_user.html', {'error': error})

        context = {
            'title': title,
            'profile': profile
        }

    return render(request, 'profile_details.html', context)


def profile_list(request):
    title = 'Profile List'
    form = ProfileSearchForm(request.POST or None)
    if form.is_valid():
        search_value = form.cleaned_data['name']

    queryset = Profile.objects.all().order_by('-created_at')

    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        "title": title,
        "form": form,
        "queryset": paged_listings,
    }
    if request.method == 'POST':
        try:
            queryset = Profile.objects.all().filter(name__icontains=search_value)
            context = {
                "title": title,
                "queryset": queryset,
                "form": form,
            }
        except:
            pass
        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Report list.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['NAME', 'Age', 'Sex', 'Temperature', 'Assessment Date', 'Assessment Score', 'COVID-19 Result'])
            instance = queryset
            for row in instance:
                writer.writerow(
                    [row.name, row.age, row.gender, row.body_temperature, row.created_at,
                     row.score, row.result])
            return response
    return render(request, "profile_list.html", context)


def profile_edit(request, id=None):
    instance = get_object_or_404(Profile, id=id)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        return redirect('profile_list')

    context = {
        "title": 'Edit ' + str(instance.name),
        "instance": instance,
        "form": form,
    }
    return render(request, "profile.html", context)


def profile_delete(request, id=None):
    instance = get_object_or_404(Profile, id=id)
    instance.delete()
    return redirect("profile_list")


def Login(request):
    if request.method == 'POST':
        utxt = request.POST['username']
        ptxt = request.POST['password']
        print('username:', utxt, 'password: ', ptxt)

        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt, password=ptxt)

            if user != None:
                login(request, user)
                return redirect('home')

    return render(request, 'login.html')


def Register(request):
    if request.method == 'POST':
        utxt = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(utxt, email, password, password2)
        if password != password2:
            error = "Password not matched"
            return render(request, 'error.html', {'error': error})

        count1 = 0
        count2 = 0
        count3 = 0
        for i in password:
            if "0" < i < "9":
                count1 = 1
            if "A" < i < "Z":
                count2 = 1
            if "a" < i < "z":
                count3 = 1

        if count1 == 0 or count2 == 0 or count3 == 0:
            error = "Your Password Didn't Strong Enough"
            return render(request, 'error.html', {'error': error})

        if len(password) < 8:
            error = "Your Password Must be Greater Than 8 Characters"
            return render(request, 'error.html', {'error': error})

        if len(User.objects.filter(username=utxt)) == 0 and len(User.objects.filter(email=email)) == 0:
            user = User.objects.create_user(username=utxt, email=email, password=password)
        else:
            error = "User already exists"
            return render(request, 'error.html', {'error': error})
        return redirect('login')
    return render(request, 'register.html')


def Logout(request):
    logout(request)
    return redirect('home')
