from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.db.models import Max
from .forms import *
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
import string
import random
import asyncio
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
# Create your views here.

"""
DEBUG 	Development-related messages that will be ignored (or removed) in a production deployment
INFO 	Informational messages for the user
SUCCESS 	An action was successful, e.g. “Your profile was updated successfully”
WARNING 	A failure did not occur but may be imminent
ERROR 	An action was not successful or some other failure occurred

"""
###############
# General Pages
###############

loop = asyncio.get_event_loop()


# A function for Authorizing users for each view
def authorized(request , roles):
    if request.user.role in roles:
        return True
    return False


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(request , username=username , password=password)
            if user :
                login(request , user)
                return redirect('summary')
            else :
                messages.error(request , "Wrong Credentials")
                redirect('login')
        else:
            messages.error(request, "Please submit both Username and Password")
            return redirect('login')
    return render(request , 'page-login.html' , {})

def logout_user(request):
    logout(request)
    messages.success(request , "You've been logged out successfuly")
    return redirect('login')

@login_required
def summary(request):
    if authorized(request,roles=['Administrator','Accountant']):
        users_count = User.objects.all().count()
        branches_count = Branch.objects.all().count()
        tags_count = Tag.objects.all().count()
        items_count = Item.objects.all().count()
        max_item_count = Item.objects.aggregate(Max('total_count'))
        max_item_price = Item.objects.aggregate(Max('price'))
        context = {
            'users_count':users_count,
            'branches_count':branches_count,
            'tags_count':tags_count,
            'items_count':items_count,
            'max_item_count': max_item_count,
            'max_item_price': max_item_price,
        }

        return render(request, 'summary.html', context)
    else:
        return redirect(item_list)



def generate_users():
    branches_list = [i for i in Branch.objects.all()]
    for i in range(1000):
        first_name = '{}'.format(get_random_string(10,string.ascii_letters))
        middle_name = '{}'.format(get_random_string(10,string.ascii_letters))
        last_name = '{}'.format(get_random_string(10,string.ascii_letters))
        username = 'user_{}'.format(get_random_string(10,string.ascii_letters))
        password = 'password_{}'.format(get_random_string(10,string.ascii_letters))
        email = '{}@{}.com'.format(username,username)
        phone = '{}'.format(get_random_string(10,string.digits))
        address = 'address_{}'.format(get_random_string(40,string.ascii_letters))
        role = '{}'.format(random.choice(['Administrator','Employee','Accountant']))
        branch = random.choice(branches_list)
        photo = "/users_images/anonymous.png"
        is_staff = False
        is_active = True
        user = User.objects.create_user(
            email=email, password=password, username=username,first_name=first_name, middle_name=middle_name,last_name=last_name, phone=phone, role=role, branch=branch, address=address, photo=photo, is_active=is_active,is_staff=is_staff)
        print(user)


def generate_items():
    branches_list = [i for i in Branch.objects.all()]
    tags_id_list = [ i for i in Tag.objects.all() ]
    for i in range(10000):
        name = 'item_{}'.format(get_random_string(10,string.ascii_letters))
        branch = random.choice(branches_list)
        price = float(get_random_string(5,string.digits))
        description = 'description_{}'.format(get_random_string(40,string.ascii_letters))
        photo = "/items_images/item.png"
        total_count = int(get_random_string(3,string.digits))
        tags = tags_id_list
        item = Item(name=name,branch=branch,price=price,description=description,photo=photo,total_count=total_count)
        item.save()
        item.tags.set(tags)
        print(item)


@login_required
def call_users_generator(request):
    loop.run_in_executor(None,generate_users)
    messages.info(request, "Refresh the page and notice change in number of users")
    return redirect('summary')

@login_required
def call_items_generator(request):
    loop.run_in_executor(None,generate_items)
    messages.info(request, "Refresh the page and notice change in number of items")
    return redirect('summary')

@login_required
def not_found(request):
    return render(request ,'404.html')

@login_required
def unauthorized(request):
    return render(request , '401.html')


##############
# users views#
##############





@login_required
def user_list(request):
    if authorized(request, roles=['Administrator']):
        all_users = User.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_users, 20)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request , 'users/list_users.html' , {'users':users})
    else:
        return redirect(unauthorized)

