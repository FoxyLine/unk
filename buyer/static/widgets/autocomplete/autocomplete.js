let input_with_autocomplete = {}

function replace_last_item(value, separator, targer) {
  const parts = value.split(separator);
  const lastPart = parts.pop();
  parts.push(targer);
  const newStr = parts.join(separator);
  return newStr

}

const Autocomplete = () => {
    selector = '[autocomplete-endpoint*="/"]'
    let inputs = document.querySelectorAll(selector);
    function ciSearch(what = '', where = '') {
      return where.toUpperCase().search(what.toUpperCase());
    }

    inputs.forEach(input => {
      if (input.id in input_with_autocomplete) {
        return
      } else {
        input_with_autocomplete[input.id] = true
      }



      input.setAttribute("has-autocomplete", "true")
      let dataEndpoint = input.getAttribute("autocomplete-endpoint")
      let separator = input.getAttribute("separator")
      console.log(dataEndpoint)
      input.classList.add('autocomplete-input');
      let wrap = document.createElement('div');
      wrap.className = 'autocomplete-wrap';
      input.parentNode.insertBefore(wrap, input);
      wrap.appendChild(input);

      let list = document.createElement('div');
      list.className = 'autocomplete-list';
      wrap.appendChild(list);

      let matches = [];
      let listItems = [];
      let focusedItem = -1;

      function setActive(active = true) {
        if(active)
          wrap.classList.add('active');
        else
          wrap.classList.remove('active');
      }

      function focusItem(index) {
        if(!listItems.length) return false;
        if(index > listItems.length - 1) return focusItem(0);
        if(index < 0) return focusItem(listItems.length - 1);
        focusedItem = index;
        unfocusAllItems();
        listItems[focusedItem].classList.add('focused');
      }
      function unfocusAllItems() {
        listItems.forEach(item => {
          item.classList.remove('focused');
        });
      }
      function selectItem(index) {
        if(!listItems[index]) return false;
        input.value = replace_last_item(input.value, separator, listItems[index].innerText)
        setActive(false);
      }
      let oninput_callback = async () => {

        let value = input.value;
        if (separator){
          const parts = value.split(separator);
          const lastPart = parts[parts.length - 1];
          value = lastPart;
        }
        searchValue = value.trim()

        if(!searchValue) return setActive(false);


        list.innerHTML = '';
        listItems = [];
        let response = await fetch(dataEndpoint+"?q="+searchValue);
        data = await response.json()
        data.forEach((dataItem, index) => {
          let search = ciSearch(searchValue, dataItem);
          if(search === -1) return false;
          matches.push(index);

          let parts = [
            dataItem.substr(0, search),
            dataItem.substr(search, searchValue.length),
            dataItem.substr(search + searchValue.length, dataItem.length - search - searchValue.length)
          ];

          let item = document.createElement('div');
          item.className = 'autocomplete-item';
          item.innerHTML = parts[0] + '<strong>' + parts[1] + '</strong>' + parts[2];
          list.appendChild(item);
          listItems.push(item);

          item.addEventListener('click', function() {
            selectItem(listItems.indexOf(item));
          });

        });

        if(listItems.length > 0) {
          focusItem(0);
          setActive(true);
        }
        else setActive(false);

      }



      input.addEventListener('input', oninput_callback)

      input.addEventListener('keydown', e => {

        let keyCode = e.keyCode;

        if(keyCode === 40) { // arrow down
          e.preventDefault();
          focusedItem++;
          focusItem(focusedItem);
        } else if(keyCode === 38) { //arrow up
          e.preventDefault();
          if(focusedItem > 0) focusedItem--;
          focusItem(focusedItem);
        } else if(keyCode === 27) { // escape
          setActive(false);
        } else if(keyCode === 13) { // enter
          selectItem(focusedItem);
        }

      });

      document.body.addEventListener('click', function(e) {
        if(!wrap.contains(e.target)) setActive(false);
      });

    });

  }