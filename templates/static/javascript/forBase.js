/**
 * Created by Uros on 3.7.2020.
 */
var mywindow = window;
$(document).ready(function() {
  enableNav();
});

function pretraga(value,url) {
    // mywindow.open('/pretraga/',"_self");
  $.ajax({
      type: 'GET',
      url: url,
      data:{'pretraga':value},
      dataType:'html',
      success:porukaNakonOdgovora,
      error: console.log("greska")
  });
}
function clickSetUp(e,url) {
    if (e.which === 1) {
        window.open(url,"_self");
    }
    if (e.which === 2) {
        window.open(url,"_blank");
    }
}
function porukaNakonOdgovora(response) {
    console.log(response);
    $("body").html(response);
    enableNav();
    // var popup = window.open('/pretraga/',"_blank");
    // popup.$('body').html("hello world");


}

function enableNav() {
  var indexBtn = $("button:contains('KnjizaraTest')");

  indexBtn.on('click',function () {
         var url = "/";

         window.open(url,"_self");

  });

  $('.btn.btn-outline-success.my-2').each(function(i, obj) {
         if(i == 0) {
             var url = "/";
              $(this).on('mousedown', function(e) {
                    clickSetUp(e,url);

                });
         }
         else if(i == 1) {
               $(this).on('click',function () {
                 var value = $(".form-control.mr-sm-2").val();
                 if(value.length>0) {
                   var url = "/pretraga/";
                   pretraga(value,url);
                 }

                });
         }
         else if(i == 2) {
             var url = "/korpa";
             $(this).on('mousedown', function(e) {
                    clickSetUp(e,url);

            });
         }
         else if(i == 3) {
               var url = "/nalog";
               $(this).on('mousedown', function(e) {
                    clickSetUp(e,url);

                });
         }

  });
}
