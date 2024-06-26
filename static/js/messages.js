const closeButtons = document.getElementsByClassName('close-button');

for (i=0; i < closeButtons.length; i++){
    closeButtons[i].addEventListener('click', function() {
        var parent = this.parentNode;

        parent.style.animation = "fadingOut 0.4s linear forwards";


        setTimeout(()=> {
            parent.style.display = 'none';
        }, 400);
    });
}

function showFlex(elementId) {
    let obj = document.getElementById(elementId);
    
    obj.style.display = 'flex';
    obj.style.animation = 'fadingIn 0.4s linear forwards'
}