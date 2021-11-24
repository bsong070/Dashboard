from . forms import DashboardForm, Notes, NotesForm, ToDo, ToDoForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import generic
from GoogleNews import GoogleNews


def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,
                          title=request.POST['title'],
                          description=request.POST['description']
                          )
            notes.save()
            messages.success(request, f"{notes} has been added.")
    else:
        form = NotesForm()

    note = Notes.objects.filter(user=request.user)
    context = {'notes': note, 'form': form}
    return render(request, 'dashboard/notes.html', context)


@login_required
def edit_note(request, pk=None):
    note = Notes.objects.get(id=pk)
    form = NotesForm(instance=note)

    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('/notes')

    context = {'form': form}
    return render(request, 'dashboard/edit_notes.html', context)


@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect(notes)


class NotesDetailView(generic.DetailView):
    model = Notes


def news(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        googlenews = GoogleNews()
        googlenews.search(text)
        news = googlenews.result()
        news_list = []
        for n in news:
            search_list = {
                'input': text,
                'title': n['title'],
                'media': n['media'],
                'img': n['img']
            }
            context = {
                'form': form,
                'results': news,
            }
            news_list.append(search_list)
        return render(request, 'dashboard/news.html', context)
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, "dashboard/news.html", context)


@login_required
def todo(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            try:
                complete = request.POST["completed"]
                if complete == 'on':
                    complete = True
                else:
                    complete = False
            except:
                complete = False
            todos = ToDo(
                user=request.user,
                title=request.POST["title"],
                completed=complete
            )
            todos.save()
            messages.success(
                request, "Item successfully added")
    else:
        form = ToDoForm()
    todo = ToDo.objects.filter(user=request.user)
    context = {
        'form': form,
        'todos': todo,
    }
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk=None):
    todo = ToDo.objects.get(id=pk)
    if todo.completed == True:
        todo.completed = False
    else:
        todo.completed = True
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    return redirect(todo)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"{username} registration is successful. Please log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, "dashboard/register.html", context)
