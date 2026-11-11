from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Document
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

@login_required
def home(request):
    today = timezone.now().date()
    soon_date = today + timedelta(days=30)
    urgent_date = today + timedelta(days=7)

    documents = Document.objects.filter(user=request.user)

    upcoming_documents = documents.filter(expiry_date__gte=today, expiry_date__lte=soon_date).order_by('expiry_date')
    
    total_documents = documents.count()

    active_documents = documents.filter(expiry_date__gte=today).count()

    expiring_soon = documents.filter(expiry_date__gte=today, expiry_date__lte=soon_date).count()

    urgent_documents = documents.filter(expiry_date__gte = today, expiry_date__lte=urgent_date).order_by('expiry_date')
    urgent_count = urgent_documents.count()

    expired_documents = documents.filter(expiry_date__lt=today).count()

    context = {
        'total_documents': total_documents,
        'active_documents': active_documents,
        'expiring_documents': expiring_soon,
        'expired_documents': expired_documents,
        'upcoming_documents': upcoming_documents,
        'urgent_count': urgent_count,
        'urgent_documents': urgent_documents,
    }

    return render(request, 'documents/home.html', context)

@login_required
def add_document(request):
    if request.method == 'POST':
        title = request.POST.get('title','').strip()
        document_type = request.POST.get('document_type','').strip()
        issue_date = request.POST.get('issue_date','').strip()
        expiry_date = request.POST.get('expiry_date','').strip()
        notes = request.POST.get('notes','').strip()

        if not all([title, document_type, issue_date, expiry_date]):
            return render(request,'documents/add_document.html',{'error': 'Please fill in all required fields.'})

        if expiry_date < issue_date:
            return render(request,'documents/add_document.html',{'error':'Expiry date cannot be before the issue date.'})

        Document.objects.create(
            user=request.user,
            title=title,
            document_type=document_type,
            issue_date=issue_date,
            expiry_date=expiry_date,
            notes=notes,
        )

        return redirect('home')
    return render(request,'documents/add_document.html')

@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title','').strip()
        document_type = request.POST.get('document_type','').strip()
        issue_date = request.POST.get('issue_date','').strip()
        expiry_date = request.POST.get('expiry_date','').strip()

        if title and document_type and issue_date and expiry_date:
            document.title = title
            document.document_type = document_type
            document.issue_date = issue_date
            document.expiry_date = expiry_date
            document.save()
            return redirect('home')

    return render(request, 'documents/edit_document.html',{
        'document': document
    })

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)

    if request.method == 'POST':
        document.delete()
        return redirect('home')

    return render(request, 'documents/delete_document.html', {
        'document': document
    })

@login_required
def all_documents(request):
    documents = Document.objects.filter(user=request.user).order_by('expiry_date')
    search_query = request.GET.get('search','').strip()
    selected_type = request.GET.get('type','').strip()
    selected_status = request.GET.get('status','').strip()

    today = timezone.localdate()
    soon_date = today + timedelta(days=30)

    if search_query:
        documents = documents.filter(title__icontains=search_query)

    if selected_type:
        documents = documents.filter(document_type=selected_type)

    if selected_status == 'expired':
        documents = documents.filter(expiry_date__lt = today)
    elif selected_status == 'expiring':
        documents = documents.filter(expiry_date__gte=today,expiry_date__lte=soon_date)
    elif selected_status == 'active':
        documents = documents.filter(expiry_date__gt=soon_date)

    document_types = Document.objects.values_list('document_type', flat=True).distinct()

    for document in documents:
        if document.expiry_date < today:
            document.status =  'Expired'
        elif document.expiry_date <= soon_date:
            document.status = 'Expiring Soon'
        else:
            document.status = 'Active'
        
    return render(request, 'documents/all_documents.html', {
        'documents':documents,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_status': selected_status,
        'document_types': document_types,
        'today':today,
        })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = CustomUserCreationForm()

    return render(request, 'documents/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'documents/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')