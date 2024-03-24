const close_buttons = document.getElementsByClassName('close-button');

for (i=0; i < close_buttons.length; i++){
    close_buttons[i].addEventListener('click', function() {
        var parent = this.parentNode;

        parent.style.animation = "fadingOut 0.4s linear forwards";


        setTimeout(()=> {
            parent.style.display = 'none';
        }, 400);
    });
}