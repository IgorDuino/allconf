from django.shortcuts import render, redirect
from django.forms     import Form, CharField


def regname(request):
    form = SubdomenForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data["name"]
        return redirect(f"http://127.0.0.1:8000/{name}.allconf.com/")

    context = {
        "form" : form
    }

    return render(request, "subdomain/regname.html", context)


class SubdomenForm(Form):
    name = CharField(label="Название", max_length=50)

