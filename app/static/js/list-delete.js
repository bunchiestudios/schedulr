
async function delete_item(event){
    let tar = $(event.target);
    var message = `Are you sure you want to delete ${tar.data("name")} and all the related data?`;
    if (!confirm(message)) {
        return;
    }
    let url = null;
    let display = '';
    let reload = false;
    console.log(tar.data("target"));
    switch(tar.data("target")){
        case "users":
            url = `/api/team/${APP.team.id}/kick`;
            display = 'user';
            break;
        case "projects":
            url = "/api/project/delete";
            display = 'project';
            reload = true;
            break;
        case "offdays":
            url = `/api/team/${APP.team.id}/offday/remove`;
            display = 'off-day';
            break;
    }
    if (url === null){
        console.log("Invalid target!");
        return;
    }
    console.log("DELETING: " + tar.data("id"));
    APP.post(
        url,
        {
            item_id: tar.data("id")
        },
        function(data){
            tar.parent().parent().hide();
            APP.toast("Removed " + display + "!");
            if(reload){
                location.reload();
            }
        },
        function (jqXHR, textStatus, errorThrown) {
            APP.toast("Failed to delete " + display + ". :(");
            console.log(textStatus, errorThrown);
        }
    );
}


APP.register_module(function () {
    $('.list-delete').on('click', (event) => {
        delete_item(event);
    });
})
