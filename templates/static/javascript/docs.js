
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
        modalContainer.classList.toggle("modal-option--not-visible");
        setBodyBackgroundColor(0);
    } );
}

function addUserBucketListener(elem) {
    elem.addEventListener('click', function(event) {
        event.preventDefault();
        getKorpa();
        modalContainer = getClass("modal-container",1);
        modalContainer.classList.toggle("modal-option--not-visible");
        setBodyBackgroundColor(1);
    } );
}



function setBodyBackgroundColor (index) {
    let container = getClass("main-container",0);
    if (isModalActive(index)) {
        container.style.backgroundColor = "rgba(0, 0, 0, 0.6)";
    }
    else {
        container.style.backgroundColor = "";
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
        modalContainer.classList.toggle("modal-option--not-visible");
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