@login_required
def user_create(request):
    if authorized(request, roles=['Administrator']):
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                is_staff = cd['is_staff']
                user = None
                if is_staff:
                    user = User.objects.create_superuser(
                        email = cd['email'],password = cd['password'],username = cd['username'],
                        first_name= cd['first_name'],middle_name = cd['middle_name'],
                        last_name = cd['last_name'],phone = cd['phone'],role = cd['role'],branch = cd['branch'],
                        address = cd['address'],photo = cd['photo'],is_active = cd['is_active'],
                        is_staff=is_staff)
                    if user:
                        messages.success(request, "User Created Successfully!")
                        return redirect(user_list)
                    else:
                        messages.error(request, "User Not Created")
                        return redirect('user-create')
                else:
                    user = User.objects.create_user(
                        email = cd['email'],password = cd['password'],username = cd['username'],
                        first_name= cd['first_name'],middle_name = cd['middle_name'],
                        last_name = cd['last_name'],phone = cd['phone'],role = cd['role'],branch = cd['branch'],address = cd['address'],photo = cd['photo'],is_active = cd['is_active'],
                        is_staff=is_staff)
                    if user:
                        messages.success(request, "User Created Successfully!")
                        return redirect('users-list')
                    else:
                        messages.error(request, "User Not Created")
                        return redirect('user-create')
        else:
            return render(request, 'users/create_user.html', {'form': form})
    else:
        return redirect(unauthorized)


@login_required
def user_update(request , id='None'):
    if authorized(request, roles=['Administrator']):
        form = UserForm()
        user = User.objects.filter(id=id).first()
        if user:
            form = UserForm(request.POST or None , instance=user )
            if request.method == 'POST':
                form = UserForm(request.POST , request.FILES  , instance=user)
                if form.is_valid():
                    cd = form.cleaned_data
                    saved = form.save(cd)
                    if saved:
                        messages.success(request, "User Updated Successfully!")
                        return redirect(user_list)
                    else:
                        messages.error(request, "User Not Updated")
                        return redirect('user-update', id=user.id)
                else:
                    messages.error(request, "Data is not valid")
                    return redirect('user-update', id=user.id)
            else:
                return render(request, 'users/update_user.html', {'form': form, 'user': user})
        else:
            return redirect(not_found)
    else:
        return redirect(unauthorized)


@login_required
def user_show(request , id='None'):
    if authorized(request, roles=['Administrator']):
        user = User.objects.filter(id=id).first()
        if user:
            return render(request , 'users/show_user.html' , {'user':user})
        else:
            messages.error(request, "No User Found")
            return redirect('not_found')
    else:
        return redirect(unauthorized)

@login_required
def user_delete(request , id):
    if authorized(request, roles=['Administrator']):
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            messages.success(request, "User Deleted Successfully!")
            return redirect(user_list)
        else:
            return redirect(not_found)
    else:
        return redirect(unauthorized)



#################
# branches views#
#################

@login_required
def branch_list(request):
    if authorized(request, roles=['Administrator']):
        all_branches = Branch.objects.all
        return render(request , 'branches/list_branches.html' , {'all_branches':all_branches})
    else:
        return redirect(unauthorized)


@login_required
def branch_create(request):
    if authorized(request, roles=['Administrator']):
        form = BranchForm()
        if request.method == 'POST':
            form = BranchForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                form.save(cd)
                messages.success(request , "Branch Created Successfully!")
                return redirect('branches-list')
            else:
                messages.error(request , "Branch Not Created")
                return redirect('branch-create')
        return render(request, 'branches/create_branch.html', {'form': form})
    else:
        return redirect(unauthorized)

@login_required
def branch_update(request , id='None'):
    if authorized(request, roles=['Administrator']):
        form = BranchForm()
        branch = Branch.objects.filter(id=id).first()
        if branch:
            form = BranchForm(request.POST or None , instance=branch)
        else:
            return redirect(not_found)
        if request.method == 'POST':
            if form.is_valid():
                cd = form.cleaned_data
                form.save(cd)
                messages.success(request , "Branch Updated Successfully!")
                return redirect(branch_list)
            else:
                messages.error(request , "Branch Not Updated")
                return redirect(branch_update)
        return render(request, 'branches/update_branch.html', {'form': form, 'branch': branch})
    else:
        return redirect(unauthorized)


@login_required
def branch_delete(request , id):
    if authorized(request, roles=['Administrator']):
        branch = Branch.objects.filter(id=id).first()
        if branch:
            branch.delete()
            messages.success(request, "Branch Deleted Successfully!")
            return redirect(branch_list)
        else:
            return redirect(not_found)
    else:
        return redirect(unauthorized)


#################
# tags views#
#################

