/**
 * Created by Uros on 24.4.2020.
 */


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

