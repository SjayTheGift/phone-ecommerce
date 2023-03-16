const btn = document.getElementById('menu-btn');
const mobile_nav = document.querySelector('.mobile-nav');

function toggleNav(){
    btn.classList.toggle('open');
    mobile_nav.classList.toggle('nav-hidden');
    document.body.classList.toggle('no-scroll');
}

btn.addEventListener('click', toggleNav);

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


let cart = JSON.parse(getCookie('cart'));

if(cart == undefined){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}


let update_btn = document.getElementsByClassName('update-cart');
let remove_btn = document.getElementsByClassName('btn-remove');
let btn_product = document.getElementsByClassName('btn-product');




function update_Btn(btn){
    for(let i = 0; i < btn.length; i++){
        btn[i].addEventListener('click', ()=>{
            let productId = btn[i].getAttribute('data-product')
            let action = btn[i].getAttribute('data-add')
            if(user != 'AnonymousUser'){
                updateUserOrder(productId, action)
            }else{
                add_cookie_storage(productId, action)
            }
           
        })
    }
}

function delete_item(btn){
    for(let i = 0; i < btn.length; i++){
        btn[i].addEventListener('click', ()=>{
            let productId = btn[i].getAttribute('data-product')
            if(user != 'AnonymousUser'){
                deleteOrderItem(productId)
            }else{
                delete cart[productId] 
                document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
                location.reload()
            }
           
        })
    }
}



function add_cookie_storage(productId, action){
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }
    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}




update_Btn(update_btn)
update_Btn(btn_product)
delete_item(remove_btn)

function updateUserOrder(productId, action){
    console.log('sending data...')

    let url = '/update_item/'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}),
        
    })
    .then((res) =>{
        return res.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function deleteOrderItem(productId){
    console.log('delete data...')

    let url = '/delete_item/'

    fetch(url,{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId}),
        
    })
    .then((res) =>{
        return res.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

