
var updateState = function(state) {
    if (!state) return;
    $(".content").load('html/' + state.page + '.html');
};

$(document).ready(function () {
    window.addEventListener('hashchange', updateState);
    window.addEventListener('popstate', function(e) {
        updateState(e.state);
    });

    var state = {
        page: 'games'
    };
    history.pushState(state, '', state.page);
    updateState(state);
});

$(".navbar-nav").click(function(e) {
    if (e.target.tagName !== 'A') return;

    e.preventDefault();
    var state = {
        page: e.target.getAttribute('href')
    };
    history.pushState(state, '', state.page);
    updateState(state);
});