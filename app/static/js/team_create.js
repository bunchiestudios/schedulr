

APP.register_module(function(){
    $('#create-team-form').on('submit', function(event){
        event.preventDefault();
        console.log('Submit!');

        // TODO: call team create API & redirect to /team on success
    });
})