/*function displayDate(e) {
  e.getElementById('counter').innerHTML = Date();
}
document.querySelector(".btn.btn-danger").addEventListener("click", displayDate(this));
*/
// DONE add Menu item to Order
document.addEventListener('click', function(event) {
    if (!event.target.matches('.btn-buy')) return;
    let element = event.target;
    // DONE make basket visible on 'btn-buy' click
    Basket = document.getElementsByClassName('OrderMap')[0];
    Basket.style.visibility ='visible';
    let myNode = element.parentNode.parentNode;
    let mySpan = myNode.getElementsByTagName("SPAN");
    let pizza = mySpan[1].innerText;
    let price = NumPrice(mySpan[2].innerText);
    // DONE create helper function to determine if ware already in list
    result = helper(pizza,price);
}, false);

let mytitle = document.getElementsByTagName('title')[0];
if (mytitle.innerText !== 'Order') {
  // Event listener for close button
  document.addEventListener('click', function(event) {
    if (event.target.matches(".close-btn")) {
      // Hide div
      closeOrder = document.getElementsByClassName('OrderMap')[0];
      console.log("close button clicked");
      closeOrder.style.visibility ='hidden';
    }
    if (!event.target.matches('.OrderView')) return;
    console.log("Order button clicked");
    OrderMap();
  });
}

function OrderMap() {
  let basket = document.getElementsByClassName('OrderMap')[0];
  if (basket.style.visibility == 'hidden') {
    basket.style.visibility = 'visible';
    updateCartTotal();
  }
}

