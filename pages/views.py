from typing import Any, Dict

from accounts.admin_utils import Trie
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from stocks_app.models import Stock

from . import pages_utils
from .forms import StockEntryForm


class HomePageView(TemplateView):
    # template instead of FormView
    # https://stackoverflow.com/questions/8133505/django-templateview-and-form
    template_name = "pages/home.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            instance = context["form"].cleaned_data
            stock = instance["stock_abbreviation"].upper()

            try:
                # in case users types in an abbreviation that is not linked to any stock on Yahoo's website
                context = self.prepare_context(context, stock)
                # if error not raised then add the searched stock to the dictionary/Trie
                # Trie.insert_word(stock) #! - add condition to avoid duplicates
                #! add query to add to db ?
            except AttributeError:
                t = Trie()
                alt = t.alternatives(stock)
                # 'store' suggestions in session and 'forward' along with the redirect
                request.session["output"] = alt
                return HttpResponseRedirect(reverse("stocks:notfound"))

            if instance["add"] is True:
                self.add_to_watchlist(request, stock)

            return render(request, "pages/home.html", context=context)
        return super(TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # display form requesting an abreviation of a stock on yahoo to display basic data.
        # either POST or None evaluated from the left.
        # if no submission - None. If submission - data from the form (post)
        form = StockEntryForm(self.request.POST or None)
        context["form"] = form
        return context

    def prepare_context(self, context, stock):
        users_selected_stock_details = pages_utils.get_requested_stock_basic_data(stock)
        # to display what stock's data is displayed
        context["stock"] = stock.upper()

        # all attributes returned by get_requested_stock_basic_data are available
        #  under output.attribute_name in html templates
        context["output"] = users_selected_stock_details
        context["price_"] = "Price"  # text only - labels
        context["price_change_"] = "Price Change"  # text only - labels
        context["percent_change_"] = "Percent Change"  # text only - labels
        return context

    def add_to_watchlist(self, request, stock):
        """
        add the stock to user's watchlist. If Stock never searched before - create new entry in db, else:
        create relationship between user and the stock.
        """

        user = request.user
        try:
            st = Stock.objects.get(name=stock)
            user.stock.add(st)
        except Stock.DoesNotExist:
            st = Stock.objects.create(name=stock)
            user.stock.add(st)
