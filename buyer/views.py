from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from buyer.models import Buyer, BuyerAccount, Mobile, MobileNumber, Stuff, StuffType
from .forms import (
    AutoCompleteWidget,
    BuyerForm,
    MobileForm,
    MobileNumberForm,
    StuffForm,
    MessengerForm,
    SiteForm,
    DarkWebForm,
)

from .elastic import more_like_buyer_by_id


# from django.contrib.contenttypes.models import ContentType
# ct = ContentType.objects.get_for_id(content_type)
# obj = ct.get_object_for_this_type(pk=object_id)

# Create your views here.
def create_buyer(request, buyer_id=None):
    MobileFormSet = modelformset_factory(
        Mobile,
        form=MobileForm,
    )
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
    buyer_instance = None
    similar_buyers = None
    if buyer_id:
        buyer_instance = get_object_or_404(Buyer, id=buyer_id)
        similar_buyers = more_like_buyer_by_id(buyer_instance.id, limit=5)

    if request.method == "POST":
        copy_POST = request.POST.copy()
        buyer_form = BuyerForm(copy_POST, instance=buyer_instance)
        mobiles_form = MobileFormSet(
            copy_POST,
            queryset=Buyer.objects.none(),
            prefix="mobiles",
        )
        mobiles_numbers_form = MobileNumberFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="mobiles-numbers"
        )
        for key in copy_POST:
            if key.endswith("stuff_type"):
                name = copy_POST[key]
                stuff_type, created = StuffType.objects.get_or_create(name=name)
                copy_POST[key] = stuff_type.pk
        stuff_form = StuffFormSet(
            copy_POST,
            queryset=Stuff.objects.filter(buyer=buyer_instance),
            prefix="stuff",
        )
        messenger_form = MessengerForm(copy_POST, prefix="messenger")
        site_form = SiteForm(copy_POST, prefix="site")
        dark_web_form = DarkWebForm(copy_POST, prefix="dark_web")

        shop_type_form = None
        if buyer_form.data["shop_type"] == Buyer.MESSENGER:
            shop_type_form = messenger_form
        elif buyer_form.data["shop_type"] == Buyer.WEB_SITE:
            shop_type_form = site_form
        elif buyer_form.data["shop_type"] == Buyer.DARK_NET:
            shop_type_form = dark_web_form

        if (
            buyer_form.is_valid()
            and mobiles_form.is_valid()
            and mobiles_numbers_form.is_valid()
            and stuff_form.is_valid()
            and (shop_type_form is None or shop_type_form.is_valid())
        ):
            buyer: Buyer = buyer_form.save(commit=False)
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
            if shop_type_form:
                buyer_account = BuyerAccount(**shop_type_form.cleaned_data, buyer=buyer)
                buyer_account.save()

            if buyer_id:
                return redirect(
                    reverse_lazy("update-buyer", kwargs={"buyer_id": buyer_id})
                )
            else:
                buyer.save()
                return redirect(
                    reverse_lazy("update-buyer", kwargs={"buyer_id": buyer.id})
                )
        else:
            stuff_form = StuffFormSet(
                copy_POST, queryset=Buyer.objects.none(), prefix="stuff"
            )
            render(
                request,
                template_name="card-buyer.html",
                context={
                    "buyer": buyer_instance,
                    "buyer_form": buyer_form,
                    "mobiles_form": mobiles_form,
                    "mobiles_numbers_form": mobiles_numbers_form,
                    "stuff_form": stuff_form,
                    "messanger_form": messenger_form,
                    "site_form": site_form,
                    "dark_web_form": dark_web_form,
                    "similar_buyers": similar_buyers,
                },
            )
    else:
        buyer_form = BuyerForm(instance=buyer_instance)
        messenger_form = MessengerForm(prefix="messenger")
        site_form = SiteForm(prefix="site")
        dark_web_form = DarkWebForm(prefix="dark_web")
        mobiles_form = MobileFormSet(queryset=Buyer.objects.none(), prefix="mobiles")
        mobiles_numbers_form = MobileNumberFormSet(
            queryset=Mobile.objects.filter(buyer=buyer_instance),
            prefix="mobiles-numbers",
        )
        stuff_form = StuffFormSet(
            queryset=Stuff.objects.filter(buyer=buyer_instance), prefix="stuff"
        )
    return render(
        request,
        template_name="card-buyer.html",
        context={
            "buyer": buyer_instance,
            "buyer_form": buyer_form,
            "mobiles_form": mobiles_form,
            "mobiles_numbers_form": mobiles_numbers_form,
            "stuff_form": stuff_form,
            "messanger_form": messenger_form,
            "site_form": site_form,
            "dark_web_form": dark_web_form,
            "similar_buyers": similar_buyers,
        },
    )


def buyer(request):
    return render(
        request, template_name="buyer.html", context={"buyers": Buyer.objects.all()}
    )
