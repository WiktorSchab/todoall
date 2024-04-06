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
