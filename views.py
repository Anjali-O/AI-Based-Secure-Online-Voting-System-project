from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from .models import *
from User.models import *
from utils import encrypt_data, decrypt_data


# Create your views here.

def registration(request):
    if User.objects.exists():
        messages.warning(request, "Registration is not allowed as a user already exists.")
        return redirect(home)  # Redirect to home or another page of your choice

    if request.method == "POST":
        full_name = request.POST.get("full-name")
        your_email = request.POST.get("your-email")
        your_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        print(full_name, your_email, your_password, confirm_password)
        if your_password == confirm_password:

            if User.objects.filter(username=your_email).exists():
                messages.warning(request, "Email exist")
            else:
                user = User.objects.create_user(first_name=full_name, username=your_email, password=your_password,is_superuser =1)
                user.save()
                print("Data Inserted")
                return redirect(home)
        else:
            messages.warning(request, "Password mismatch")
    return render(request, "registration.html")


def home(request):
    return render(request, "home.html")




def signin(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            admin = User.objects.get(username=user)
            if admin.is_superuser is True:
                login(request, user)
                return redirect(home)
        else:
            messages.warning(request, "Account not found")
    return render(request, "login.html")




def otpgene(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(username=email).exists():
            def generate_otp():
                return random.randint(1000, 9999)

            otp = generate_otp()
            send_mail("OTP for Password Reset", f"Your OTP for forgot password verification is {otp}",
                      settings.EMAIL_HOST_USER, [email])
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['time'] = str(datetime.now())
            return redirect(passreset)
        else:
            messages.warning(request, "Account not Found")
    return render(request, "otpgenerate.html")


def passreset(request):
    otp = request.session.get('otp')
    print(otp)
    email = request.session.get('email')
    send_time = request.session.get('time')
    send_time = datetime.strptime(send_time,"%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    duration = current_time-send_time
    print(duration)
    if request.method == "POST":
        otp1 = int(request.POST.get("otp"))
        # print(type(otp1))
        new_password = request.POST.get("password")
        rnew_password = request.POST.get("npassword")
        if new_password == rnew_password:
            if otp == otp1 and duration <= timedelta(minutes=5):
                user = User.objects.get(username=email)
                user.set_password(new_password)
                user.save()
                return redirect(signin)
            elif otp == otp1 and duration > timedelta(minutes=5):
                messages.warning(request,"Time exceeded !!")
            else:
                messages.warning(request, "Invalid otp")
        else:
            messages.warning(request, "Password Mismatch")
    return render(request, "passwordreset.html")


def signout(request):
    logout(request)
    return redirect(home)


def view_candidate(request):
    all_candidates = Candidate.objects.all()
    print(all_candidates)
    return render(request, "view_all_candidate.html", {'all_candidates': all_candidates})


def add_candidate(request):
    all_districts = District.objects.all()
    if request.method == "POST":
        candidate_name = request.POST.get("candidate_name")
        candidate_party = request.POST.get("can_party")
        candidate_symbol = request.FILES.get("can_symbol",'')
        candidate_district_name = request.POST.get("district")
        candidate_bio = request.POST.get("can_bio")
        candidate_district = District.objects.get(district=candidate_district_name)

        print(candidate_name, candidate_party, candidate_symbol, candidate_district_name, candidate_bio, "hhhhhh")

        print(candidate_name,candidate_party,candidate_symbol,candidate_district.district,candidate_bio)
        candidate = Candidate.objects.create(candidate_name=candidate_name, candidate_party=candidate_party, candidate_symbol=candidate_symbol, candidate_district=candidate_district.district, candidate_bio=candidate_bio)
        candidate.save()
        print("candidate saved!")
        return redirect(view_candidate)
    return render(request, 'add_candidate.html', {'all_districts': all_districts})


def show_vote(request):
    candidates = Candidate.objects.all()
    for can in candidates:
        votes = Vote.objects.filter(candidate_id=can.id)
        can.count = votes.count()
    return render(request, 'showvote.html', {'votes': candidates})


def edit_candidate(request,cid):
    all_districts = District.objects.all()
    candidate = Candidate.objects.filter(pk=cid).values('candidate_name','candidate_party','candidate_symbol','candidate_district','candidate_bio')
    print(candidate)
    if request.method == "POST":
        new_candidate_name = request.POST.get("candidate_name")
        new_candidate_party = request.POST.get("can_party")
        new_candidate_symbol = request.FILES.get("can_symbol",Candidate.candidate_symbol)
        new_candidate_district_new = request.POST.get("district")
        new_candidate_bio = request.POST.get("can_bio")
        candidate_district = District.objects.get(district=new_candidate_district_new)
        update_candidate = Candidate.objects.get(pk=cid)

        update_candidate.candidate_name = new_candidate_name
        update_candidate.candidate_party = new_candidate_party
        update_candidate.candidate_symbol = new_candidate_symbol
        update_candidate.candidate_district = candidate_district.district
        update_candidate.candidate_bio = new_candidate_bio
        print(update_candidate)
        update_candidate.save()
        return redirect(view_candidate)

    return render(request,'edit_candidate.html',{'all_districts':all_districts ,'candidates':candidate})


def delete_candidate(request,cid):
    candidate = Candidate.objects.filter(pk=cid)
    print(candidate)
    candidate.delete()
    return redirect(view_candidate)


def add_state(request):
    if request.method == "POST":
        state = request.POST.get("state")
        print(state)
        state = State.objects.create(state=state)
        state.save()
        print("state saved!")
        return redirect(view_state)
    return render(request, 'add_state.html')


def view_state(request):
    all_states = State.objects.all()
    return render(request, 'view_state.html', {'all_states': all_states})


def edit_state(request,sid):
    state = State.objects.filter(pk=sid).values('state')
    print(state)
    if request.method == "POST":
        new_state = request.POST.get("state")
        update_state = State.objects.get(pk=sid)
        update_state.state = new_state
        print(update_state)
        update_state.save()
        return redirect(view_state)
    return render(request, 'edit_state.html', {'states': state})


def delete_state(request,sid):
    state = State.objects.filter(pk=sid)
    print(state)
    state.delete()
    return redirect(view_state)


def add_district(request):
    if request.method == "POST":
        district = request.POST.get("district")
        print(district)
        state_id = request.POST.get("state")
        print(state_id)
        state = get_object_or_404(State, pk=state_id)
        district = District.objects.create(district=district, state=state)
        district.save()
        print("district saved!")
        return redirect(view_district)

    all_states = State.objects.all()
    return render(request, 'add_district.html', {'all_states': all_states})


def view_district(request):
    all_districts = District.objects.select_related('state').all()
    return render(request, 'view_district.html', {'all_districts': all_districts})


def edit_district(request, did):
    district = District.objects.filter(pk=did).values('district')
    print(district)
    all_states = State.objects.all()
    if request.method == "POST":
        new_district = request.POST.get("district")
        new_state_id = request.POST.get("state")
        new_state = State.objects.get(pk=new_state_id)
        update_district = District.objects.get(pk=did)
        update_district.district = new_district
        update_district.state = new_state
        print(update_district)
        update_district.save()
        return redirect(view_district)
    return render(request, 'edit_district.html', {'districts': district, 'all_states': all_states})


def delete_district(request, did):
    district = District.objects.filter(pk=did)
    print(district)
    district.delete()
    return redirect(view_district)


def add_municipality(request):
    if request.method == "POST":
        district_id = request.POST.get("district")
        municipality_name = request.POST.get("municipality")
        print(f"District ID: {district_id}, Municipality: {municipality_name}")
        district = District.objects.get(pk=district_id)
        municipality = Municipality.objects.create(district=district, municipality=municipality_name)
        municipality.save()
        print("Municipality saved!")
        return redirect(view_municipality)
    districts = District.objects.all()  # Fetch districts for selection in form
    return render(request, 'add_municipality.html', {'districts': districts})


def view_municipality(request):
    all_municipalities = Municipality.objects.select_related('district').all() # Optimize query
    return render(request, 'view_municipality.html', {'all_municipalities': all_municipalities})


def edit_municipality(request, mid):
    municipality = Municipality.objects.get(pk=mid)
    districts = District.objects.all()

    if request.method == "POST":
        new_municipality_name = request.POST.get("municipality")
        new_district_id = request.POST.get("district")
        new_district = District.objects.get(pk=new_district_id)
        municipality.municipality = new_municipality_name
        municipality.district = new_district
        municipality.save()
        return redirect(view_municipality)
    return render(request, 'edit_municipality.html', {'municipality': municipality, 'districts': districts})


def delete_municipality(request, mid):
    municipality = Municipality.objects.get(pk=mid)
    print(f"Deleting: {municipality}")
    municipality.delete()
    return redirect(view_municipality)




#Wants to change this function for convert text into encrypt  on voterdetails table shows on admin home page first step


def add_voters(request):
    if request.method == "POST":
        v_aadhaar = request.POST.get("v_aadhaar")
        v_id = request.POST.get("v_id")
        v_name = request.POST.get("v_name")

        # Encrypt the data
        encrypted_aadhaar = encrypt_data(v_aadhaar)
        encrypted_v_id = encrypt_data(v_id)
        encrypted_v_name = encrypt_data(v_name)

        # Save encrypted data to the database
        voter = VoterDetails.objects.create(
            v_aadhaar=encrypted_aadhaar,
            v_id=encrypted_v_id,
            v_name=encrypted_v_name
        )
        voter.save()

        print("✅ Voter added with encrypted data!")
        return redirect(view_voters)  # Redirect to the voter list page

    return render(request, 'add_voters.html')




#This one for showing the all details currently encrypted wants to change it on decrypted

def view_voters(request):
    all_voters = VoterDetails.objects.all()

    # Create a new list with decrypted values
    decrypted_voters = []
    for voter in all_voters:
        decrypted_voters.append({
            'id': voter.id,  # Ensure ID is included for edit/delete URLs
            'v_aadhaar': decrypt_data(voter.v_aadhaar),
            'v_id': decrypt_data(voter.v_id),
            'v_name': decrypt_data(voter.v_name),
        })

    print('hello',decrypted_voters)  # Check if data is populated in the terminal

    return render(request, 'view_voters.html', {'all_voters': decrypted_voters})




def edit_voters(request, vid):

    voter = VoterDetails.objects.get(pk=vid)

    # Decrypt data before passing to the form
    decrypted_voter = {
        'v_aadhaar': decrypt_data(voter.v_aadhaar),
        'v_id': decrypt_data(voter.v_id),
        'v_name': decrypt_data(voter.v_name),
    }

    print("Decrypted Data:", decrypted_voter)  # Debugging

    if request.method == "POST":
        new_v_aadhaar = request.POST.get("v_aadhaar")
        new_v_id = request.POST.get("v_id")
        new_v_name = request.POST.get("v_name")

        # Encrypt updated data before saving
        voter.v_aadhaar = encrypt_data(new_v_aadhaar)
        voter.v_id = encrypt_data(new_v_id)
        voter.v_name = encrypt_data(new_v_name)

        voter.save()
        return redirect(view_voters)

    return render(request, 'edit_voters.html', {'voter': decrypted_voter})  # ✅ Correct key






def delete_voters(request,vid):
    voter = VoterDetails.objects.filter(pk=vid)
    print(voter)
    voter.delete()
    return redirect(view_voters)




#add decryption to user.first_name and pass to the UI

def view_user_reg(request):
    all_user_reg = UserReg.objects.all()

    decrypted_users = []
    for user_reg in all_user_reg:
        decrypted_first_name = decrypt_data(user_reg.user.first_name)  # Decrypt the first name

        decrypted_users.append({
            'user': user_reg.user,
            'decrypted_first_name': decrypted_first_name,  # Add decrypted first name
            'aadhaar': user_reg.aadhaar,
            'username': decrypt_data(user_reg.user.username),
            'state': user_reg.state,
            'district': user_reg.district,
            'municipality': user_reg.municipality
        })

    return render(request, 'view_reg_voters.html', {'reg_voters': decrypted_users})
