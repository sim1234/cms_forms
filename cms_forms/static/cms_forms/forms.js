function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function submitCMSForm(form, method){
    let params = {
        method: method,
        cache: 'no-cache',
        credentials: 'same-origin',
        redirect: "manual",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    };
    if (method === "POST") {
        // TODO: get submit button via let submit = document.activeElement;
        params["body"] = new FormData(form);
    }
    fetch(form.action, params).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else if (response.ok) {
            response.text().then(text => {
                form.innerHTML = text;
                // TODO: Update file fields
                [...form.getElementsByTagName("script")].forEach(function (value) { // Execute scripts
                    value.remove();
                    const newScript = document.createElement("script");
                    if (value.src) {
                        newScript.src = value.src;
                    }
                    newScript.appendChild(document.createTextNode(value.innerHTML));
                    form.appendChild(newScript);
                })
            })
        } else {
            console.error(response);
        }
    })
}