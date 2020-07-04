/**
 * Created by Uros on 24.4.2020.
 */
$(document).ready(function() {

    $("button:contains('Stavi u korpu')").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var url = $(this).attr("value");
           dodaj_u_korpu(knjigaISBN,url);
        });
    $("button:contains('Budite prvi')").on('click', function () {
           ocenjivanje();
        });

});


function zvezdice(br) {
    var ukupno = "";
    var i;
    for (i=0;i<br;i++) {
        ukupno+="&#11088;";
    }
    document.write(ukupno);
}
function komadi() {
    var ukupno = "";
    var i;
    for (i=2;i<12;i++) {
        var br = (i).toString();
        var option = document.createElement("option");
        option.text = br;
        option.value = br;
        var select = document.getElementById("kolicina");
        select.appendChild(option);
    }

}
function dodaj_u_korpu(knjigaISBN,url) {
    var kolicina = getKolicina();
    $.ajax({
        type: 'POST',
        url: url,
        data:{'knjigaISBN':knjigaISBN,'kolicina':kolicina},
        dataType:'json',
        success:poruka_nakon_dodavanja,
        error: $(".modal-body").html("Morate biti prijavljeni za ovu akciju.")
    });
}
function poruka_nakon_dodavanja (response) {
    poruka = JSON.parse(response);
    if (poruka === 1) {
        $(".modal-body").html("Knjiga je dodata u korpu!");
    }

    else {
        $(".modal-body").html("Knjiga vec postoji u korpi.");
    }
    $(".modal-body").css("width","");
    $(".modal-body").css("margin","");
}
function poruka_nakon_ocenjivanja(response) {
    poruka = JSON.parse(response);
    alert(poruka);
    if (poruka === 1) {
        $(".modal-body").html("Uspesno ste ocenili knjigu!");
    }
    else if (poruka === 2) {
        $(".modal-body").html("Azurirali ste svoju ocenu za ovu knjigu.");
    }
}
function ocenjivanje() {
    // alert("okk");
    $(".modal-body").html("");
    $(".modal-body").append('<div class="rate">');
    for (i = 5;i>0;i--) {
        var id="star"+i;
        var value = i+"";

        var nekiText = i+" stars";
        var forAdd = '<input type="radio" id="idd" name="rate" value="valuee" /> <label for="idd" title="valuee">valuee stars</label>'.replaceAll("idd",id).replaceAll("valuee",value).replaceAll('\"',"'");
        $(".rate").append(forAdd);
    }
    $(".modal-body").css("width","50%");
    $(".modal-body").css("margin","0 auto");
    var labels = $("label");
    labels.on('click',function () {
        ocenjivanjeKnjige(getISBN(),$(this).attr("title"));

     });

}


function ocenjivanjeKnjige(knjigaISBN,ocena) {
    $.ajax({
        type: 'POST',
        url: "/ocenjivanje_knjige",
        data:{'knjigaISBN':knjigaISBN,'ocena':ocena},
        dataType:'json',
        success:poruka_nakon_ocenjivanja,
        error: $(".modal-body").html("Morate biti prijavljeni za ovu akciju.")
    });
}


function getISBN() {
    var isbn = $(".btn.btn-outline-success.my-2.default-btn").attr("data-value");
    return isbn;
}
function getCsrf() {
    var csrf = $("textarea").attr("data-value");
    return csrf;
}


function getKolicina() {
   var e = document.getElementById("kolicina");
   var kol  = parseInt(e.options[e.selectedIndex].value);
   return kol;
}
function testzakol(knjiga) {

    alert(knjiga);
}
function modalZaDom(){
    document.write(
      '<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">' +
      '<div class="modal-dialog" role="document">' +
      '<div class="modal-content">' +
      '<div class="modal-header">' +
      '<h5 class="modal-title" id="exampleModalLabel">KnjizaraTest</h5>' +
      '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
      '<span aria-hidden="true">&times;</span> </button> </div> <div class="modal-body">' +
      ' ... ' +
      '</div>' +
      '<div class="modal-footer">' +
      '<button type="button" class="btn btn-secondary" data-dismiss="modal">' +
      'Close' +
      '</button>' +
      '</div>' +
      '</div>' +
      '</div>' +
      '</div>'
    );
}

