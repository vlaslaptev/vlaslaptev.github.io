var steps;
var $_baseDiv;

$(document).ready(function () {
    setDraggable($('.round'));
    droppable($('.tower'));
    steps = 0;
    $_baseDiv = $(".base")[0];
});

function cancel(e) {
    e.preventDefault();
    e.stopPropagation();
    return false;
}

function setDraggable(element) {
    $(element)
        .attr('draggable', 'true')
        .bind('dragend', cancel)
        .bind('dragstart', function (event) {
            if (canBeDragged($(event.target).parent(), event.target.id))
                event.originalEvent.dataTransfer.setData("Text", event.target.id);
            return true;
        })
}

function droppable(element) {
    $(element)
        .bind('dragover', cancel)
        .bind('drop', function (event) {
            event.preventDefault();
            var target = $(event.target);
            if (!target.hasClass("tower")) {
                target = $(target.parents(".tower"));
            }
            var discId = event.originalEvent.dataTransfer.getData("Text");
            if (discId && canAppend(target, discId)) {
                $("#count").text(++steps);
                var disc = $("#" + discId);
                disc.remove();
                target.append(disc);
                setDraggable(disc);
            }
            winCheck();
            return false;
        });
}

function winCheck() {
    if ($("#tower-3").children().length == 5) {
        $("#steps").append('<p>Победа</p>')
    }
}

function canBeDragged(from, discId) {
    return $(from).children().last().attr('id') == discId;
}

function canAppend(target, discId) {
    var children = $(target).children();
    return children.length == 1 || parseInt(children.last().attr('id')) >= parseInt(discId);
}

$(".restart").click(function () {
    $("#steps").html('Ходы - <span id="count">0</span>');
    steps = 0;
    $(".tower").children().each(function () {
        if (!$(this).hasClass("base")) {
            $(this).detach().appendTo("#tower-1");
        }
    });

    $("div[id*=_round]").sort(function (a, b) {
        if (parseInt(a.id) > parseInt(b.id)) {
            return -1;
        } else {
            return 1;
        }
    }).appendTo("#tower-1");
});

$(".info").click(function () {
    var alert = $("#info-alert");
    if (alert.hasClass("info-alert-hidden")) {
        alert.removeClass("info-alert-hidden");
    } else {
        alert.addClass("info-alert-hidden");
    }
});

$(".close").click(function () {
    $("#info-alert").addClass("info-alert-hidden");
});