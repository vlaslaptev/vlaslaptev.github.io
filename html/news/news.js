function loadNews() {
    for (var i = 0; i < news_list.length; i++) {
        $(".news-items").append($("<div>").load("html/news/" + news_list[i] + ".html")).append("<hr>");
    }
    $(".nav-page").on("click", pageLinkClick);
}

loadNews();