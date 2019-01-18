

APP.register_module(function(){
    let code = window.location.pathname.split('/').pop();
    console.log(code);
    
    APP.post('/api/user/jointeam',
    {
        join_token: code
    },
    function(data){
        APP.toast("Joined team successfully! Redirecting...");
        APP.redirect_after('/', 1500);
    },
    function( jqXHR, textStatus, errorThrown){
        APP.toast("Failed to join team :(");
        console.log(textStatus, errorThrown);
    })
})