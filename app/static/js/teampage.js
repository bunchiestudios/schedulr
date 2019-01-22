function clear_modal(){
    $('#project-list').hide();
    $('#chip-container').hide();
}

function display_join_link(link){
    clear_modal();
    $('#chip-container').show();
    $('#chip-container .mdl-chip__text').text(link);
    $('#chip-container .material-icons').text('file_copy');
    $('#chip-container .material-icons').on('click', ()=>APP.copy_to_clipboard(link));
    APP.showModal(
        "Team join link", 
        "Send this link to your coworkers. They must be logged in first!",
        ()=>{
            $('#chip-container').hide();
        }
    );
}

function project_request_delete(project_id, project_name){
    var message = `Are you sure you want to delete ${project_name} and all its related data?`;
    if(confirm(message)){
        console.log("DELETING");
    }
}

async function list_projects(){
    clear_modal();
    var list_container = $('#project-list');
    var list_element = $('#project-list .mdl-list');
    APP.team.projects = await $.post(`/api/team/${APP.team.id}/projects`).promise();
    list_container.show();
    APP.showModal(
        `Projects in ${APP.team.name}`,
        "",
        () => {
            console.log('HIDING');
            list_container.hide();
        }
    );
    list_element.empty();
    APP.team.projects.forEach(async function(project_id){
        var project = await $.post(`/api/project/${project_id}`).promise();
        var delbutton = `<a class="mdl-list__item-secondary-action pointer" onclick="project_request_delete(${project.id}, '${project.name}')"><i class="material-icons">delete</i></a>`;

        var element = $(`
        <div class="mdl-list__item">
            <span class="mdl-list__item-primary-content">
                <i class="material-icons mdl-list__item-avatar">group_work</i>
                <span id="project-name"></span>
            </span>
            ${APP.team.user_is_owner ? delbutton : ''}
        </div>
        `);
        element.find('#project-name').text(project.name);
        list_element.append(element);
    });
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
    $('#view-projects').on('click', async (event)=>{
        console.log('WOOp');
        APP.toggle_drawer();
        list_projects();
    });

    $('#add-project-button').on('click', (event) => {
        event.preventDefault();
        var name = prompt("Provide project name:");
        console.log(name);
        if (name !== null && !name.isEmpty()){
            APP.post(
                '/api/project',
                {
                    name: name,
                    team_id: APP.team.id
                },
                (data) => {
                    APP.toast("Project created!");
                    list_projects();
                },
                () => {
                    APP.toast("Failed to create project.");
                }
            )
        }
    });
});