from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from buyer.models import Buyer, Mobile, MobileNumber, Stuff, StuffType
from .forms import (
    AutoCompleteWidget,
    BuyerForm,
    MobileForm,
    MobileNumberForm,
    StuffForm,
)


# Create your views here.
def buyer_index(request):
    MobileFormSet = modelformset_factory(Mobile, form=MobileForm)
    MobileNumberFormSet = modelformset_factory(MobileNumber, form=MobileNumberForm)
    StuffFormSet = modelformset_factory(
        Stuff,
        form=StuffForm,
        widgets={
            "stuff_type": AutoCompleteWidget(
                data_endpoint=reverse_lazy("autocomplete-buyer-stuff")
            )
        },
    )

    if request.method == "POST":
        copy_POST = request.POST.copy()
        buyer_form = BuyerForm(copy_POST)
        mobiles_form = MobileFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="mobiles"
        )
        mobiles_numbers_form = MobileNumberFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="mobiles-numbers"
        )
        for key in copy_POST:
            if key.endswith("stuff_type"):
                name = copy_POST[key]
                stuff_type, created = StuffType.objects.get_or_create(name=name)
                copy_POST[key] = stuff_type.id

        stuff_form = StuffFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="stuff"
        )

        if (
            buyer_form.is_valid()
            and mobiles_form.is_valid()
            and mobiles_numbers_form.is_valid()
            and stuff_form.is_valid()
        ):
            buyer = buyer_form.save(commit=False)
            buyer.save()
            for mobile in mobiles_form.cleaned_data:
                if mobile:
                    mobile = Mobile(**mobile, buyer=buyer)
                    mobile.save()

            for mobile_number in mobiles_numbers_form.cleaned_data:
                if mobile_number:
                    mobile_number = MobileNumber(**mobile_number, buyer=buyer)
                    mobile_number.save()

            for stuff in stuff_form.cleaned_data:
                if stuff:
                    stuff = Stuff(**stuff, buyer=buyer)
                    stuff.save()

            return redirect(
                reverse_lazy("buyer"),
            )
        else:
            stuff_form = StuffFormSet(
                request.POST, queryset=Buyer.objects.none(), prefix="stuff"
            )
            print(buyer_form.errors)
            print(mobiles_form.errors)
            print(mobiles_numbers_form.errors)
            print(stuff_form.errors)
            render(
                request,
                template_name="buyer.html",
                context={
                    "buyer_form": buyer_form,
                    "mobiles_form": mobiles_form,
                    "mobiles_numbers_form": mobiles_numbers_form,
                    "stuff_form": stuff_form,
                },
            )
    else:
        buyer_form = BuyerForm()
        mobiles_form = MobileFormSet(queryset=Buyer.objects.none(), prefix="mobiles")
        mobiles_numbers_form = MobileNumberFormSet(
            queryset=Buyer.objects.none(), prefix="mobiles-numbers"
        )
        stuff_form = StuffFormSet(queryset=Buyer.objects.none(), prefix="stuff")

    return render(
        request,
        template_name="buyer.html",
        context={
            "buyer_form": buyer_form,
            "mobiles_form": mobiles_form,
            "mobiles_numbers_form": mobiles_numbers_form,
            "stuff_form": stuff_form,
        },
    )
