/**
 * Created by Uros on 25.4.2020.
 */

$(document).ready(function() {

       $(".btn.btn-outline-success.my-2.default-btn").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var url = $(this).attr("value");
           korpaAction(knjigaISBN,url);
           // var putanja = $(this).attr("id").toString().toLowerCase().replace(" ","_");
           //  window.open(putanja,"_self");
        });
       $("button:contains('Obrisi')").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var url = $(this).attr("value");
           korpaAction(knjigaISBN,url);
        });
       $("button:contains('-1')").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var url = $(this).attr("value");
           korpaAction(knjigaISBN,url);
        });
       $("button:contains('+1')").on('click', function () {
           var knjigaISBN = $(this).attr("data-value");
           var url = $(this).attr("value");
           korpaAction(knjigaISBN,url);
        });

});

function testISBN(knjigaISBN) {
    alert(knjigaISBN);
}

function korpaAction(knjigaISBN,url) {

    if(url.toString() === "/naruci_iz_korpe") {
        $.ajax({
            type: 'POST',
            url: url,
            data: {'radnja':"narucivanje"},
            dataType:'json',
            success:modifyDivDom,
            error: zaGreske
        });
    }
    else if(url.toString() === "/brisanje_iz_korpe") {
        $.ajax({
            type: 'POST',
            url: url,
            data:{'knjigaISBN':knjigaISBN,'radnja':'brisanje'},
            dataType:'json',
            success:modifyDivDom,
            error: zaGreske
        });
    }
    else if(url.toString() === "/smanji_kolicinu") {
        $.ajax({
            type: 'POST',
            url: url,
            data:{'knjigaISBN':knjigaISBN,'radnja':'oduzimanje'},
            dataType:'json',
            success:modifyDivDom,
            error: zaGreske
        });
    }
    else if(url.toString() === "/povecaj_kolicinu") {
        $.ajax({
            type: 'POST',
            url: url,
            data:{'knjigaISBN':knjigaISBN,'radnja':'dodavanje'},
            dataType:'json',
            success:modifyDivDom,
            error: zaGreske
        });
    }
}
function modifyDivDom(response) {
    var knjigaISBN = String(response["knjigaISBN"]);
    var poruka = response["poruka"];

    if(poruka === 1) {
        var root = ".d-flex.justify-content-center.default-look"
        $(".col").remove();
        $(root).append('<div class="col"></div>');
        $(".col").append('<h4>Sadrzaj korpe</h4>');
        $(".col").append('<p id="ukupno">Ukupno: <b> 0.00 din </b></p>');
        $(".modal-body").html("Narudzbina je uspesna!");
    }
    else if (poruka===2) {
        var divKnjige = "knjiga_"+knjigaISBN;
        $("."+divKnjige).remove();
        setUkupno();
    }
    else if (poruka === 3) {
        var kolicina = String(response["kolicina"]);
        var kolicinaInt = response["kolicina"]
        var ukupno = (parseFloat($("td#cena_"+knjigaISBN).html().replace("Cena: ",""))*kolicinaInt).toFixed(2);
        $("td#kolicina_"+knjigaISBN).html("Komada: "+kolicina);
        if(kolicinaInt == 1) {
            $("td#kolicina_"+knjigaISBN).hide();
        }
        else {
            $("td#kolicina_"+knjigaISBN).show();
        }
        $("td#ukupno_"+knjigaISBN).html("Ukupno: "+ukupno);
        setUkupno();

    }
    else if (poruka === 4) {
        var kolicina = String(response["kolicina"]);
        var kolicinaInt = response["kolicina"]
        var ukupno = (parseFloat($("td#cena_"+knjigaISBN).html().replace("Cena: ",""))*kolicinaInt).toFixed(2);
        if(kolicinaInt == 1) {
            $("td#kolicina_"+knjigaISBN).hide();
        }
        else {
            $("td#kolicina_"+knjigaISBN).show();
        }
        $("td#kolicina_"+knjigaISBN).html("Komada: "+kolicina);
        $("td#ukupno_"+knjigaISBN).html("Ukupno: "+ukupno);

        setUkupno();
    }
}

function setUkupno () {
    var ukupno = 0;
    var i = $("table tr td[id^='ukupno_']").each(
        function () {

            var ukupno2 = parseFloat($(this).html().replace('Ukupno: ',''));
            console.log("Konzola:" + ukupno2.toString())
            ukupno = ukupno + ukupno2;

        }
    );
    // console.log(ukupno);
    $("p#ukupno").html("Ukupno: "+"<b>"+ukupno.toString()+" din</b>");
}
function zaGreske() {
    alert("Greska");
}
function narucitest() {
    alert("Naruceno");
}