function helper(pizzaName,price) {
  // DONE select pizza in cookies with name=name
  let myOrder = document.cookie.replace(/(?:(?:^|.*;\s*)Order\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  if (myOrder.length === 0) {
    // DONE if Order do not exist,
    // Create Order Object
    myOrder = {
      "Pizza": {
        [pizzaName]: [
          {"Price":price},
          {"Amount":1}]
      }
    };
    // DONE save it in Cookie
    let myCookie = "Order=" + encodeURIComponent(JSON.stringify(myOrder)) +";"+ exday(1) + ";" + "path=/";
    document.cookie = myCookie;
    // DONE add <tr> to <tbody>
    let amount = 1;
    let placeForRow = document.getElementsByClassName('orderBasket')[0];
    let myRow = document.createElement('tr');
    let currency = currencyForPage();
    let buttonRemove = buttonLang();
    let myRowContent = `
      <td>${pizzaName}</td>
      <td class="price">${price} ${currency}</td>
      <td>
          <button class="btn btn-secondary order-btn btn-minus">-</button>
          <span class="amount">x${amount}</span>
          <button class="btn btn-secondary order-btn btn-plus">+</button>
      </td>
      <td>
          <button class="btn btn-danger order-btn remove-btn">${buttonRemove}</button>
      </td>`;
    myRow.innerHTML = myRowContent;
    placeForRow.append(myRow);
    updateCartTotal();
    return -1;
  }else {
    // DONE Search for pizzaName in Object
    let retrOrder = JSON.parse(decodeURIComponent(myOrder));
    let list_ = Object.keys(retrOrder.Pizza);
    let i = 0;
    while(list_[i]) {
      if (pizzaName === list_[i]) {
        // DONE if pizzaName in cookies, increase amount by 1
        retrOrder.Pizza[list_[i]][1].Amount += 1;
        // DONE Save changes to Cookie
        let myCookie = "Order=" + encodeURIComponent(JSON.stringify(retrOrder)) +";"+ exday(1) + ";" + "path=/";
        document.cookie = myCookie;
        let trList = document.getElementsByTagName('TR');
        for (let x = 0; x < trList.length; x++) {
          // DONE search for <tr> with with this pizza
          if (pizzaName ===trList[x].firstElementChild.innerText) {
            console.log("bingo!");
            // DONE update amount
            let amountTag = trList[x].getElementsByClassName('amount')[0];
            let amount = amountTag.innerText.slice(1,);
            amount++;
            amountTag.innerText ='x' + amount;
            // DONE update total value
          }
          updateCartTotal();
        }
        return 0;
      }
      i++;
    }
    // DONE if pizzaName not in cookies, add new pizza to object
    retrOrder.Pizza[pizzaName] = [{"Price":price},{"Amount":1}];
    // DONE Save changes to Cookie
    let myCookie = "Order=" + encodeURIComponent(JSON.stringify(retrOrder)) +";"+ exday(1) + ";" + "path=/";
    document.cookie = myCookie;
    // DONE add <tr> to <tbody>
    let amount = 1;
    let placeForRow = document.getElementsByClassName('orderBasket')[0];
    let myRow = document.createElement('tr');
    let currency = currencyForPage();
    let buttonRemove = buttonLang();
    let myRowContent = `
      <td>${pizzaName}</td>
      <td class="price">${price} ${currency}</td>
      <td>
          <button class="btn btn-secondary order-btn btn-minus">-</button>
          <span class="amount">x${amount}</span>
          <button class="btn btn-secondary order-btn btn-plus">+</button>
      </td>
      <td>
          <button class="btn btn-danger order-btn remove-btn">${buttonRemove}</button>
      </td>`;
    myRow.innerHTML = myRowContent;
    placeForRow.append(myRow);
    updateCartTotal();
    return 1;
  }
}



function fillBasket() {
  // This function Fill's basket if cookie Order isn't empty
  let escapedOrder = document.cookie.replace(/(?:(?:^|.*;\s*)Order\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  if (escapedOrder.length > 0) {
    // DONE escaped order to object
    let objectOrder = JSON.parse(decodeURIComponent(escapedOrder));
    // DONE Find the beginning of table with querySelector or byClassName
    // select only first item
    let TableStart = document.getElementsByClassName('orderBasket')[0];
    // DONE Get list of Object Keys
    let listKeys = Object.keys(objectOrder.Pizza);
    for (let i = 0; i < listKeys.length; i++) {
      let Name = listKeys[i];// -> Name
      let Price = objectOrder.Pizza[listKeys[i]][0].Price;// -> Price
      let Amount = objectOrder.Pizza[listKeys[i]][1].Amount;// -> Amount
      // DONE if page language uk  curency = "грн" else curency = "UAH";
      let currency = currencyForPage();
      let buttonRemove = buttonLang();
      // DONE Create <tr> element
      let cartRow = document.createElement('tr');
      // DONE Create row content
      let cartRowContents = `
        <td>${Name}</td>
        <td class="price">${Price} ${currency}</td>
        <td>
            <button class="btn btn-secondary order-btn btn-minus">-</button>
            <span class="amount">x${Amount}</span>
            <button class="btn btn-secondary order-btn btn-plus">+</button>
        </td>
        <td>
            <button class="btn btn-danger order-btn remove-btn">${buttonRemove}</button>
        </td>`;
      cartRow.innerHTML = cartRowContents;
      TableStart.append(cartRow);
    }
    console.log("call updateCartTotal();");
    updateCartTotal();
  }
}


document.addEventListener("DOMContentLoaded", function(event){
   // DONE This function fills basket if .orderBasket true
  if (!! document.querySelector(".orderBasket")) {
    fillBasket();
  }
  // DONE This function fills table order if .orderList true
  if (!!document.querySelector(".orderList")) {
    // DONE on page load isert list of order to page
    let escapedOrder = document.cookie.replace(/(?:(?:^|.*;\s*)Order\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    if (escapedOrder.length > 0) {
      // DONE escaped order to object
      let objectOrder = JSON.parse(decodeURIComponent(escapedOrder));
      // DONE Find the beginning of table with querySelector or byClassName
      // select only first item
      let TableStart = document.getElementsByClassName('orderList')[0];

      // DONE Get list of Object Keys
      let listKeys = Object.keys(objectOrder.Pizza);
      for (let i = 0; i < listKeys.length; i++) {
        let Name = listKeys[i];// -> Name
        let Price = objectOrder.Pizza[listKeys[i]][0].Price;// -> Price
        let Amount = objectOrder.Pizza[listKeys[i]][1].Amount;// -> Amount
        // DONE if page language uk  curency = "грн" else curency = "UAH";
        let currency = currencyForPage();
        let buttonRemove = buttonLang();
        // DONE Create <tr> element
        let cartRow = document.createElement('tr');
        // DONE Create row content
        let cartRowContents = `
          <td>${Name}</td>
          <td class="price">${Price} ${currency}</td>
          <td>
              <button class="btn btn-secondary order-btn btn-minus">-</button>
              <span class="amount">x${Amount}</span>
              <button class="btn btn-secondary order-btn btn-plus">+</button>
          </td>
          <td>
              <button class="btn btn-danger order-btn remove-btn">${buttonRemove}</button>
          </td>`;
        cartRow.innerHTML = cartRowContents;
        TableStart.append(cartRow);
      }
      updateCartTotal();
    }
    // DONE disable address field on toggle
    document.getElementById("customSwitch1").addEventListener("click", function(event) {
      function lol() {
        address_row.disabled = false;
        address_row.required = false;
        document.getElementById("customSwitch1").value ="off";
      }
      function kek() {
        address_row.disabled = true;
        address_row.required = true;
        address_row.value = "";
        document.getElementById('invalidInput').style = "display: none;";
        document.getElementById("customSwitch1").value ="on";
      }
      let address_row = document.getElementById('customerAddress');
      address_row.disabled ? lol(): kek();
      console.log(document.getElementById("customSwitch1").value);
    });
    // DONE prevent user from submit if address field is empty and green.
    document.getElementById("our-button").addEventListener("click",function(event) {
      let Address = document.getElementById('customerAddress');
      if (document.getElementById("customSwitch1").value == "off") {
        if (Address.value == "") {
          document.getElementById('invalidInput').style = "display: flex";
          event.preventDefault();
          //return false;
        }
      }
    }, false);
  }
});

// EventListener for Order page
if (document.getElementsByClassName("orderList")[0] !== undefined){
  document.getElementsByClassName("orderList")[0].addEventListener("click", function(event) {
    if (event.target && event.target.nodeName == "BUTTON") {
      var classes = event.target.className.split(" ");
      if (classes) {
        for(var x = 0; x < classes.length; x++) {
          if(classes[x] === "btn-plus") {
            let amountTag = event.target.previousElementSibling;
            let amount = amountTag.innerText.slice(1,);
            amount++;
            amountTag.innerText ='x' + amount;
            let myRow = event.target.parentElement.parentElement;
            let MealName = myRow.firstElementChild.innerText;
            // DONE update cookie amount
            EditCookie("increase", MealName);
            updateCartTotal();
          }
          else if(classes[x] === "btn-minus") {
            let amountTag = event.target.nextElementSibling;
            let amount = amountTag.innerText.slice(1,);
            if (amount > 1) {
              amount--;
              amountTag.innerText = 'x' + amount;
              let myRow = event.target.parentElement.parentElement;
              let MealName = myRow.firstElementChild.innerText;
              // DONE update cookie amount
              EditCookie("decrease", MealName);
              updateCartTotal();
            }
          }
          else if(classes[x] === "remove-btn") {
            console.log(event.target);
            let myRow = event.target.parentElement.parentElement;
            let MealName = myRow.firstElementChild.innerText;
            EditCookie("remove", MealName);
            myRow.remove();
            updateCartTotal();
          }
        }
      }
    }
  });
}

// EventListener for basket
document.getElementById("myBasket").addEventListener("click", function(e) {
  //e.target was the clicked element
  if (e.target && e.target.nodeName == "BUTTON") {
    // Get the CSS classes
    var classes = e.target.className.split(" ");
    // search for CSS class!
    if (classes) {
      // For every CSS class the element has...
      for(var x = 0; x < classes.length; x++) {
        // if it has the css class we want...
        if(classes[x] === "btn-plus") {
          let amountTag = e.target.previousElementSibling;
          let amount = amountTag.innerText.slice(1,);
          amount++;
          amountTag.innerText ='x' + amount;
          let myRow = e.target.parentElement.parentElement;
          let MealName = myRow.firstElementChild.innerText;
          // DONE update cookie amount
          EditCookie("increase", MealName);
          updateCartTotal();
        }
        else if(classes[x] === "btn-minus") {
          let amountTag = e.target.nextElementSibling;
          let amount = amountTag.innerText.slice(1,);
          if (amount > 1) {
            amount--;
            amountTag.innerText = 'x' + amount;
            let myRow = e.target.parentElement.parentElement;
            let MealName = myRow.firstElementChild.innerText;
            // DONE update cookie amount
            EditCookie("decrease", MealName);
            updateCartTotal();
          }
        }
        else if(classes[x] === "remove-btn") {
          console.log(e.target);
          let myRow = e.target.parentElement.parentElement;
          let MealName = myRow.firstElementChild.innerText;
          EditCookie("remove", MealName);
          myRow.remove();
          updateCartTotal();
        }
      }
    }
  }
});

function EditCookie(operation,MealName) {
  // DONE create single function
  // DONE To edit amount, add new meals to order, remove meals from order
  // operation types: decrease, increase, remove
  let escapedOrder = document.cookie.replace(/(?:(?:^|.*;\s*)Order\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  if (escapedOrder.length > 0) {
    let objectOrder = JSON.parse(decodeURIComponent(escapedOrder));
    switch(operation) {
      case "increase":
        console.log("increase");
        objectOrder.Pizza[MealName][1].Amount++;
        break;

      case "decrease":
        console.log("decrease");
        objectOrder.Pizza[MealName][1].Amount--;
        break;

      case "remove":
        console.log("remove");
        delete objectOrder.Pizza[MealName];
        break;

    }
    let myCookie = "Order=" + encodeURIComponent(JSON.stringify(objectOrder)) +";"+ exday(1) + ";" + "path=/";
    document.cookie = myCookie;
  }
}

// DONE Create function to calculate TOTAL price
function updateCartTotal() {
  let TotalPrice = 0;
  let TotalAmount = 0;
  let rowPrice = 0;
  let escapedOrder = document.cookie.replace(/(?:(?:^|.*;\s*)Order\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  if (escapedOrder.length > 0) {
    let objectOrder = JSON.parse(decodeURIComponent(escapedOrder));
    let listKeys = Object.keys(objectOrder.Pizza);
    for (let i = 0; i < listKeys.length; i++) {
      let Price = objectOrder.Pizza[listKeys[i]][0].Price;// -> Price
      let Amount = objectOrder.Pizza[listKeys[i]][1].Amount;// -> Amount
      rowPrice = Price * Amount;
      TotalPrice = TotalPrice + rowPrice;
      TotalAmount = TotalAmount + Amount;
    }
  }
  let currency = currencyForPage();
  document.getElementById('total-money').innerText = TotalPrice + " " + currency;
  document.getElementById('total-amount').innerText = TotalAmount;
  document.getElementById('Total').innerText = TotalPrice;
  if (document.getElementById('order-Total') !== null) {
    document.getElementById('order-Total').innerText = TotalPrice;
  }
}

// function to check display UAH or грн currency
function currencyForPage() {
  // DONE if page language uk  curency = "грн" else curency = "UAH";
  let currency = "UAH";
  if (document.getElementsByTagName('HTML')[0].lang !== "en") {
    currency = "грн";
  }
  return currency;
}

function buttonLang() {
  // this function translates single red button Remove
  let buttonName = "Remove";
  if (document.getElementsByTagName('HTML')[0].lang !== "en") {
    buttonName = "Вилучити";
  }
  return buttonName;
}

// define how much days cookies will exist
function exday(exdays) {
  let d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  return expires;
}
// function splits price and currency
function NumPrice(str) {
  let res = str.split(' ');
  return Number(res[0]);
}
