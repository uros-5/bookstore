let selectorStar = ".rate > .font-zvezdica:eq(star)";
let currentStar = 0;
let clickedStar = 0;
let clicked = false;

function addOcenjivanjeListener () {
    let modalContainer = getClass("modal-container",2);
    setCloseRatingModal(2);
    $(".button:contains('Ocenite')").click(function(event) {
        event.preventDefault();
        modalContainer.classList.toggle("modal-option--not-visible");
        setBodyBackgroundColorRating(2);
    })
}

function setHover(placeno) {
    if(placeno == 3 || placeno || 4) {
        let stars = $(".rate > .font-zvezdica");
        for(let i=0;i<stars.length;i++) {
            $(selectorStar.replace("star",i+"") ).on("mouseover",function() {
                hoverIn(i)
            });

            $(selectorStar.replace("star",i+"") ).on("mouseout", function() {
                hoverOut(i);
            });

            $(selectorStar.replace("star",i+"") ).on("click", function() {
                hoverOut(i);
                hoverIn(i);
                clicked = !clicked;
                clickedStar = i+1;
            });
        }

        /* $(".rate").on("mouseover",function() {
            console.log(currentStar);
        }) */

        /* $(".rate").on("mouseout",function() {
            hoverOut(currentStar);
            console.log("out")
        }) */
    }
    
}
/* rgb(219, 186, 139) */
function hoverIn(index) {
    currentStar = index;
    for(let i=0;i<index+1;i++) {
        $(selectorStar.replace("star",i)).css("color","rgb(255,172,51)");
        $(selectorStar.replace("star",i)).css("cursor","pointer");
    }
}

function hoverOut(index) {
    currentStar = index;
    for(let i=0;i<index+1;i++) {
        if (clicked == false) {
            $(selectorStar.replace("star",i+"")).css("color","rgb(113, 72, 14)");
            $(selectorStar.replace("star",i+"")).css("cursor","default");
        }
        
    }
}

function setCloseRatingModal(index) {
    let modalClose = getClass("modal-close",index);
    let modalContainer = getClass("modal-container",index);

    modalClose.addEventListener('click', function(event) {
        event.preventDefault();
        modalContainer.classList.toggle("modal-option--not-visible");
        setBodyBackgroundColor(index);
        // ajaks
        if (clickedStar != 0) {
            $.ajax({
                type: 'POST',
                url: "/ocenjivanje/",
                data: {"csrfmiddlewaretoken":getCsrf(0),"ocena":clickedStar,"ISBN":isbn},
                dataType:'json',
                success:afterKomentarPosted,
                error: zaGreske2
            });
        }
        
    });
}

function afterRating(response) {
    console.log(response);
}

function zvezdice(counter) {
    let ukupno = "";
    for(let i=0;i<counter;i++) {
        ukupno+="a ";
    }
    document.write(ukupno);
}