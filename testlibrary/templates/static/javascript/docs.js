
function getClass(name,index) {
    if (index == null) {
        return document.getElementsByClassName(name);
    }

    else {
        return document.getElementsByClassName(name)[index];
    }
}

function addModalListener(elem) {
    elem.addEventListener('click', function(event) {
        event.preventDefault();
        if (isSelected(elem) == false) {
            /* console.log("okkk"); */
            toggleModalItem();
            toggleModalOption();
        }
        
    });
}

function addUserIconListener(elem) {
    elem.addEventListener('click', function(event) {
        event.preventDefault();
        modalContainer = getClass("modal-container",0);
        modalContainer.classList.toggle("modal-container--not-visible");
        setBodyBackgroundColor(0);
    } );
}

function addUserBucketListener(elem) {
    elem.addEventListener('click', function(event) {
        event.preventDefault();
        console.log("hello");
        getKorpa();
        modalContainer = getClass("modal-container",1);
        modalContainer.classList.toggle("modal-container--not-visible");
        setBodyBackgroundColor(1);
    } );
}



function setBodyBackgroundColor (index) {
    let container = getClass("main-container",0);
    if (isModalActive(index)) {
        $(".main-container").css({"background-color":"rgb(85, 81, 81)"});
        $(".main-container").css({"opacity":"0.95"});
    }
    else {
        $(".main-container").css({"background-color":""});
        $(".main-container").css({"opacity":"1.00"});
    }
}



function toggleModalItem() {
    let items = getClass("modal-item",null);
    for (let i=0;i<2;i++) {
        items[i].classList.toggle("selected-option");
    }
}

function toggleModalOption() {
    let options = getClass("modal-option",null);
    for (let i=0;i<2;i++) {
        options[i].classList.toggle("modal-option--not-visible");
    }
}

function setCloseModal(index) {
    let modalClose = getClass("modal-close",index);
    let modalContainer = getClass("modal-container",index);

    modalClose.addEventListener('click', function(event) {
        event.preventDefault();
        modalContainer.classList.toggle("modal-container--not-visible");
        setBodyBackgroundColor(index);
    });
}
/* (function () {
    setForModal()
}) (); */

function setForModal() {
    let items = getClass("modal-item",null);
    for (let i=0;i<2;i++) {
        addModalListener(items[i]);
        setCloseModal(i);
    }
}

function setBodyBackgroundColorRating (index) {
    let container = getClass("main-container",0);
    if (isModalActiveRating(index)) {
        $(".main-container").css({"background-color":"rgb(85, 81, 81)"});
        $(".main-container").css({"opacity":"0.80"});
    }
    else {
        $(".main-container").css({"background-color":""});
        $(".main-container").css({"opacity":"1.00"});
    }
}

function isModalActiveRating(index) {
    let modal = getClass("modal-container",index);
    if (modal.classList.length == 2) {
        return true;
    }
    return false;
}

function setForNav() {
    let userIcon = getClass("fa-user",0);
    addUserIconListener(userIcon);

    let bucketIcon = getClass("fa-shopping-basket",0);
    addUserBucketListener(bucketIcon);

}

function isSelected(elem) {
    for (let i=0;i<elem.classList.length;i++) {
        if (elem.classList[i] == "selected-option") {
            return true;
        }
    }
    return false
}

function isModalActive(index) {
    let modal = getClass("modal-container",index);
    if (modal.classList.length == 1) {
        return true;
    }
    return false;
}

function raiseModal() {
    console.log(elem.classList);
}

function insertUserModal(check) {
    let modalLogged = '<div class="modal-container modal-container--not-visible"> <i class="fas fa-times modal-close"></i> <div class="modal-items modal-items-gap"> <div class="modal-item modal-item--full-column selected-option"></div> <h3 class="modal-option__title">Nalog</h3> <a href="/user_info" class="button button--big modal-item--full-column">Korisnicki podaci</a> <a href="/narudzbine" class="button button--big modal-item--full-column">Naruceno</a> <a class="button button--big modal-item--full-column">Utisci</a> <a href="/ocene-i-misljenja" class="button button--big modal-item--full-column">Ocene i misljenja</a> <a href="/logout" class="button button--big modal-item--full-column">Logout</a> </div> </div>';
    if (check == true) {
        $(".modal-container")[0].remove()
        $(".nav-container").after(modalLogged);
        setForModal();
    }
    else {
        $(".nav-container").after(modalLogged);   
    } 
}