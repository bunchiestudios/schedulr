

APP.register_module(function(){
    $('#create-team-form').on('submit', function(event){
        event.preventDefault();

        APP.post('/api/team', {
            name: $('#team-name-input').val()
        },
        function(data){
            APP.toast("Team created successfully!");
            APP.redirect_after('/team', 500);
        },
        function( jqXHR, textStatus, errorThrown){
            APP.toast("Failed to create team :(");
            console.log(textStatus, errorThrown);
        })
    });
});