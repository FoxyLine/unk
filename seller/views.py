from django.shortcuts import render
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from .forms import SellerForm

from .models import Seller, SellerStuff
from buyer.models import (
    Mobile,
    MobileNumber,
    Stuff,
    StuffType,
    Buyer,
    InternetAccount,
    Bank,
    Crypto,
    OnlinePay,
    Clad,
)
from buyer.forms import (
    MobileForm,
    MobileNumberForm,
    StuffForm,
    AutoCompleteWidget,
    InternetAccountForm,
    BankForm,
    OnlinePay,
    CryptoForm,
    OnlinePayForm,
    CladForm,
)
from .forms import MasterCladForm


def seller_index(request):
    return render(request, template_name="seller.html")


def create_seller(request, seller_id=None):
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
    InternetAccountFormSet = modelformset_factory(
        InternetAccount, form=InternetAccountForm
    )
    BankFormSet = modelformset_factory(Bank, form=BankForm, extra=1)
    OnlinePayFormSet = modelformset_factory(OnlinePay, form=OnlinePayForm, extra=1)
    CryptoFormSet = modelformset_factory(Crypto, form=CryptoForm, extra=1)

    CladsFormSet = modelformset_factory(Clad, form=CladForm)
    MasterCladsFormSet = modelformset_factory(Clad, form=MasterCladForm)

    seller_instance = None
    similar_buyers = None
    if seller_id:
        seller_instance = get_object_or_404(Seller, id=seller_id)
        # similar_buyers = more_like_buyer_by_id(buyer_instance.id, limit=5)

    if request.method == "POST":
        copy_POST = request.POST.copy()
        seller_form = SellerForm(copy_POST, instance=seller_instance)
        mobiles_form = MobileFormSet(
            copy_POST,
            queryset=Seller.objects.none(),
            prefix="mobiles",
        )
        mobiles_numbers_form = MobileNumberFormSet(
            copy_POST, queryset=Seller.objects.none(), prefix="mobiles-numbers"
        )
        internet_account_form = InternetAccountFormSet(
            copy_POST, queryset=Seller.objects.none(), prefix="seller-inernet-account"
        )
        bank_form = BankFormSet(
            copy_POST, queryset=Seller.objects.none(), prefix="bank"
        )
        online_pay_form = OnlinePayFormSet(
            copy_POST, queryset=Seller.objects.none(), prefix="online-pay"
        )
        crypto_form = CryptoFormSet(
            copy_POST, queryset=Seller.objects.none(), prefix="crypto"
        )
        clads_form = CladsFormSet(
            copy_POST, request.FILES, queryset=Buyer.objects.none(), prefix="clads"
        )
        master_clads_form = MasterCladsFormSet(
            copy_POST,
            request.FILES,
            queryset=Buyer.objects.none(),
            prefix="master-clads",
        )

        for key in copy_POST:
            if key.endswith("stuff_type"):
                name = copy_POST[key]
                stuff_type, created = StuffType.objects.get_or_create(name=name)
                copy_POST[key] = stuff_type.pk

        stuff_form = StuffFormSet(
            copy_POST,
            queryset=SellerStuff.objects.filter(seller=seller_instance),
            prefix="stuff",
        )

        if (
            seller_form.is_valid()
            and mobiles_form.is_valid()
            and mobiles_numbers_form.is_valid()
            and stuff_form.is_valid()
            and internet_account_form.is_valid()
            and clads_form.is_valid()
            and bank_form.is_valid()
            and online_pay_form.is_valid()
            and crypto_form.is_valid()
            and master_clads_form.is_valid()
        ):
            seller: Seller = seller_form.save(commit=False)
            seller.save()

            formsets = [
                (Mobile, mobiles_form, seller.mobiles),
                (MobileNumber, mobiles_numbers_form, seller.mobile_numbers),
                (Stuff, stuff_form, seller.stuffs),
                (InternetAccount, internet_account_form, seller.interner_accounts),
                (Bank, bank_form, seller.banks),
                (OnlinePay, online_pay_form, seller.online_pays),
                (Crypto, crypto_form, seller.cryptos),
                (Clad, clads_form, seller.clads),
                (Clad, master_clads_form, seller.master_clads),
            ]

            for model_class, formset, related_manager in formsets:
                instances = []
                for form in formset.cleaned_data:
                    if not form:
                        continue
                    instance = model_class(**form)
                    if isinstance(form.get("id"), model_class):
                        instance.id = form["id"].id
                    if model_class == Clad and form.get("photo") != "":
                        instance.photo = form.get("photo")
                    if formset == master_clads_form:
                        instance.type_clad = Clad.MASTER_CLAD
                    instance.save()
                    instances.append(instance)
                related_manager.set(instances)

            if seller_id:
                return redirect(
                    reverse_lazy("update-seller", kwargs={"seller_id": seller_id})
                )
            else:
                seller.save()
                return redirect(
                    reverse_lazy("update-seller", kwargs={"seller_id": seller.id})
                )
        else:
            seller_form = SellerForm()

            # stuff_form = StuffFormSet(copy_POST, queryset=Buyer.objects.none(), prefix="stuff")
            # print(stuff_form.errors)
            render(
                request,
                template_name="card-seller.html",
                context={
                    "seller": seller_instance,
                    "seller_form": seller_form,
                    "mobiles_form": mobiles_form,
                    "mobiles_numbers_form": mobiles_numbers_form,
                    "stuff_form": stuff_form,
                    "internet_account_form": internet_account_form,
                    "bank_form": bank_form,
                    "online_pay_form": online_pay_form,
                    "crypto_form": crypto_form,
                    "clads_form": clads_form,
                    "master_clads_form": master_clads_form,
                    # "messanger_form": messenger_form,
                    # "site_form": site_form,
                    # "dark_web_form": dark_web_form,
                    # "similar_buyers": similar_buyers,
                },
            )
    else:
        seller_form = SellerForm(instance=seller_instance)
        if seller_instance:
            mobiles_form = MobileFormSet(
                queryset=seller_instance.mobiles.all(), prefix="mobiles"
            )
            mobiles_numbers_form = MobileNumberFormSet(
                queryset=seller_instance.mobile_numbers.all(), prefix="mobiles-numbers"
            )
            stuff_form = StuffFormSet(
                queryset=seller_instance.stuffs.all(), prefix="stuff"
            )
            internet_account_form = InternetAccountFormSet(
                queryset=seller_instance.interner_accounts.all(),
                prefix="seller-inernet-account",
            )
            clads_form = CladsFormSet(
                queryset=seller_instance.clads.all(), prefix="clads"
            )
            master_clads_form = CladsFormSet(
                queryset=seller_instance.master_clads.all(), prefix="master-clads"
            )
            bank_form = BankFormSet(queryset=seller_instance.banks.all(), prefix="bank")
            online_pay_form = OnlinePayFormSet(
                queryset=seller_instance.online_pays.all(), prefix="online-pay"
            )
            crypto_form = CryptoFormSet(
                queryset=seller_instance.cryptos.all(), prefix="crypto"
            )

        else:
            mobiles_form = MobileFormSet(
                queryset=Seller.objects.none(), prefix="mobiles"
            )
            mobiles_numbers_form = MobileNumberFormSet(
                queryset=MobileNumber.objects.none(), prefix="mobiles-numbers"
            )
            stuff_form = StuffFormSet(
                queryset=MobileNumber.objects.none(), prefix="stuff"
            )
            internet_account_form = InternetAccountFormSet(
                queryset=MobileNumber.objects.none(), prefix="seller-inernet-account"
            )
            clads_form = CladsFormSet(
                queryset=MobileNumber.objects.none(), prefix="clads"
            )
            master_clads_form = CladsFormSet(
                queryset=MobileNumber.objects.none(), prefix="master-clads"
            )
            bank_form = BankFormSet(queryset=MobileNumber.objects.none(), prefix="bank")
            online_pay_form = OnlinePayFormSet(
                queryset=MobileNumber.objects.none(), prefix="online-pay"
            )
            crypto_form = CryptoFormSet(
                queryset=MobileNumber.objects.none(), prefix="crypto"
            )

    return render(
        request,
        template_name="card-seller.html",
        context={
            "seller": seller_instance,
            "seller_form": seller_form,
            "mobiles_form": mobiles_form,
            "mobiles_numbers_form": mobiles_numbers_form,
            "stuff_form": stuff_form,
            "internet_account_form": internet_account_form,
            "bank_form": bank_form,
            "online_pay_form": online_pay_form,
            "crypto_form": crypto_form,
            "clads_form": clads_form,
            "master_clads_form": master_clads_form,
            # "messanger_form": messenger_form,
            # "site_form": site_form,
            # "dark_web_form": dark_web_form,
            # "similar_buyers": similar_buyers,
        },
    )
