from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import NewUserForm,NameForm, TrainerForm, CollegeForm
from .mongo import mongodata
import datetime
from .invoice import create_invoice
from .send_mail import send_confirmation_email,send_invoice_email

# Create your views here.
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})


def homepage(request):
    return render(request, 'main/home.html')



def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})



def process(form):
    db = mongodata()
    d = dict()
    d['trainer_name'] = form.cleaned_data['Trainer']
    d['college_name'] = form.cleaned_data['College']

    td = db.trainer_details(d['trainer_name'])
    bd = db.bank_details(td['_id'])
    cl = db.college_location(d['college_name'])

    d['food'] = form.cleaned_data['Food']
    d['accomodation'] = form.cleaned_data['Accomodation']
    d['mode'] = form.cleaned_data['Mode_of_Training']
    d['base_location'] = td['location']
    d['phno'] = td['phno']

    if d['mode'] == 'online':
        d['food'] = 'No'
        d['accomodation'] = 'No'
        d['travel'] = 'No'
    elif d['mode'] == 'offline':
        if cl == d['base_location']:
            d['travel'] = 'No'
        else:
            d['travel'] = 'Yes'

    d['start_date'] = form.cleaned_data['Start_Date']
    d['end_date'] = form.cleaned_data['End_Date']
    d['pay_per_day'] = form.cleaned_data['Pay_per_day']
    d['no_of_days'] = str(d['end_date'] - d['start_date'] + datetime.timedelta(days=1)).split()[0]
    d['email'] = td['email']
    d['bank'] = bd['bank']
    d['acc'] = bd['acc_no']
    d['ifsc'] = bd['ifsc']
    d['pan'] = bd['pan']

    message = (
        "\nGreetings from genesis!!\nThis is an email confirmation post of our telephonic conversation about you\n"
        "associating with Genesis for our forthcoming project on the contractual basis.\n"
        "PFB the details about the project.\n")
    message += "\nName of the college : " + d['college_name']
    message += "\nRemuneration : INR " + str(d['pay_per_day']) + '/- per day incl of TDS'
    message += "\nStart date : " + str(d['start_date'])
    message += "\nEnd date : " + str(d['end_date'])
    message += "\nNo of days : " + str(d['no_of_days'])
    message += "\nMode of training : " + str(d['mode'])
    if d['accomodation'] == 'No':
        message += "\nAccomadation : Not Applicable"
    else:
        message += "\nAccomadation : Provided"
    if d['food'] == 'Yes':
        message += "\nFood Allowance : INR 150/day"
    else:
        message += "\nFood Allowance : Not Applicable"
    print(message)

    def get_dates():
        dates = list()
        temp = d['start_date']
        while temp <= d['end_date']:
            dates.append(str(temp))
            temp += datetime.timedelta(days=1)
        return dates

    d['dates'] = get_dates()
    invoice_path = create_invoice(d)
    print(invoice_path)


    try:
        send_confirmation_email(d['email'], message)
        print("Conformation email sent to ", d['email'])
    except Exception as e:
        print(e)
        print("Unable to send conformation email")

    try:
        send_invoice_email(invoice_path, d['college_name'], d['start_date'], d['end_date'])
        print('Invoice email sent')
    except Exception as e:
        print(e)
        print('Failed to send invoice')


def form_name_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            process(form)
            messages.success(request, "Invoice sent successfully!!")
            return redirect('/')
    else:
        form = NameForm()
        if form.is_valid():
            process(form)
            messages.success(request, "Invoice sent successfully!!")
            return redirect('/')
    return render(request, 'main/form.html', {'form': form})

def add_trainer(form):
    db = mongodata()
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    phno = form.cleaned_data['phno']
    location = form.cleaned_data['location']
    data1 = {'name': name, 'email': email, 'phno':phno, 'location':location}
    bank = form.cleaned_data['bank']
    acc_no = form.cleaned_data['acc_no']
    ifsc = form.cleaned_data['ifsc']
    pan = form.cleaned_data['pan']
    data2 = {'bank':bank, 'acc_no':acc_no, 'ifsc':ifsc, 'pan':pan}

    try:
        db.add_trainer(data1, data2)
    except:
        print("adding trainer failed")


def add_college(form):
    db = mongodata()
    name = form.cleaned_data['name']
    location = form.cleaned_data['location']
    data = {'name':name, 'location':location}

    try:
        db.add_college(data)
    except:
        print("adding college falied")

def form_add_trainer_view(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            add_trainer(form)
            messages.success(request, "Trainer added successfully!!")
            return redirect('/')

    else:
        form = TrainerForm()
        if form.is_valid():
            add_trainer(form)
            messages.success(request, "Trainer added successfully!!")
            return redirect('/')
    return render(request, 'main/addtrainer.html', {'form': TrainerForm})

def form_add_college_view(request):
    if request.method == 'POST':
        form = CollegeForm(request.POST)
        if form.is_valid():
            add_college(form)
            messages.success(request, "College added successfully!!")
            return redirect('/')
    else:
        form = CollegeForm()
        if form.is_valid():
            add_college(form)
            messages.success(request, "College added successfully!!")
            return redirect('/')
    return render(request, 'main/addcollege.html', {'form': CollegeForm})

def allcollege(request):
    db = mongodata()
    collegeList = db.college_names()
    collegeDict = {
        "names": collegeList,
    }
    return render(request, 'main/allcollege.html',collegeDict)

def alltrainer(request):
    db = mongodata()
    trainerList = db.trainer_names()
    trainerDict = {
        "names": trainerList,
    }
    return render(request, 'main/allcollege.html',trainerDict)