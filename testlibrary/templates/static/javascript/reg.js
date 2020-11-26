function addListenerRegBtn() {
    $("#reg-form").on("submit" , function(event) {
        event.preventDefault();
        regForm()
    })
}

function regForm() {
    $.ajax({
        type: 'POST',
        url: "reg-user",
        data: {"csrfmiddlewaretoken":getCsrf(1),'username':getUsernameReg(),"password":getPasswordReg(),
    "first_name":getName(),"last_name":getLastName(),"email":getEmail()},
        /* headers: {"X-CSRFToken":getCsrf()} */
        dataType:'json',
        success:successReg,
        error: errorReg
    });
}

function successReg(message) {
    if (message["register"] === 1) {
        console.log("Username already exists.")
    }
    else if (message["register"] === 2) {
        console.log("Email already exists.")
    }
    else if (message["register"] === true) {
        insertUserModal(true);
    }
    else if (message["register"] === false) {
        console.log("Fill all necessary informations.")
    }
}

function errorReg(message) {
    console.log(message);
}

function getName() {
    return $("#reg-form-name").val()
}

function getLastName() {
    return $("#reg-form-last-name").val()
}

function getEmail() {
    return $("#reg-form-email").val()
}

function getUsernameReg() {
    return $("#reg-form-username").val()
}

function getPasswordReg() {
    return $("#reg-form-password").val()
}

function getPasswordRegCheck() {
    return $("#reg-form-password-check").val()
}





function getName() {
    return $("#reg-form-name").val()
}