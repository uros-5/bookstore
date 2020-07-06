$(document).ready(function() {

    $("button:contains('Snimi izmene')").on('click', function () {
           var userID = $(this).attr("data-value");
          var url = $(this).attr("value");
          sacuvaj_izmene(userID,url);
        });

});

function sacuvaj_izmene(userID,url) {
  var data = get_input();
  data['userID'] = userID;
  $.ajax({
      type: 'POST',
      url: url,
      data:data,
      dataType:'json',
      success:poruka_nakon_dodavanja,
      error: console.log("Greska")
  });
}

function get_input() {
  var data = {};
  var inputs = $(".form-control");
  inputs.each(function(i, obj) {
    if(i>1) {
      var id = $(this).attr("id");
      var value = $(this).val();
      data[id] = value;
    }

  });

  return data;

}

function poruka_nakon_dodavanja(response) {
  var poruka = response["poruka"];
  var odgovor = response["odgovor"]
  if(poruka === 1) {
    $(".modal-body").html(odgovor.toString());
  }
  else if(poruka === 2) {
    $(".modal-body").html(odgovor.toString());
  }

}
