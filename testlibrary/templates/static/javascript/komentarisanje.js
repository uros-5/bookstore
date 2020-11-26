function addKomentarBtnListener () {
    $(".button.button--big:contains('Komentarisi')").click(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/komentarisanje/",
            data: {"csrfmiddlewaretoken":getCsrf(0),"komentar":getKomentar(),"ISBN":isbn},
            dataType:'json',
            success:afterKomentarPosted,
            error: zaGreske2
        });
    });
}

function getKomentar() {
    return $("input.main-container__label").val()
}

function afterKomentarPosted (response) {
    console.log(response);
}

