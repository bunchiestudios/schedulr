

APP.register_module(function(){
    $('#create-team-form').on('submit', function(event){
        event.preventDefault();
        console.log('Submit!');

        // TODO: call team create API & redirect to /team on success
        APP.post('/api/team', {
            name: $('#team-name-input').val()
        },
        function(data){
            APP.toast("Team created successfully!");
            APP.redirect_after('/team', 2000);
        },
        function( jqXHR, textStatus, errorThrown){
            APP.toast("Failed to create team :(");
            console.log(textStatus, errorThrown);
        })
    });
})