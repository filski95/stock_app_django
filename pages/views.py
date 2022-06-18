from django.shortcuts import render
from django.views.generic.base import TemplateView

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
            stock = instance["stock_abbreviation"]
            users_selected_stock_details = pages_utils.get_requested_stock_basic_data(stock)
            print(users_selected_stock_details)
            # to display what stock data are displayed
            context["stock"] = stock.upper()

            #! all attributes returned by get_requested_stock_basic_data are available
            #! under output.attribute_name in html templates
            context["output"] = users_selected_stock_details
            context["price_"] = "Price"  # text only - labels
            context["price_change_"] = "Price Change"  # text only - labels
            context["percent_change_"] = "Percent Change"  # text only - labels

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
