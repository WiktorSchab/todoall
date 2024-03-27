const radioButtonContainer = document.getElementsByClassName('radio-button-container');

for (i=0; i < radioButtonContainer.length; i++){
    let colorToSet = radioButtonContainer[i].querySelector('input[type="radio"]').value;

    let spanElement = radioButtonContainer[i].querySelector('span');
    spanElement.classList.add('radio-'+colorToSet);
}

function showFlex(elementId) {
    let obj = document.getElementById(elementId);
    
    obj.style.display = 'flex';
    obj.style.animation = 'fadingIn 0.4s linear forwards'
}