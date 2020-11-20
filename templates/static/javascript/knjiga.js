/**
 * Created by Uros on 24.4.2020.
 */
$(document).ready(function() {

    $("button:contains('Stavi u korpu')").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var kolicina = getKolicina();
           var url = $(this).attr("value");

           var podaci = {'knjigaISBN':knjigaISBN,'kolicina':kolicina};
           ajaxPOST(podaci,url,poruka_nakon_dodavanja);
        });
    $("button:contains('Budite prvi')").on('click', function () {
           zvezdiceNaModalu();
        });
    $("button:contains('Ocenite knjigu')").on('click', function () {
           zvezdiceNaModalu();
        });

});


function ajaxPOST(podaci,url,success) {
    $.ajax({
        type: 'POST',
        url: url,
        data:podaci,
        dataType:'json',
        success:success,
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





function odabirOcene () {
    var labels = $("label");
    labels.on('click',function () {
        var knjigaISBN = getISBN();
        var ocena = $(this).attr("title");
        var url = "/ocenjivanje_knjige";
        var podaci = {'knjigaISBN':getISBN(),'ocena':ocena};
        ajaxPOST(podaci,url,poruka_nakon_ocenjivanja);

     });
}

function poruka_nakon_ocenjivanja(response) {
    var poruka = response["poruka"];
    var oceneKnjige = response["oceneKnjige"]

    if (poruka === 1) {
        $(".modal-body").html("Uspesno ste ocenili knjigu!");
        napraviNovuTabeluZaOcene(oceneKnjige);
    }
    else if (poruka === 2) {
        $(".modal-body").html("Azurirali ste svoju ocenu za ovu knjigu.");
        napraviNovuTabeluZaOcene(oceneKnjige);
    }
}

function napraviNovuTabeluZaOcene(oceneKnjige) {
    $("table")[0].remove();
    // var col = ;
    $( ".col-xs-12" ).eq(0).append('<table>');
    $( ".col-xs-12 > table" ).eq(0).append('<tbody><tr> <th>Ocenio</th> <th>Ocena</th> </tr></tbody>');

    for (i = 0;i<oceneKnjige.length;i++) {

        var red = "<tr> <td><b>kor</b></td> <td>ocena</td> </tr>".replaceAll("kor",oceneKnjige[i][0]).replaceAll("ocena",napraviZvezdice(oceneKnjige[i][1]));
        $("tbody").eq(0).append(red);
    }
}

//getters

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

// VEZANO ZA DODAVANJE ELEMENATA NA DOM knjiga.html
function zvezdice(br) {
    document.write(napraviZvezdice(br));
}
function napraviZvezdice(br) {
    var ukupno = "";
    var i;
    for (i=0;i<br;i++) {
        ukupno+="&#11088;";
        /* ukupno+="a"; */
    }
    return ukupno;
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

function zvezdiceNaModalu() {
    //DODAVANJE ZVEZDICA ZA OCENJIVANJE NA MODALU
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
    //ODABIR OCENE
    odabirOcene();

}
