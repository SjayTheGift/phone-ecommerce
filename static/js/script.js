const btn = document.getElementById('menu-btn');
const mobile_nav = document.querySelector('.mobile-nav');

function toggleNav(){
    btn.classList.toggle('open');
    mobile_nav.classList.toggle('nav-hidden');
    document.body.classList.toggle('no-scroll');
}

btn.addEventListener('click', toggleNav);
