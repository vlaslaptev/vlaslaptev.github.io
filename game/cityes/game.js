document.getElementById("enter").addEventListener("click", function () {
    game();
});

var played = [];
var lastChar = "";

function loadCityInfo(cityName) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://ru.wikipedia.org/api/rest_v1/page/summary/" + cityName); // false for synchronous request


    xhr.onload = function (e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
            var result = JSON.parse(xhr.responseText);
            console.log(result.extract);
            document.getElementById("wiki-text").innerHTML = result.extract;
        }
    };
    xhr.send(null);

}

function game() {
    var cityName = document.getElementById("game-input").value;
    if (checkCity(cityName)) {
        document.getElementById("history-input").value = cityName + "\n" + document.getElementById("history-input").value;
        var lastChar = getLustChar(cityName);
        document.getElementById("game-input").value = lastChar.toUpperCase();
        loadCityInfo(cityName);
    }
}

function checkCity(city) {
    if (lastChar != "" && city[0].toUpperCase() != lastChar.toUpperCase()) {
        alert("Город должен начинаться с буквы " + lastChar);
        document.getElementById("game-input").value = lastChar.toUpperCase();
        return false;
    }
    if (played.indexOf(city) > -1) {
        alert("Этого город уже был");
        return false;
    }
    if (cityes.indexOf(city) > -1) {
        played.push(city);
        lastChar = getLustChar(city);
        return true;
    } else {
        alert("Этого города нет в базе");
    }
}

function keypress(e) {
    if (e.keyCode == 13) {
        game();
    }
}

function getLustChar(cityName) {
    var lastChar = cityName[cityName.length - 1];
    if (lastChar == "ь") {
        lastChar = cityName[cityName.length - 2];
    }
    return lastChar;
}