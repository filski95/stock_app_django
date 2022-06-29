from typing import Any, Dict

from accounts.admin_utils import Trie
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
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

            try:  # in case users types in an abbreviation that is not linked to any stock on Yahoo's website
                context = self.prepare_context(context, stock)
            except AttributeError:
                t = Trie()

                alternative = t.alternatives(stock)
                print(f"alaternative {alternative}")
                # 'store' suggestions in session and 'forward' along with the redirect
                request.session["alternative"] = alternative
                return HttpResponseRedirect(reverse("stocks:notfound"))

            if instance["add"] is True:
                add_status = self.add_to_watchlist(request, stock)
                if add_status is False:
                    context["Error"] = "You have to log in in order to add stocks to the watchlist"

            return render(request, "pages/home.html", context=context)
        return super(TemplateView, self).render(context)

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
        context["price_header"] = "Price"  # text only - labels
        context["price_change_header"] = "Price Change"  # text only - labels
        context["percent_change_header"] = "Percent Change"  # text only - labels
        return context

    def add_to_watchlist(self, request, stock):
        """
        add the stock to user's watchlist. If Stock never searched before - create new entry in db, else:
        create relationship between user and the stock.
        """
        try:
            user = request.user
            try:
                st = Stock.objects.get(name=stock)
                user.stock.add(st)
            except Stock.DoesNotExist:
                st = Stock.objects.create(name=stock)
                user.stock.add(st)
        except AttributeError:
            return False
