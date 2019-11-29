var photoTimer = 30 * 1000;
var clockTimer = 1 * 1000;

setInterval(loadPhoto, photoTimer);

setInterval(setClock, clockTimer);

function loadPhoto() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            var data = JSON.parse(this.responseText);

            document.getElementById('photo').src = data['link'];
            document.getElementById('path').innerHTML = data['path'];
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