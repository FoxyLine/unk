from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from buyer.models import (
    Buyer,
    InternetAccount,
    Mobile,
    MobileNumber,
    Stuff,
    StuffType,
    Clad,
    Bank,
    Crypto,
    OnlinePay,
)
from .forms import (
    AutoCompleteWidget,
    BuyerForm,
    MobileForm,
    MobileNumberForm,
    StuffForm,
    InternetAccountForm,
    CladForm,
    CryptoForm,
    BankForm,
    OnlinePayForm,
)

from .elastic import more_like_buyer_by_id


def create_buyer(request, buyer_id=None):
    StuffFormSet = modelformset_factory(
        Stuff,
        form=StuffForm,
        widgets={
            "stuff_type": AutoCompleteWidget(
                data_endpoint=reverse_lazy("autocomplete-buyer-stuff")
            )
        },
    )
    MobileFormSet = modelformset_factory(
        Mobile,
        form=MobileForm,
    )
    MobileNumberFormSet = modelformset_factory(MobileNumber, form=MobileNumberForm)

    CladsFormSet = modelformset_factory(Clad, form=CladForm)
    BankFormSet = modelformset_factory(Bank, form=BankForm, extra=1)
    OnlinePayFormSet = modelformset_factory(OnlinePay, form=OnlinePayForm, extra=1)
    CryptoFormSet = modelformset_factory(Crypto, form=CryptoForm, extra=1)
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
        clads_form = CladsFormSet(
            copy_POST, request.FILES, queryset=Buyer.objects.none(), prefix="clads"
        )
        bank_form = BankFormSet(copy_POST, queryset=Buyer.objects.none(), prefix="bank")
        online_pay_form = OnlinePayFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="online-pay"
        )
        crypto_form = CryptoFormSet(
            copy_POST, queryset=Buyer.objects.none(), prefix="crypto"
        )
        account = InternetAccountForm(copy_POST)

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

        if (
            buyer_form.is_valid()
            and mobiles_form.is_valid()
            and mobiles_numbers_form.is_valid()
            and stuff_form.is_valid()
            and clads_form.is_valid()
            and bank_form.is_valid()
            and online_pay_form.is_valid()
            and crypto_form.is_valid()
            and account.is_valid()
        ):
            buyer: Buyer = buyer_form.save(commit=False)
            buyer.save()
            print(account.cleaned_data)
            if any(account.cleaned_data.values()):
                internet_account = InternetAccount(**account.cleaned_data)
                internet_account.save()
                buyer.accounts.set([internet_account])
            print(clads_form.cleaned_data)

            formsets = [
                (Mobile, mobiles_form, buyer.mobiles),
                (MobileNumber, mobiles_numbers_form, buyer.mobile_numbers),
                (Stuff, stuff_form, buyer.stuffs),
                (Bank, bank_form, buyer.banks),
                (OnlinePay, online_pay_form, buyer.online_pays),
                (Crypto, crypto_form, buyer.cryptos),
                (Clad, clads_form, buyer.clads),
            ]

            for model_class, formset, related_manager in formsets:
                instances = []
                for form in formset.cleaned_data:
                    if not form:
                        continue
                    instance = model_class(**form)
                    if isinstance(form.get("id"), model_class):
                        instance.id = form["id"].id
                    if (
                        model_class == Clad
                        and form.get("photo") != ""
                        and form.get("photo") is not None
                    ):
                        instance.photo = form.get("photo")
                    elif model_class == Clad and instance.id:
                        instance.photo = Clad.objects.get(pk=instance.id).photo
                    instance.save()
                    instances.append(instance)
                if model_class == Clad:
                    buyer.clads.set(instances)
                else:
                    related_manager.set(instances)

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
                    "similar_buyers": similar_buyers,
                    "clads_form": clads_form,
                    "bank_form": bank_form,
                    "online_pay_form": online_pay_form,
                    "crypto_form": crypto_form,
                    "account": account,
                },
            )
    else:
        buyer_form = BuyerForm(instance=buyer_instance)
        if buyer_instance and buyer_instance.get_account():
            account = InternetAccountForm(
                data=model_to_dict(buyer_instance.get_account())
            )
        else:
            account = InternetAccountForm()

        if buyer_instance:
            mobiles_form = MobileFormSet(
                queryset=buyer_instance.mobiles.all(), prefix="mobiles"
            )
            mobiles_numbers_form = MobileNumberFormSet(
                queryset=buyer_instance.mobile_numbers.all(), prefix="mobiles-numbers"
            )
            stuff_form = StuffFormSet(
                queryset=buyer_instance.stuffs.all(), prefix="stuff"
            )
            clads_form = CladsFormSet(
                queryset=buyer_instance.clads.all(), prefix="clads"
            )
            bank_form = BankFormSet(queryset=buyer_instance.banks.all(), prefix="bank")
            online_pay_form = OnlinePayFormSet(
                queryset=buyer_instance.online_pays.all(), prefix="online-pay"
            )
            crypto_form = CryptoFormSet(
                queryset=buyer_instance.cryptos.all(), prefix="crypto"
            )
        else:
            mobiles_form = MobileFormSet(
                queryset=MobileNumber.objects.none(), prefix="mobiles"
            )
            mobiles_numbers_form = MobileNumberFormSet(
                queryset=MobileNumber.objects.none(), prefix="mobiles-numbers"
            )
            stuff_form = StuffFormSet(
                queryset=MobileNumber.objects.none(), prefix="stuff"
            )
            clads_form = CladsFormSet(
                queryset=MobileNumber.objects.none(), prefix="clads"
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
        template_name="card-buyer.html",
        context={
            "buyer": buyer_instance,
            "buyer_form": buyer_form,
            "mobiles_form": mobiles_form,
            "mobiles_numbers_form": mobiles_numbers_form,
            "stuff_form": stuff_form,
            "similar_buyers": similar_buyers,
            "clads_form": clads_form,
            "bank_form": bank_form,
            "online_pay_form": online_pay_form,
            "crypto_form": crypto_form,
            "account": account,
        },
    )


def buyer(request):
    return render(
        request, template_name="buyer.html", context={"buyers": Buyer.objects.all()}
    )
