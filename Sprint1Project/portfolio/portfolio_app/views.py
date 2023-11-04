from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Golfer, Notebook, GolfRound
from .forms import GolfRoundForm, NotebookForm,GolferForm
from django.views import generic
from django.db import IntegrityError

def index(request):
    return render(request, 'portfolio_app/index.html')

def hours_of_operation(request):
    return render(request, 'portfolio_app/hours_of_operation.html')

def add_round(request, notebook_id):
    if request.method == "POST":
        form = GolfRoundForm(request.POST)
        if form.is_valid():
            golf_round = form.save(commit=False)
            golf_round.notebook_id = notebook_id
            golf_round.save()
            messages.success(request, "Round added successfully!")
            return redirect('notebook_detail', pk=notebook_id)
    else:
        form = GolfRoundForm()
    return render(request, 'portfolio_app/round_form.html', {'form': form})

def delete_round(request, pk):
    round = get_object_or_404(GolfRound, pk=pk)
    notebook_id = round.notebook.id
    round.delete()
    messages.success(request, "Deleted!")
    return redirect('notebook_detail', pk=notebook_id)


def update_round(request, pk):
    round = get_object_or_404(GolfRound, pk=pk)
    if request.method == 'POST':
        form = GolfRoundForm(request.POST, instance=round)
        if form.is_valid():
            form.save()
            notebook_id = round.notebook.id  # get the notebook_id from the GolfRound object
            return redirect('notebook_detail', pk=notebook_id)  # redirect to notebook_detail page
    else:
        form = GolfRoundForm(instance=round)
    return render(request, "portfolio_app/round_form.html", {'form': form})


def update_notebook(request, pk):
    notebook = get_object_or_404(Notebook, pk=pk)
    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)
        form.save()
        return redirect('notebook_detail', pk=pk)
    else:
        form = NotebookForm(instance=notebook)
    return render(request, "portfolio_app/notebook_form.html", {'form': form})


from django.db import IntegrityError

def add_golfer(request):
    if request.method == "POST":
        form = GolferForm(request.POST)
        if form.is_valid():
            try:
                new_golfer = form.save()
                #  a new Notebook is created for each Golfer
                new_notebook = Notebook.objects.create(golfer=new_golfer)
                messages.success(request, "Golfer added successfully!")
                return redirect('notebook_detail', pk=new_notebook.pk)  # redirect to the detail view of the new Notebook
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


class GolferListView(generic.ListView):
    model = Golfer

class GolferDetailView(generic.DetailView):
    model = Golfer

class NotebookListView(generic.ListView):
    model = Notebook
    queryset = Notebook.objects.all().prefetch_related('golfer')
    context_object_name = 'notebooks'  # override the default context name here

class NotebookDetailView(generic.DetailView):
    model = Notebook

    def get_context_data(self, **kwargs):
        golf_rounds = GolfRound.objects.all().filter(notebook__id=self.object.id)
        context = super().get_context_data(**kwargs)
        context["golf_rounds"] = golf_rounds
        return context

class GolfRoundListView(generic.ListView):
    model = GolfRound

class GolfRoundDetailView(generic.DetailView):
    model = GolfRound

