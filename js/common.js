var currentState = '';
$(document).ready(function () {
    setInterval(checkLocalState, 500);
});

function buildURL(anchor) {
    return anchor.substr(1);
}

function escapeString(string) {
    return string.replace("/", "\\/")
}

$(".nav a").on("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    var href = $(this).attr('href')
    updateState(href);
    $(".nav").find(".active").removeClass("active");
    $(this).parent().addClass("active");


    $(".content").load('html/' + href + '.html');
});

function checkLocalState() {
    if (document.location.hash && document.location.hash != currentState) {
        currentState = document.location.hash;
        if (currentState) {
            $(".content").load('html/' + buildURL(currentState) + '.html');
            $(".nav").find(".active").removeClass("active");
            $(".nav a[href=" + escapeString(buildURL(currentState)+"]")).parent().addClass("active");
        }
    }
}

function updateState(state) {
    state = "#" + state;
    if (state == currentState) {
        return false;
    }
    if (document.location.hash != state) {
        document.location.hash = state;
    }
    currentState = state;
    return true;
}