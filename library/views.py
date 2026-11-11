from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import BookForm, MemberForm, CategoryForm
from .models import Book, Category, Member, Loan

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'book_count': Book.objects.count(),
        'member_count': Member.objects.count(),
        'active_loans': Loan.objects.filter(status='ISSUED').count(),
        'returned_count': Loan.objects.filter(status='RETURNED').count(),
        'overdue_count': Loan.objects.filter(status='ISSUED', due_date__lt=timezone.localdate()).count(),
        'recent_loans': Loan.objects.select_related('book', 'member')[:6],
    }
    return render(request, 'library/dashboard.html', context)

@login_required
def book_list(request):
    q = request.GET.get('q', '').strip()
    books = Book.objects.select_related('category').all()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q) |
                             Q(isbn__icontains=q) | Q(category__name__icontains=q))
    return render(request, 'library/book_list.html', {'books': books, 'q': q})

@login_required
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.available_copies = book.total_copies
        book.save()
        messages.success(request, 'Book added successfully.')
        return redirect('book_list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Book'})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        updated = form.save(commit=False)
        issued = book.total_copies - book.available_copies
        if updated.total_copies < issued:
            form.add_error('total_copies', f'There are already {issued} issued copies.')
        else:
            updated.available_copies = updated.total_copies - issued
            updated.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Book'})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        if book.loans.exists():
            messages.error(request, 'This book has loan history and cannot be deleted.')
        else:
            book.delete()
            messages.success(request, 'Book deleted.')
        return redirect('book_list')
    return render(request, 'library/confirm_delete.html', {'object': book, 'kind': 'book'})

@login_required
def member_list(request):
    q = request.GET.get('q', '').strip()
    members = Member.objects.all()
    if q:
        members = members.filter(Q(name__icontains=q) | Q(student_id__icontains=q) |
                                 Q(email__icontains=q) | Q(phone__icontains=q))
    return render(request, 'library/member_list.html', {'members': members, 'q': q})

@login_required
def member_create(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Member registered.')
        return redirect('member_list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Member'})

@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, 'Member updated.')
        return redirect('member_list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Member'})

@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        if member.loans.exists():
            messages.error(request, 'This member has loan history and cannot be deleted.')
        else:
            member.delete()
            messages.success(request, 'Member deleted.')
        return redirect('member_list')
    return render(request, 'library/confirm_delete.html', {'object': member, 'kind': 'member'})

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category added.')
        return redirect('category_list')
    return render(request, 'library/category_list.html', {'categories': categories, 'form': form})

@login_required
def issue_book(request):
    books = Book.objects.filter(available_copies__gt=0).order_by('title')
    members = Member.objects.all().order_by('name')
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=request.POST.get('book'))
        member = get_object_or_404(Member, pk=request.POST.get('member'))
        if book.available_copies < 1:
            messages.error(request, 'No copies are currently available.')
        elif Loan.objects.filter(book=book, member=member, status='ISSUED').exists():
            messages.error(request, 'This member already has this book issued.')
        else:
            with transaction.atomic():
                book.available_copies -= 1
                book.save(update_fields=['available_copies'])
                Loan.objects.create(book=book, member=member, issued_by=request.user,
                                    due_date=timezone.localdate() + timedelta(days=14))
            messages.success(request, 'Book issued. Due date is in 14 days.')
            return redirect('loan_list')
    return render(request, 'library/issue_book.html', {'books': books, 'members': members})

@login_required
def loan_list(request):
    status = request.GET.get('status', '')
    loans = Loan.objects.select_related('book', 'member', 'issued_by').all()
    if status in ('ISSUED', 'RETURNED'):
        loans = loans.filter(status=status)
    return render(request, 'library/loan_list.html', {'loans': loans, 'status': status})

@login_required
def return_book(request, pk):
    loan = get_object_or_404(Loan.objects.select_related('book'), pk=pk)
    if request.method == 'POST':
        if loan.status == 'RETURNED':
            messages.info(request, 'This book was already returned.')
        else:
            with transaction.atomic():
                loan.status = 'RETURNED'
                loan.return_date = timezone.localdate()
                loan.save(update_fields=['status', 'return_date'])
                loan.book.available_copies += 1
                loan.book.save(update_fields=['available_copies'])
            messages.success(request, f'Book returned. Fine: ₹{loan.fine}')
        return redirect('loan_list')
    return render(request, 'library/confirm_return.html', {'loan': loan})

@login_required
def reports(request):
    return render(request, 'library/reports.html', {
        'available_books': Book.objects.filter(available_copies__gt=0),
        'issued_loans': Loan.objects.filter(status='ISSUED').select_related('book', 'member'),
        'returned_loans': Loan.objects.filter(status='RETURNED').select_related('book', 'member'),
    })
