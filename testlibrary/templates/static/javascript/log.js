function addListenerLogBtn() {
    $("#log-form").on("submit" , function(event) {
        event.preventDefault();
        console.log("forma je poslata");
        logForm()
    })
}

function logForm() {
    $.ajax({
        type: 'POST',
        url: "/log-user/",
        data: {"csrfmiddlewaretoken":getCsrf(0),'username':getUsername(),"password":getPassword()},
        /* headers: {"X-CSRFToken":getCsrf()} */
        dataType:'json',
        success:successLogin,
        error: errorLogin
    });
}

function getUsername() {
    return $("#log-form-username").val()
}

function getPassword() {
    return $("#log-form-password").val()
}

function getCsrf(index) {
    return $("input[name='csrfmiddlewaretoken']")[index].value;
}

function getCountCsrf() {
    return $("input[name='csrfmiddlewaretoken']").length
}

function successLogin(message) {
    if (message["login"] == true) {
        insertUserModal(true);
        setCloseModal(1);
        
    }
    else if (message["login"] == false) {
        console.log("ERROR")
    }
}

function errorLogin(message) {
    console.log(message);
}