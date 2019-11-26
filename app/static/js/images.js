var photoTimer = 30000;
var clockTimer = 1000;
var img_counter = 0

setInterval(loadPhoto, photoTimer);

setInterval(setClock, clockTimer);

function loadPhoto() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            var test = JSON.parse(this.responseText);

            document.getElementById('photo').src = test['link'];
            document.getElementById('path').innerHTML = test['path'];
        }
    };
    xhttp.open("GET", "/get_random_image", true);
    xhttp.send();
}

function setClock() {
    var d = new Date();
    document.getElementById('dateHead').innerHTML = d.toDateString();
    document.getElementById('timeHead').innerHTML = d.toLocaleTimeString();
}