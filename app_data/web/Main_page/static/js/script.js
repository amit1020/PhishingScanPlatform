$(document).ready(function() {
    // cool nav menu
    $(window).on('load resize', function() {
        var $thisnav = $('.current-menu-item').offset().left;

        $('.menu-item').hover(function() {
            var $left = $(this).offset().left - $thisnav;
            var $width = $(this).outerWidth();
            var $start = 0;
            $('.wee').css({ 'left': $left, 'width': $width });
        }, function() {
            var $initwidth = $('.current-menu-item').width();
            $('.wee').css({ 'left': '0', 'width': $initwidth });
        });
    });

});

document.addEventListener('contextmenu', function(event) {
    event.preventDefault();

});


//Navigatie menu buttons
function Navigation_menu_function(page_name) {
    let page_name;
    switch (page_name) {
        case "Home":
            window.location.href = "http://"
            console.log(button_name);
        case "About":
            window.location.href = "http://"
            console.log(button_name);
        default:
            console.log("Error");
    } //close the switch


} //close the function