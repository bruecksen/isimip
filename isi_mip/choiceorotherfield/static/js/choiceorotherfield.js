(function($) {
    $(function() {
        $('.choiceorotherfield').each(function () {
            var choiceorotherfield = $(this);
            choiceorotherfield.find('input[type=radio]').not(":last").change(function () {
                // regular Radio Button
                if (!$(this).is(':checked')) return;
                choiceorotherfield.find('input[type=text]').addClass("choiceorotherfield-disabled");
            });

            choiceorotherfield.find('input[type=radio]').last().change(function () {
                // last Radio Button
                if (!$(this).is(':checked')) return;
                choiceorotherfield.find('input[type=text]').removeClass("choiceorotherfield-disabled");
            });

            choiceorotherfield.find('input[type=text]').focus(function () {
                choiceorotherfield.find('input[type=radio]').last().prop("checked", true);
                $(this).removeClass("choiceorotherfield-disabled");
            });

            choiceorotherfield.find('input[type=text]').on('propertychange change click keyup input paste', function () {
                choiceorotherfield.find('input[type=radio]').last().val($(this).val());
            });

            // trigger initialization
            choiceorotherfield.find('input[type=radio]').change();
        });
    });
}(django.jQuery));