@login_required
def tag_list(request):
    if authorized(request, roles=['Administrator']):
        all_tags = Tag.objects.all
        return render(request , 'tags/list_tags.html' , {'all_tags':all_tags})
    else:
        return redirect(unauthorized)

@login_required
def tag_create(request):
    if authorized(request, roles=['Administrator']):
        form = TagForm()
        if request.method == 'POST':
            form = TagForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                form.save(cd)
                messages.success(request , "Tag Created Successfully!")
                return redirect(tag_list)
            else:
                messages.error(request , "Tag Not Created")
                return redirect(tag_create)
        return render(request, 'tags/create_tag.html', {'form': form})
    else:
        return redirect(unauthorized)

@login_required
def tag_update(request , id='None'):
    if authorized(request, roles=['Administrator']):
        form = TagForm()
        tag = Tag.objects.filter(id=id).first()
        if tag:
            form = TagForm(request.POST or None , instance=tag)
        else:
            return redirect(not_found)
        if request.method == 'POST':
            if form.is_valid():
                cd = form.cleaned_data
                form.save(cd)
                messages.success(request , "Tag Updated Successfully!")
                return redirect(tag_list)
            else:
                messages.error(request , "Tag Not Updated")
                return redirect(tag_update)
        return render(request, 'tags/update_tag.html', {'form': form, 'tag': tag})
    else:
        return redirect(unauthorized)


@login_required
def tag_delete(request , id):
    if authorized(request, roles=['Administrator']):
        tag = Tag.objects.filter(id=id).first()
        if tag:
            tag.delete()
            messages.success(request, "Tag Deleted Successfully!")
            return redirect(tag_list)
        else:
            return redirect(not_found)
    else:
        return redirect(unauthorized)


##############
# items views#
##############

@login_required
def item_list(request):
    if authorized(request, roles=['Administrator','Employee','Accountant']):
        all_items = Item.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_items, 20)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return render(request , 'items/list_items.html' , {'items':items})
    else:
        return redirect(unauthorized)

@login_required
def item_create(request):
    if authorized(request, roles=['Administrator','Employee']):
        form = ItemForm()
        if request.method == 'POST':
            form = ItemForm(request.POST , request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                if request.user.role == 'Employee':
                    if cd['branch'] == request.user.branch:
                        form.save(cd)
                        messages.success(request, "Item Created Successfully!")
                        return redirect(item_list)
                    else:
                        messages.error(request, "Employee and Item should be in same branch")
                        return redirect(item_create)
                if request.user.role == 'Administrator':
                    form.save(cd)
                    messages.success(request , "Item Created Successfully!")
                    return redirect(item_list)
            else:
                messages.error(request , "Item Not Created")
                return redirect(item_create)
        return render(request, 'items/create_item.html', {'form': form})
    else:
        return redirect(unauthorized)

@login_required
def item_update(request , id='None'):
    if authorized(request, roles=['Administrator','Employee']):
        form = ItemForm()
        item = Item.objects.filter(id=id).first()
        if item:
            form = ItemForm(request.POST or None , instance=item)
        else:
            return redirect(not_found)
        if request.method == 'POST':
            form = ItemForm(request.POST , request.FILES , instance=item)
            if form.is_valid():
                cd = form.cleaned_data
                if request.user.role == 'Employee':
                    if cd['branch'] == request.user.branch:
                        form.save(cd)
                        messages.success(request, "Item Updated Successfully!")
                        return redirect(item_list)
                    else:
                        messages.error(request, "Employee and Item should be in same branch")
                        return redirect('item-update', id=item.id)
                if request.user.role == 'Administrator':
                    form.save(cd)
                    messages.success(request , "Item Created Successfully!")
                    return redirect(item_list)
            else:
                messages.error(request , "Item Not Updated")
                return redirect('item-update', id=item.id)
        return render(request, 'items/update_item.html', {'form': form, 'item': item})
    else:
        return redirect(unauthorized)

@login_required
def item_show(request , id):
    if authorized(request, roles=['Administrator']):
        item = Item.objects.filter(id=id).first()
        if item:
            return render(request , 'items/show_item.html' , {'item':item})
        else:
            messages.error(request, "No Item Found")
            return redirect('not_found')
    else:
        return redirect(unauthorized)


@login_required
def item_delete(request , id):
    if authorized(request, roles=['Administrator']):
        item = Item.objects.filter(id=id).first()
        if item:
            item.delete()
            messages.success(request, "Item Deleted Successfully!")
            return redirect(item_list)
        else:
            return redirect(not_found)
    else:
        return redirect(unauthorized)