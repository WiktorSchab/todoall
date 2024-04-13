function extendTask(taskId){
    // Retrieve task elements
    let task = document.getElementById(taskId);
    let extendContent = task.getElementsByClassName('extended-content-task')[0];
    let extendButton = task.getElementsByClassName('extend-button')[0];

    // Modify button - change icon and click event handler
    extendButton.classList.remove('bi-arrow-down');
    extendButton.classList.add('bi-arrow-up');
    extendButton.removeAttribute("onclick");
    extendButton.onclick = function(){colapseTask(taskId)};

    // Display content
    extendContent.style.display = 'flex';
}

function colapseTask(taskId){
    // Retrieve task elements
    let task = document.getElementById(taskId);
    let extendContent = task.getElementsByClassName('extended-content-task')[0];
    let extendButton = task.getElementsByClassName('extend-button')[0];

    // Modify button - change icon and click event handler
    extendButton.classList.remove('bi-arrow-up');
    extendButton.classList.add('bi-arrow-down');
    extendButton.removeAttribute("onclick");
    extendButton.onclick = function(){extendTask(taskId)};

    // Hide content
    extendContent.style.display = 'none';
}

const radioButtonContainer = document.getElementsByClassName('radio-button-container');

for (i=0; i < radioButtonContainer.length; i++){
    let colorToSet = radioButtonContainer[i].querySelector('input[type="radio"]').value;

    let spanElement = radioButtonContainer[i].querySelector('span');
    spanElement.classList.add('radio-'+colorToSet);
}

function newTask(elementId, tableName, tableID) {
    // Showing obj
    showFlex(elementId);
    
    let obj = document.getElementById(elementId);

    let title = obj.querySelector('#new-task-title');
    title.innerHTML = tableName;

    // Adding id of table to the invisible input, so data can added only to choosed table
    let tableIdInput = document.getElementById('id_table_id');
    tableIdInput.value = tableID;
}
