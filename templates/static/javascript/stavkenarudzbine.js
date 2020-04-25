/**
 * Created by Uros on 25.4.2020.
 */
function testISBN(knjigaISBN) {
    alert(knjigaISBN);
}
function obrisiIzKorpe(knjigaISBN,url) {
    $.ajax({
        type: 'POST',
        url: url,
        data:{'knjigaISBN':knjigaISBN,'radnja':'brisanje'},
        dataType:'json',
        success:ukloniDivDom,
        error: zaGreske
    });
}
function ukloniDivDom(response) {
    var knjigaISBN = String(response["knjigaISBN"]);
    var poruka = response["poruka"];
    if (poruka===1) {
        var divKnjige = "knjiga_"+knjigaISBN;
        $("."+divKnjige).remove();
    }
    setUkupno();
}
function smanjiKolicinu(knjigaISBN,url) {
    $.ajax({
        type: 'POST',
        url: url,
        data:{'knjigaISBN':knjigaISBN,'radnja':'oduzimanje'},
        dataType:'json',
        success:smanjiKolicinuDom,
        error: zaGreske
    });
}
function smanjiKolicinuDom (response) {

    var poruka = response["poruka"];

    if(poruka === 1) {
        var knjigaISBN = String(response["knjigaISBN"]);
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
}
function povecajKolicinu(knjigaISBN,url) {
    $.ajax({
        type: 'POST',
        url: url,
        data:{'knjigaISBN':knjigaISBN,'radnja':'dodavanje'},
        dataType:'json',
        success:povecajKolicinuDom,
        error: zaGreske
    });
}
function povecajKolicinuDom(response) {
    var poruka = response["poruka"];
     if(poruka === 1) {
        var knjigaISBN = String(response["knjigaISBN"]);
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
    $("p#ukupno").html("Ukupno: "+ukupno.toString());
}
function zaGreske() {
    alert("Greska");
}