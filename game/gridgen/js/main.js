var wrapper = document.getElementById("main-wrapper");
var rowProbability = [1, 1, 1, 1, 1, 1, 1, 2, 3, 4];
var columnProbability = [1, 1, 1, 1, 1, 1, 2, 2, 3];

function addGridElements() {
    for (var i = 0; i < 500; i++) {
        var div = document.createElement('div');
        div.className = "cell";
        div.style.background = getRandomColor();
        div.style.gridRow = "span " + randomWithProbability(rowProbability);
        div.style.gridColumn = "span " + randomWithProbability(columnProbability);
        div.innerHTML = nextChar();
        wrapper.appendChild(div);
    }
}

addGridElements();

window.onbeforeunload = function () {
    window.scrollTo(0, 0);
};


function getRandomColor() {
    var r = Math.round((getRandomInt(0, 255) + 140) / 2);
    var g = Math.round((getRandomInt(0, 255) + 140) / 2);
    var b = Math.round((getRandomInt(0, 255) + 140) / 2);
    return 'rgb(' + r + ', ' + g + ', ' + b + ')';
}

function nextChar() {
    var nxtChar = "";
    if (getRandomInt(0, 10) > 4) {
        nxtChar = String.fromCharCode(getRandomInt(0, 65536));
        return nxtChar;
    }
    nxtChar += getRandomInt(11, 136755);
    return "&#" + nxtChar;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function randomWithProbability(notRandomNumbers) {
    var idx = Math.floor(Math.random() * notRandomNumbers.length);
    return notRandomNumbers[idx];
}

window.onscroll = function (ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        addGridElements();
    }
};
