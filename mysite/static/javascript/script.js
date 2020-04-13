var isClickable = true;
var coefficientNumber = 0;
var nb_detail = 5;
var pauseNumber = 15;

//Appelée à chaque click sur le tableau
function check(event) {
    if (isClickable) {
        //Verifie si le nombre de clics autorisés est atteint
        checkClickNumber();
        checkClickPosition();
    }
}

//Vérifie si un détail à été trouvé
function checkClickPosition() {
    var painting = document.getElementsByClassName('painting')[0];

    var x = event.clientX; // x de la souris
    var y = event.clientY; // y de la souris

    var height =  painting.offsetHeight; //hauteur du tableau
    var width =  painting.offsetWidth; //largeur du tableau

    var viewportOffset = painting.getBoundingClientRect();
    var top = viewportOffset.top; // y du point haut-gauche du cadre
    var left = viewportOffset.left; // x du point haut-gauche du cadre

    scaleX = width / 100;
    scaleY = height / 100;

    // controle si le clic correspond à un détail
    var num = -1;
    for (var i = 0; i < nb_detail; i++) {
        if ((x >= left + (tab[i].x * scaleX)) &&
            (x <= left + (tab[i].x * scaleX) + (tab[i].width * scaleX)) &&
            (y >= top + (tab[i].y * scaleY)) &&
            (y <= top + (tab[i].y * scaleY) + (tab[i].height * scaleY))) {
            num = i;
            break;
        }
    }

    // check le détail correct
    if (num > -1 && num < nb_detail) {
        $.ajax({
            type : "POST",
            url : "check_detail",
            dataType: 'json',
            data : { 'num' : num + 1}
        })
        tab[num].checked = true;
        var position = num + 1;
        $('.footer .detail-image:nth-child('+ position +')').addClass('check');
    }

    // check si le niveau est fini
    var end = true;
    for (var i = 0; i < nb_detail; i++) {
        if (tab[i].checked == false) {
            end = false;
            break;
        }
    }

    if (end) {
        $('.next-level').addClass("show");
    }
}

//Ajoute un clic au compteur et vérifie si le nombre de click n'a pas été atteint
function checkClickNumber() {
    click++;
    $.ajax({
        type : "POST",
        url : "new_click",
        dataType: 'json',
        data : { 'click' : 1}
    })

    if (click >= pauseNumber) {
        coefficientNumber++;
        isClickable = false;
        setTimeout(() => {
          isClickable = true;
          if(pauseNumber == 15){
            pauseNumber = pauseNumber + 10;
          } else {
            pauseNumber = pauseNumber + 5 ;
          }
        }, coefficientNumber*10000);

        var secondsLeft = coefficientNumber * 10;
        $('.timer').addClass('show');
        $('.timer').removeClass('hide');
        $('.timer p').text(secondsLeft);
        var interval = setInterval(function() {
             secondsLeft --;
            $('.timer p').text(secondsLeft);
            if (secondsLeft <= 0) {
              $('.timer p').text('');
              $('.timer').addClass('hide');
              $('.timer').removeClass('show');
               clearInterval(interval);
            }
        }, 1000);
    }
}

//Affiche ou cache les popups
function popUp(obj){
  if($(obj).hasClass('show')){
    $(obj).removeClass('show');
    $(obj).addClass('hide');
  } else {
    $('.popup').removeClass('show');
    $(obj).addClass('show');
  }
}

//Cache les indices des détails qui ont déjà été trouvé
function checkClues(){
  for (var i = 0; i < nb_detail; i++) {
    if(tab[i].checked == true){
      $('.clues .details img:nth-child('+ (i+1) +')').addClass('hide');
    }
  }
}

// Affiche l'indice demandé 
function displayClue(index){
  $('.clue .value').text(tab[index].clue)
}


//fonctions pour gérer les cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$( document ).ready(function() {
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
});
