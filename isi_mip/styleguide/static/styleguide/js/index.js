$(function () {
    $('.widget-styleguide-meta h2').click(function () {
        if ($(this).parent().hasClass('open')) {
            $(this).parent().removeClass('open');
            $(this).next().slideUp();
        } else {
            $(this).parent().addClass('open');
            $(this).next().slideDown();
        }
    });
});
