$(".nav a").on("click", function(e){
	e.preventDefault();
	e.stopPropagation();
	$(".nav").find(".active").removeClass("active");
	$(this).parent().addClass("active");

	$(".content").load($(this).href);
});

