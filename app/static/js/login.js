

APP.register_module(function(){
    $('#msft-login').on('click', (event) => {
        event.preventDefault();
        APP.redirect($('#msft-login').attr('redirect'));
    });
    $('#google-login').on('click', (event) => {
        event.preventDefault();
        APP.redirect($('#google-login').attr('redirect'));
    });
});