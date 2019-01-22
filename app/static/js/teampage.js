
function display_join_link(link){
    $('#chip-container').show();
    $('#chip-container .mdl-chip__text').text(link);
    $('#chip-container .material-icons').text('file_copy');
    APP.showModal("Team join link", "Send this link to your coworkers. They must be logged in first!");
    $('#chip-container .material-icons').on('click', ()=>APP.copy_to_clipboard(link));
}

APP.register_module(async function(){
    APP.team = await $.post('/api/me/team').promise();
    $('#get-invite-link').on('click', (event)=>{
        APP.toggle_drawer();
        APP.post(`/api/team/${APP.team.id}/join_token`, null, 
        function(data){
            display_join_link(data.link);
        },
        function(jqXHR, text, error){
            APP.toast("Could not get join link!");
        });
    });
    $('#refresh-code').on('click', (event)=>{
        APP.post(`/api/team/${APP.team.id}/join_token/new`, null, 
        function(data){
            display_join_link(data.link);
        },
        function(jqXHR, text, error){
            APP.toast("Could not get join link!");
        });
    });
});