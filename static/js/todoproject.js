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

function invitation(notificationID, decision){
    // Creating target url
    let currentUrl = window.location.href; 
    let baseUrl = currentUrl.split('/project/')[0]; 
    let targetUrl = baseUrl + 'decision_invite'; 

    // Removing notification from tile regardless of what decision made
    notificationTile = document.getElementById('not'+notificationID);
    notificationTile.remove();

    let csrftoken = getCookie('csrftoken');
    let data = {
        'decision':decision,
        'notificationID':notificationID,
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
}