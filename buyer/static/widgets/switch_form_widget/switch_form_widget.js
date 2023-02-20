function switchForm(event, group_switch, ids_forms) {
    var selectBox = event.currentTarget;
    let forms = []
    forms = document.querySelectorAll(`[switch='${group_switch}']`);
    console.log(forms);
    forms.forEach(form => {
        if (form.classList.contains(ids_forms.at( selectBox.selectedIndex-1))){
            form.style.display = "unset"
        } else {
            form.style.display = "none"
        }
    });
   }


   document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[switcher]").forEach((e)=> {
        let event = {currentTarget: e} // Мок для event
        e.onchange(event);

   })})