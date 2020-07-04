/**
 * Created by Uros on 3.7.2020.
 */

$(document).ready(function() {
       var indexBtn = $("button:contains('KnjizaraTest')");

       indexBtn.on('click',function () {
              var url = "/";
              window.open(url,"_self");

       });

       $('.btn.btn-outline-success.my-2').each(function(i, obj) {
              if(i == 0) {
                  $(this).on('click',function () {
                     var url = "/";
                     window.open(url,"_self");
                     });
              }
              else if(i == 1) {
                    $(this).on('click',function () {
                     var url = "/pretraga";
                     window.open(url,"_self");
                     });
              }
              else if(i == 2) {
                    $(this).on('click',function () {
                     var url = "/dodavanje_stavke_narudzbine";
                     window.open(url,"_self");
                     });
              }
              else if(i == 3) {
                    $(this).on('click',function () {
                     var url = "/nalog";
                     window.open(url,"_self");
                     });
              }

       });



});