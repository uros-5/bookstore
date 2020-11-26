function userInfoBtnListener () {
    let btn = $(".button.user-data__button");
    btn.click( function () {
        $.ajax({
            type: 'POST',
            url: "/user-info-update/",
            data: {"csrfmiddlewaretoken":getCsrf(0),"userInfo":getUserInfo()},
            dataType:'json',
            success:afterUpdateUserInfo,
            error: zaGreske2
        });
    })
}

function getUserInfo() {
    let inputKeys = ["username","email","first_name","last_name","grad","ulicaIBroj","telefon"];
    let userInfoArray = $(".main-container > input");
    let return_obj = {};
    for (let i = 0;i<userInfoArray.length;i++) {
        return_obj[inputKeys[i]] = userInfoArray[i].value;
    }
    return return_obj;
}

function afterUpdateUserInfo(response) {
    console.log(response);
}