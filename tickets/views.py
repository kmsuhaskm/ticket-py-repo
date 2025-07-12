from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, TicketForm, TicketReplyForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket, TicketReply
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'tickets/signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(user=request.user)
    status_filter = request.GET.get('status')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    return render(request, 'tickets/dashboard.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if not request.user.is_staff and request.user != ticket.user:
        return redirect('dashboard')

    replies = ticket.replies.all()
    if request.method == 'POST':
        form = TicketReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            reply.save()
            return redirect('ticket_detail', pk=pk)
    else:
        form = TicketReplyForm()
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'replies': replies, 'form': form})

@user_passes_test(is_admin)
def change_status(request, pk, status):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = status
    ticket.save()
    return redirect('dashboard')
