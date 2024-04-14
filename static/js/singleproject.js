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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Szukaj ciasteczka o nazwie csrfToken
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function addUser(projectID) {
    // Object to display feedback message
    let requestInfoDisplay = document.getElementById('request-status-info');

    // Creating target url
    let currentUrl = window.location.href; 
    let baseUrl = currentUrl.split('/project/')[0]; 
    let targetUrl = baseUrl + '/add_user'; 

    // Getting value from input
    let userInput = document.getElementById('user-input');
    let user = userInput.value;
    
    let csrftoken = getCookie('csrftoken');
    let data = {
        'projectID':projectID,
    }

    // Sending Ajax req to add_user view
    fetch(targetUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data) // Adding data
    })
    // Displaying feedback
    .then(response => response.json())
    .then(data => {
        requestInfoDisplay.innerHTML = data.req_status;
    })
}

