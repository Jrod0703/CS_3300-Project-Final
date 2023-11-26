from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Golfer, Notebook, GolfRound
from .forms import GolfRoundForm, NotebookForm, GolferForm, UserRegisterForm, UserLoginForm
from django.views import generic

from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

#returns the index.html 
def index(request):
    return render(request, 'portfolio_app/index.html')
#renders hours of ops page
def hours_of_operation(request):
    return render(request, 'portfolio_app/hours_of_operation.html')
#adds a round using the post method 
def add_round(request, notebook_id):
    if request.method == "POST":
        form = GolfRoundForm(request.POST)
        if form.is_valid():
            golf_round = form.save(commit=False)
            golf_round.notebook_id = notebook_id
            golf_round.save()
            messages.success(request, "Round added successfully!")
            #get the notebook_id from the GolfRound object
            return redirect('notebook_detail', pk=notebook_id)
    else:#creates epty form and then renders the form 
        form = GolfRoundForm()
    return render(request, 'portfolio_app/round_form.html', {'form': form})
#delete using update method and then redirects to notebokko detail
def delete_round(request, pk):
    round = get_object_or_404(GolfRound, pk=pk)
    notebook_id = round.notebook.id
    round.delete()
    messages.success(request, "Deleted!")
    return redirect('notebook_detail', pk=notebook_id)

#udpates a round using update method and redirect as well
def update_round(request, pk):
    round = get_object_or_404(GolfRound, pk=pk)
    if request.method == 'POST':
        form = GolfRoundForm(request.POST, instance=round)
        if form.is_valid():
            form.save()
            # get the notebook_id from the GolfRound object
            notebook_id = round.notebook.id  
             # redirect to notebook detail template 
            return redirect('notebook_detail', pk=notebook_id) 
    else:
        form = GolfRoundForm(instance=round)
    return render(request, "portfolio_app/round_form.html", {'form': form})

#grabs the notebook associated with the user.
def update_notebook(request, pk):
    notebook = get_object_or_404(Notebook, pk=pk, golfer__user=request.user)
    #creteas the form with post and all the others noteboos
    if request.method == 'POST':
        form = NotebookForm(request.POST, request.FILES, instance=notebook)
        if form.is_valid():
            form.save()
            return redirect('notebook_detail', pk=pk)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = NotebookForm(instance=notebook)
    return render(request, "portfolio_app/notebook_form.html", {'form': form})



def add_golfer(request):
    if request.method == "POST":
        form = GolferForm(request.POST)
        if form.is_valid():
            try:
                new_golfer = form.save()
                #  a new Notebook is created for each Golfer
                new_notebook = Notebook.objects.create(golfer=new_golfer)
                messages.success(request, "Golfer added successfully!")
                return redirect('notebook_detail', pk=new_notebook.pk) 
            #required to use unique email
            except IntegrityError:
                form.add_error('email', 'A golfer with that email already exists.')
    else:
        form = GolferForm()

    return render(request, 'portfolio_app/add_golfer.html', {'form': form})

def delete_golfer(request):
    if request.method == 'POST':
        golfer_name = request.POST.get('name')
        try:
            # tries to get the Golfer object by name
            golfer_to_delete = Golfer.objects.get(name=golfer_name)
            golfer_to_delete.delete()
            # if successful, send a success message
            messages.success(request, "Golfer deleted successfully!")
        except Golfer.DoesNotExist:
            # if the Golfer object is not found, send an error message
            messages.error(request, "Golfer not found.")
        # redirect to the home page regardless of the outcome
        return redirect('index')

    # if the request is not POST, render the delete page
    return render(request, 'portfolio_app/delete_golfer.html')


#  create registration view that saves both User and Golfer
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        golfer_form = GolferForm(request.POST)
        if user_form.is_valid() and golfer_form.is_valid():
            user = user_form.save()

            # saves the golfer with a reference to the user
            golfer = golfer_form.save(commit=False)
            golfer.user = user
            golfer.save()
            
            # creates a new notebook instance and associate it with the golfer on the spot ( had issues with this not working on part 1 got it fixed)
            notebook = Notebook(golfer=golfer)  
            notebook.save()

            # log in the user in after registering
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')  # redirect to the index page or dashboard
    else:
        user_form = UserRegisterForm()
        golfer_form = GolferForm()
    return render(request, 'portfolio_app/register.html', {
        'user_form': user_form,
        'golfer_form': golfer_form
    })


# create a login view using Django's authentication system
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'portfolio_app/login.html', {'form': form})

#  a logout view that logs out the user
def user_logout(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('index')



@login_required
def upload_file_to_notebook(request, pk):
    # Ensure the user owns the notebook
    notebook = get_object_or_404(Notebook, pk=pk, golfer__user=request.user)  #
    if request.method == 'POST' and 'file_field' in request.FILES:
        #adds
        notebook.image = request.FILES['file_field'] if 'image' in request.FILES['file_field'].content_type else notebook.image
        notebook.video = request.FILES['file_field'] if 'video' in request.FILES['file_field'].content_type else notebook.video
        notebook.save()
        messages.success(request, "File uploaded successfully!")
        return redirect('notebook_detail', pk=pk)
    else:
        return redirect('notebook_detail', pk=pk)  # Redirect to detail view if not a POST request or file not in request


def delete_media(request, pk, media_type):
    notebook = get_object_or_404(Notebook, pk=pk)
    user = request.user

    #  if the user has permission to delete the media
    if user == notebook.golfer.user:
        if media_type == 'image' and notebook.image:
            # deltes the image file
            notebook.image.delete()
            messages.success(request, "Image deleted successfully!")
        elif media_type == 'video' and notebook.video:
            # delets the video file
            notebook.video.delete()
            messages.success(request, "Video deleted successfully!")

    # redirects back to the notebook detail page
    return redirect('notebook_detail', pk=pk)


# updates views handling Notebook to ensure users can only update their own
class NotebookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Notebook
    form_class = NotebookForm
    template_name = 'portfolio_app/notebook_form.html'
    success_url = reverse_lazy('notebook-list')

    def get_queryset(self):
        """Override the get_queryset method to filter the Notebook to the logged-in user"""
        qs = super().get_queryset()
        return qs.filter(golfer__user=self.request.user)
#should display all notebooks, just cant change anything without being logged in
class NotebookListView(generic.ListView):
    model = Notebook
    context_object_name = 'notebooks'
    template_name = 'portfolio_app/notebook_list.html'

    def get_queryset(self):
        """Override the get_queryset method to allow users to see all notebooks, but only modify their own"""
        return Notebook.objects.all().prefetch_related('golfer')

class NotebookDetailView(generic.DetailView):
    model = Notebook
    template_name = 'portfolio_app/notebook_detail.html'

    def get_context_data(self, **kwargs):
        # the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # creates the rounds for this notebook
        context['golf_rounds'] = GolfRound.objects.filter(notebook=self.object).order_by('-date')
        context['is_owner'] = self.object.golfer.user == self.request.user
        return context
