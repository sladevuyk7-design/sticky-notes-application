from django.shortcuts import render, get_object_or_404, redirect
from .models import StickyNote
from .forms import StickyNoteForm


# Display all sticky notes
def note_list(request):
    notes = StickyNote.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


# Display one sticky note
def note_detail(request, pk):
    note = get_object_or_404(StickyNote, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


# Create a sticky note
def note_create(request):
    if request.method == 'POST':
        form = StickyNoteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = StickyNoteForm()

    return render(request, 'notes/note_form.html', {'form': form})


# Edit a sticky note
def note_update(request, pk):
    note = get_object_or_404(StickyNote, pk=pk)

    if request.method == 'POST':
        form = StickyNoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = StickyNoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form})


# Delete a sticky note
def note_delete(request, pk):
    note = get_object_or_404(StickyNote, pk=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')

    return render(request, 'notes/note_confirm_delete.html', {'note': note})