from django.shortcuts import render, redirect
from django.forms     import Form, CharField
from django.conf      import settings


def regname(request):
    form = SubdomenForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data["name"]
        return redirect(f"http://{name}.{settings.SITE}/check/")

    context = {
        "form": form
    }

    return render(request, "subdomain/regname.html", context)


def check(request):
    name = request.build_absolute_uri().split(settings.SITE)[0][:-1][::-1]
    for i, sym in enumerate(name):
        if not sym.isalnum():
            name = name[:i][::-1]
            break

    context = {
        "name" : name
    }

    return render(request, "subdomain/subdm.html", context)


class SubdomenForm(Form):
    name = CharField(label="Название", max_length=50)

