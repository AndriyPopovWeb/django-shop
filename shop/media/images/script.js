// fetch('/product/get/price/1').then((response) => {return response.json()}).then((data) => {return data});
console.log("1234354566443")
count = 0
for (var i = 0; i < Object.values(JSON.parse(localStorage.getItem('cart'))).length; i++) {
var key = Object.keys(JSON.parse(localStorage.getItem('cart')))[i];
var obj = document.getElementById("cartinner");
// function fetchurl(url) {
//     result = ""
//     var ret = fetch(url).then((response) => {return response.json()}).then((data) => {
//         return data}); 
//     console.log(ret)
//     return ret;
//     };

function givemeadataplease(dat) {

    sav = dat

}
function fetchurl(url) {
res = fetch(url).then(response => {
    if (!response.ok) {
      console.log('Something went wrong... Status: ' + response.status)
    } else {
      return response.json()
    }
  })
  .then(data => {return data})
    res.then(data => {givemeadataplease(data)});
    return sav}
console.log(fetchurl("/product/get/price/1"))
obj.innerHTML += '<div class="card-header"> Товар '+fetch('/product/get/price/'+key).then((response) => {return response.json()}).then((data) => {return data.text})+' грн &#8372 </div><div class="card text-center"><div class="card-body"><div><img src=' + fetch('/product/get/image/'+key).then((response) => {return response.json()}).then((data) => {return data})+'width="200" height="200" alt="{{ product.name }}"><h3>{{ product.name }}</h3>{% endif %}{% endfor %}</div><div style="padding-bottom: 20px"><h5 class="card-title">' + fetch('/product/get/name/'+key).then((response) => {return response.json()}).then((data) => {return data})+ '</h5></div><a href="/product/'+key+'" class="btn btn-primary">Перейти до товару</a></div><div style="padding-bottom: 20px"><div class="btn-group" role="group" aria-label="4 години мого часу"><button type="button" class="btn btn-secondary btn-success">Додати товар</button><div id="centerbtn"><button type="button" class="btn btn-secondary " disabled></button></div><button type="button" class="btn btn-secondary btn-danger">Забрати товар</button></div><button type="button" class="btn btn-danger">Видалити</button></div><div class="card-footer text-muted">я це робив 4 години</div></div>';}