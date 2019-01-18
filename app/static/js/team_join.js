

APP.register_module(function(){
    let code = window.location.pathname.split('/').pop();
    console.log(code);
    
    APP.post('/api/user/jointeam',
    {
        code: code
    },
    function(data){
        console.log("Ok");
    },
    function( jqXHR, textStatus, errorThrown){
        APP.toast("Failed to join team :(");
        console.log(textStatus, errorThrown);
    })
})