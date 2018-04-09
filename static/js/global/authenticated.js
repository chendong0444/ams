$(document).ready(function(){
    if ($("#id_allow_anonymous_view").length > 0) {
        if ($("#id_allow_anonymous_view:checked").length == 1) {
            $('fieldset.permissions .form-group:not(fieldset.permissions .form-group:first)').hide();

            if($('fieldset.permissions > .form-group').length > 1) {
                $('fieldset.permissions .form-group:first').append('<a id="adv-perms" href="#id_allow_anonymous_view">+ </a>');
            }
        } else {
            if($('fieldset.permissions > .form-group').length > 1) {
                $('fieldset.permissions .form-group:first').append('<a id="adv-perms" href="#id_allow_anonymous_view">- </a>');
            }
        }
        $('#adv-perms').click(function() {
            $('fieldset.permissions .form-group:not(fieldset.permissions .form-group:first)').slideToggle('fast');
             if ($('#adv-perms').text() == '- ') {
                $('#adv-perms').text('+ ');}
            else {$('#adv-perms').text('- ');}
        });
        $('#id_allow_anonymous_view').click(function() {
            if ($("#id_allow_anonymous_view:checked").length == 1) {
                $('fieldset.permissions .form-group:not(fieldset.permissions .form-group:first)').slideUp('fast');
                $('#adv-perms').text('+ ');
            } else {
                $('fieldset.permissions .form-group:not(fieldset.permissions .form-group:first)').slideDown('fast');
                $('#adv-perms').text('- ');
            }
        });
    }

    $("#admin-bar ul li").has(".sub").not('#themecolor').hover(function(){
        $(this).children(".sub").addClass('active');
    }, function() {
        $(this).children(".sub").removeClass('active');
    });
    $("#user-bar li").has(".sub").hover(function(){
        $(this).children(".sub").addClass('active');
    }, function() {
        $(this).children(".sub").removeClass('active');
    });

});
