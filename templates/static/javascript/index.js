/**
 * Created by Uros on 16.6.2020.
 */

$(document).ready(function() {
       $(".nova-knjiga__slika").on('click', function () {
           var putanja = $(this).attr("id").toString().toLowerCase().replace(" ","_");
           // alert(putanja);
            window.open(putanja,"_self");
        });
       $(".p-2").on('click', function () {
           var putanja = $(this).attr("id").toString().toLowerCase().replace(" ","_");
            // alert(putanja);
            window.open(putanja,"_self");
        });

        $("body").hide().fadeIn(1500);

});