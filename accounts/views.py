from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from accounts.forms import CustomUserCreationForm

from .admin_utils import Trie


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/customuser_form.html"
    success_url = reverse_lazy("login")
    success_message = "Your profile was created successfully"


def add_trie_stock(request):
    """
    method creates a StockDictionary that queries all stocks already added to DB and adds them to the Trie
    visible on the page for superusers only. [see html template]
    """
    t = Trie()
    for word in t.stocks:
        t.insert_word(word.name)
    print(t.stocks)
    return redirect(reverse("pages:home"))
