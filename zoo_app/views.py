from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
from django.contrib import messages

def logcheck(request):
    if 'active_user' in request.session:
        user = User.objects.get(id=request.session['active_user'])
        context ={
            "logged_in" : True,
            "user": user
        }
    else:
        context = {
            "logged_in" : False
        }
    return context

def index(request):
    context = logcheck(request)
    context['all_animals'] = Animal.objects.all()
    context['all_families'] = Family.objects.all()
    context['all_classes'] = Aniclass.objects.all()
    context['all_biomes'] = Biome.objects.all()
      
    return render(request, "index.html", context)

def index_redir(request):
    return redirect("/")


def register(request):
    context = logcheck(request)
    return render(request, "register.html", context)

def register_exe(request):
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        handle = request.POST['handle']
        email = request.POST['email']
        pwd = request.POST['pwd']   
        
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')

        posthash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, handle=handle, email=email, pwdhash = posthash)
        user = User.objects.last()
        request.session['active_user'] = user.id
    return redirect("/")

def logout(request):
    del request.session['active_user']
    return redirect('/')

def login(request):
    context= logcheck(request)
    return render(request, "login.html", context)

def login_exe(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST['email']
        pwd = request.POST['pwd']
       
        check = User.objects.authenticate(email, pwd)
        if check:
            user = User.objects.get(email=email)
            request.session['active_user'] = user.id
            return redirect("/")
        else:
            messages.error(request, "Email and Password do not match")
            return redirect("/login")
                          
    return redirect("/login")

def contribute(request):
    context = logcheck(request)
    return render(request, "contribute.html", context)

def animal(request, render_id):
    animal = Animal.objects.get(id=render_id)
    biome = animal.biome.first()
    all_biomes = animal.biome.all()
    comments = animal.comments.all()
    edits = animal.edits.all()
    context = logcheck(request)
    context["animal"] = animal
    context["biome"] = biome
    context["comments"] = comments
    context["edits"] = edits
    context['all_biomes'] = all_biomes
    return render(request, "animal.html", context)

def family(request, render_id):
    family = Family.objects.get(id=render_id)
    comments = family.comments.all()
    edits = family.edits.all()
    all_animals = family.animals.all()
    context = logcheck(request)
    context['family'] = family
    context['all_animals'] = all_animals
    context['comments'] = comments
    context['edits'] = edits
    
    return render(request, "family.html", context)

def aniclass(request, render_id):
    aniclass = Aniclass.objects.get(id=render_id)
    comments = aniclass.comments.all()
    edits = aniclass.edits.all()
    all_animals = aniclass.animals.all()
    context = logcheck(request)

    context['aniclass'] = aniclass
    context['all_animals'] = all_animals
    context['comments'] = comments
    context['edits'] = edits

    return render(request, "aniclass.html", context)

def biome(request, render_id):
    biome = Biome.objects.get(id=render_id)
    comments = biome.comments.all()
    edits = biome.edits.all()
    context = logcheck(request)

    context['biome'] = biome
    context['all_animals'] = biome.animals.all()
    context['comments'] = comments
    context['edits'] = edits
    return render(request, "biome.html", context)

def add_biome(request):
    
    context = logcheck(request)
    return render(request, "add_biome.html", context)

def add_biome_exe(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        img = request.FILES['img']
        obj = Biome.objects.create(name = name, desc=desc, img = img)
        obj.save()
        editor = User.objects.get(id = request.session['active_user'])
        Edit.objects.create(editor=editor, bedit=obj, text="Created")
        return redirect(f"/biomes/{obj.id}")
    return redirect('/')

def add_class(request):
    context = logcheck(request)
    return render(request, "add_class.html", context)

def add_class_exe(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        img = request.FILES['img']
        obj = Aniclass.objects.create(name = name, desc=desc, img = img)
        obj.save()
        editor = User.objects.get(id = request.session['active_user'])
        Edit.objects.create(editor=editor, cedit=obj, text="Created")
        return redirect(f"/aniclasses/{obj.id}")
    return redirect("/")

def add_family(request):

    all_classes = Aniclass.objects.all()
    context = logcheck(request)
    context['all_classes'] = all_classes
    return render(request, "add_family.html", context)

def add_family_exe(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        img = request.FILES['img']
        aniclass = Aniclass.objects.get(id=request.POST['class'])
        obj = Family.objects.create(name = name, aniclass= aniclass, desc=desc, img = img)
        obj.save()
        editor = User.objects.get(id = request.session['active_user'])
        Edit.objects.create(editor=editor, fedit=obj, text = "Created")
        return redirect(f"/families/{obj.id}")
    return redirect("/")

def add_animal(request):
    lastmade = Animal.objects.last()
    all_families = Family.objects.all()
    all_biomes = Biome.objects.all()
    context ={
        "all_families": all_families,
        "all_biomes": all_biomes,
    }
    if lastmade:
        context['lastmade'] = lastmade
    return render(request, "add_animal.html", context)

def add_animal_exe(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        biome = request.POST['biome']
        face_img = request.FILES['face_img']
        wide_img = request.FILES['wide_img']
        family = Family.objects.get(id=request.POST['family'])
        aniclass = family.aniclass
        obj = Animal.objects.create(name = name, family= family, aniclass= aniclass, desc=desc, face_img = face_img, wide_img = wide_img)
        obj.biome.add(biome)
        obj.save()
        editor = User.objects.get(id = request.session['active_user'])
        Edit.objects.create(editor=editor, aedit=obj, text="Created")
    return redirect(f"/animals/{obj.id}")

def user_profile(request, render_id):
    context= logcheck(request)
    render_user = User.objects.get(id=render_id)
    if 'user' in context:
        if context['user'] == render_user:
            context['match'] = True
        else:
            context['match'] = False
    else:
        context['match'] = False
    context['render_user'] = render_user
    context['render_user_comments'] = render_user.comments.all()
    context['render_user_edits'] = render_user.edits.all()
    return render(request, "user.html", context)

def edit_user(request):
    context= logcheck(request)
    if 'user' in context:
        return render(request, "edit_user.html", context)
    else:
        return redirect("/")

def edit_user_exe(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id=request.session['active_user'])
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        new_handle = request.POST['handle']
        old_handle = user.handle
        new_email = request.POST['email']
        old_email = user.email
         
        
        errors = User.objects.update_validator(first_name, last_name, old_handle, new_handle, old_email, new_email)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_user')

        
        user.first_name = first_name
        user.last_name = last_name
        user.handle = new_handle
        user.email = new_email
        user.save()
        return redirect(f"users/{user.id}")
    return redirect("/")

def comment(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        text = request.POST['text']
        target = request.POST['target']
        model_type = request.POST['model_type']
        if model_type == "animal":
            animal = Animal.objects.get(id=target)
            Comment.objects.create(text= text, commentor=user, acomment= animal)
            redir = "animals"
        if model_type == "aniclass":
            aniclass = Aniclass.objects.get(id=target)
            Comment.objects.create(text=text, commentor=user, ccomment= aniclass)
            redir = "aniclasses"
        if model_type == "family":
            family = Family.objects.get(id=target)
            Comment.objects.create(text=text, commentor=user, fcomment= family)
            redir = "families"
        if model_type == "biome":
            biome = Biome.objects.get(id=target)
            Comment.objects.create(text=text, commentor=user, bcomment= biome)
            redir = "biomes"

        
        return redirect(f"/{redir}/{target}")
    return redirect("/")

def edit_family(request, render_id):
    family = Family.objects.get(id=render_id)
    context = logcheck(request)
    context['family']= family
    return render(request, "edit_family.html", context)

def edit_family_exe(request):
    print("in POST")
    print(request.POST)
    print("in FILES")
    print(request.FILES)
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        family = Family.objects.get(id=request.POST['family_id'])
        if 'name' in request.POST:
            name = request.POST['name']
            desc = request.POST['desc']            
            family.name = name
            family.desc = desc
            family.save()
            Edit.objects.create(editor=user, fedit=family, text="Edited Name/Description")
        if 'img' in request.FILES:
            family.img = request.FILES['img']
            family.save()
            Edit.objects.create(editor=user, fedit=family, text="Updated Image")
        return redirect(f"/families/{family.id}")
    return redirect("/")

def edit_aniclass(request, render_id):
    aniclass = Aniclass.objects.get(id=render_id)
    context = logcheck(request)
    context["aniclass"] = aniclass
    return render(request, "edit_aniclass.html", context)

def edit_aniclass_exe(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        aniclass = Aniclass.objects.get(id=request.POST['aniclass_id'])
        if 'name' in request.POST:
            name = request.POST['name']
            desc = request.POST['desc']            
            aniclass.name = name
            aniclass.desc = desc
            aniclass.save()
            Edit.objects.create(editor=user, cedit=aniclass, text="Edited Name/Description")
        if 'img' in request.FILES:
            aniclass.img = request.FILES['img']
            aniclass.save()
            Edit.objects.create(editor=user, cedit=aniclass, text="Updated Image")
        return redirect(f"/aniclasses/{aniclass.id}")
    return redirect("/")

def edit_biome(request, render_id):
    biome = Biome.objects.get(id=render_id)
    context = logcheck(request)
    context['biome']= biome 
    return render(request, "edit_biome.html", context)

def edit_biome_exe(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        biome = Biome.objects.get(id=request.POST['biome_id'])
        if 'name' in request.POST:
            name = request.POST['name']
            desc = request.POST['desc']            
            biome.name = name
            biome.desc = desc
            biome.save()
            Edit.objects.create(editor=user, bedit=biome, text="Edited Name/Description")
        if 'img' in request.FILES:
            biome.img = request.FILES['img']
            biome.save()
            Edit.objects.create(editor=user, bedit=biome, text="Updated Image")
        return redirect(f"/biomes/{biome.id}")
    return redirect("/")

def edit_animal(request, render_id):
    animal = Animal.objects.get(id=render_id)
    all_biomes = Biome.objects.all()
    existing_biomes = animal.biome.all()
    potential_biomes=[]
    for biome in all_biomes:
        if biome not in existing_biomes:
            potential_biomes.append(biome)
    
    context = logcheck(request)
    context['animal'] = animal
    context['potential_biomes'] = potential_biomes
    context['existing_biomes'] = existing_biomes
    context['biome'] = existing_biomes.first()
    

    return render(request, "edit_animal.html", context)

def edit_animal_exe(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['active_user'])
        animal = Animal.objects.get(id=request.POST['animal_id'])
        if 'name' in request.POST:
            name = request.POST['name']
            desc = request.POST['desc']            
            animal.name = name
            animal.desc = desc
            animal.save()
            Edit.objects.create(editor=user, aedit=animal, text="Edited Name/Description")
        if 'biome' in request.POST:
            biome = Biome.objects.get(id=request.POST['biome'])
            animal.biome.add(biome)
            Edit.objects.create(editor=user, aedit=animal, text="Added Habitat")
        if 'kill_biome' in request.POST:
            biome = Biome.objects.get(id=request.POST['kill_biome'])
            animal.biome.remove(biome)
            Edit.objects.create(editor=user, aedit=animal, text="Removed Habitat")


        if 'face_img' in request.FILES:
            animal.face_img = request.FILES['face_img']
            animal.save()
            Edit.objects.create(editor=user, aedit=animal, text="Updated Face Image")
        if 'wide_img' in request.FILES:
            animal.wide_img = request.FILES['wide_img']
            animal.save()
            Edit.objects.create(editor=user, aedit=animal, text="Updated Wide Image")
        return redirect(f"/animals/{animal.id}")
    return redirect("/")