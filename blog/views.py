from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement
# Create your views here.
def animal_list(request):
    animaux = Animal.objects.filter()
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animaux': animaux,'equipements': equipements})




def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.disponibilite == "libre" and nouveau_lieu.id_equip == "mangeoire" and animal.etat == "affamé":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                animal.etat = "repus"
                animal.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.disponibilite == "libre" and nouveau_lieu.id_equip == "nid" and animal.etat == "fatigué":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                animal.etat = "endormi"
                animal.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.disponibilite == "libre" and nouveau_lieu.id_equip == "roue" and animal.etat == "repus":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                animal.etat = "fatigué"
                animal.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.id_equip == "litière" and animal.etat == "endormi":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                animal.etat = "affamé"
                animal.save()
                return redirect('animal_detail', id_animal=id_animal)
            else:
                message = 'problème'
                return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
    else:
        message='ok'
        form = MoveForm()
        return render(request, 'animalerie/animal_detail.html', {'animal': animal, 'lieu': lieu, 'form': form,'message':message})
