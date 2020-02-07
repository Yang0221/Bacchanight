function getCoordinate(event)
{
    var x = event.clientX ;
    var y = event.clientY;
    return {x : x, y : y};
}

function checkCoordinate(x, y){
    var solidX = 755;
    var solidY = 450;
    if( (x < solidX + 15) && (x > solidX - 15) && (y < solidY + 15) && (y > solidY + 15)){
        return true;
    }
    return false;
}

function check(detimg, event){
    //document.getElementById(detimg).style.border = "solid 5px #c9e265";

    console.log(tab);


    var height = document.getElementById('painting').offsetHeight / 10;
    var width = document.getElementById('painting').offsetWidth / 10;

    //console.log("height : " + height + "width : " + width)

    var viewportOffset = painting.getBoundingClientRect();
    // these are relative to the viewport, i.e. the window
    var top = viewportOffset.top;

    var left = viewportOffset.left;
    var xup = left + (3*width);
    var xdown = left + (4*width);
    var yup = top + (7*height);
    var ydown = top + (8*height);
    console.log(xup);

    //console.log("x : " + (left + (3*width)) + "\n x2 :" + (left + (4*width)) + "\ny : " + (top + (7*height)) + "\ny2 : " + (left +(8*height) ) );
    if( event.clientX > xup && event.clientX < xdown && event.clientY > yup && event.clientY < ydown){
        console.log('ok');
        document.getElementById(detimg).setAttribute("class", "check");
        document.getElementById("nextlevel").style.display = "block";
    }

    console.log(" x : " + event.clientX + "\n y : " + event.clientY);
    //  var x = (event.clientX) - (document.getElementById('tableau').offsetWidth);
    //console.log("width :" +  document.getElementById('painting').offsetWidth
     //+ "\n height : " + document.getElementById('painting').offsetHeight);
    //  + "\n x : " + event.clientX + "\n y : " + event.clientY
    //  + "\n top position : " + document.getElementById('tableau').offsetTop
    // );
    //var coordinates = getCoordinate(event);
    //console.log("x : " + coordinates.x + " y : " + coordinates.y);
    //if(checkCoordinate(x, coordinates.y)){
    //}
    //document.getElementById(detimg).setAttribute("class","check");

    // Popup for indice
    /*var indice = document.getElementById('PopupIndice');
    function openIndice() {
          indice.style.top = "0px";
    }
    function closeIndice() {
          indice.style.top = "-300px";
    }*/
}
function openPopUpClue(){
    document.getElementById('popup').style.display = 'block';
}
function closePopUpClue(){
    document.getElementById('popup').style.display = 'none';
}
function OpenClueText(){
    document.getElementById('clueText').style.display = 'block';
}
function CloseClueText(){
    document.getElementById('clueText').style.display = 'none';
}
function OpenNoCluePopUp(){
    document.getElementById('noClueAvalaible').style.display = 'block';
}
function CloseNoCluePopUp(){
    document.getElementById('noClueAvalaible').style.display = 'none';
}
