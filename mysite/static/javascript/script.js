function check(event) {
    var x = event.clientX; // x de la souris
    var y = event.clientY; // y de la souris

    var height = document.getElementById('painting').offsetHeight; //hauteur du tableau
    var width = document.getElementById('painting').offsetWidth; //largeur du tableau

    var viewportOffset = painting.getBoundingClientRect();
    var top = viewportOffset.top; // y du point haut-gauche du cadre
    var left = viewportOffset.left; // x du point haut-gauche du cadre

    var nb_level = 5;

    scaleX = width / 100;
    scaleY = height / 100;

    var num = -1;
    for (var i = 0; i < nb_level; i++) {
        if ((x >= left + (tab[i].x * scaleX)) &&
            (x <= left + (tab[i].x * scaleX) + (tab[i].width * scaleX)) &&
            (y >= top + (tab[i].y * scaleY)) &&
            (y <= top + (tab[i].y * scaleY) + (tab[i].height * scaleY))) {
            num = i;
            break;
        }
    }
    if (num > -1 && num < nb_level) {
        /*$.ajax({
            type : "POST",
            url : "/check_detail",
            dataType: 'json',
            data : { 'num' : num + 1}
        })*/
    
        tab[num].checked = true;
        $('.details div:nth-child(' + (num + 1) + ') img').addClass("check");
    }

   

    var end = true;
    for (var i = 0; i < nb_level; i++) {
        if (tab[i].checked == false) {
            end = false;
        }

    }
    if (end) {
        document.getElementById('nextlevel').style.display = 'block';
    }
}




////////    TODO : une seule fonction popup    //////////
function openPopUpClue() {
    document.getElementById('popup').style.display = 'block';
}

function closePopUpClue() {
    document.getElementById('popup').style.display = 'none';
}

function OpenClueText() {
    document.getElementById('clueText').style.display = 'block';
}

function CloseClueText() {
    document.getElementById('clueText').style.display = 'none';
}

function OpenNoCluePopUp() {
    document.getElementById('noClueAvalaible').style.display = 'block';
}

function CloseNoCluePopUp() {
    document.getElementById('noClueAvalaible').style.display = 'none';
}