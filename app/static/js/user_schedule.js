var table_data = {
    table: null,
    container: null,
    hot: null,
    project_list: null,
    year: null,
    project_offset: 0,
}

function trim_str(str, size){
    return str.length > size ?
        str.substring(0, size - 3) + "..." : 
        str;
}

async function render_table(){
    $("#schedule-year").text(table_data.year);
    let data = await $.get('/api/me/schedule', {
        year: table_data.year
    });
    table_data.data = data;
    table_data.project_names = data.projects.map((item) => item.name);
    var week_names = [];
    for (let index = 0; index < data.schedule.length; index++) {
        var week = new Week(table_data.year, index + 1);
        var string = `${week.isoWeek()} (${week.month()})`;
        if (week.isCurrent()){
            string = "<b>" + string + "</b>";
        }
        week_names.push(string);
    }
    
    table_data.hot.updateSettings({
        data: data.schedule,
        rowHeaders: week_names,
        colHeaders: table_data.project_names,
        columns: function(index){
            return {
                type: 'numeric',
                allowEmpty: false
            }
        },
    });
    
}

async function send_updates(changes){
    var proj_ids = [];
    var weeks = [];
    var hours = [];
    changes.forEach(change => {
        if(change[2] === change[3]){
            return;
        }
        proj_ids.push(table_data.data.projects[change[1] + table_data.project_offset].id);
        weeks.push(new Week(table_data.year, change[0] + 1 ).isoWeek());
        hours.push(change[3]);
    });
    APP.post(
        '/api/user/register-many',
        {
            project_id: proj_ids,
            iso_week: weeks,
            hours: hours
        },
        function(data){
            console.log(data);
            var errors = false;
            for (const item of data) {
                if(item.hasOwnProperty('success') && !item.success){
                    errors = true;
                }
            }
            if(errors){
                APP.toast("Some Hours failed to be proccessed. Try reloading.");
            }
        },
        function(){
            APP.toast("Failed to update schedule :(  Try reloading.");
        }
    );
}

async function send_update(change){
    if(change[2] === change[3]){
        return;
    }
    var project_id = table_data.data.projects[change[1] + table_data.project_offset].id;
    var week = new Week(table_data.year, change[0] + 1 ).isoWeek();
    APP.post(
        '/api/user/register',
        {
            project_id: project_id,
            iso_week: week,
            hours: change[3]
        },
        function(data){
            console.log(data);
        },
        function(){
            APP.toast("Failed to update schedule :(  Try reloading.");
        }
    );
}

function addProject(project){
    // Verify project is not already in list.
    for (const prev_project of table_data.data.projects) {
        if(project.id === prev_project.id){
            APP.toast("Project already exists!");
            return;
        }
    }
    // Add project to list
    table_data.data.projects.push(project);

    // Add zeros to array, this is the new column
    table_data.data.schedule.forEach(element => {
        element.push(0);
    });

    // Add header (project name)
    table_data.project_names.push(project.name);

    // Render table with new data
    table_data.hot.render();

    // Make sure the new column gets the numeric renderer
    table_data.hot.updateSettings({
        columns: function(index){
            return {
                type: 'numeric',
                allowEmpty: false
            }
        }
    });
}


APP.register_module(async function(){
    APP.team = await $.post('/api/me/team').promise();
    table_data.year = moment().year();
    table_data.container = $('#schedule-table');

    table_data.hot = new Handsontable(table_data.container[0], {
        data: [[]],
        rowHeaderWidth: 160,
        afterGetRowHeader: (col, TH) => {
            TH.className = 'left';
        },
        afterChange: function(changes, source) {
            console.log(source, changes);
            if(source === 'edit' || source === 'Autofill.fill'){
                if(changes.length === 1){
                    send_update(changes[0]);
                }
                else{
                    send_updates(changes);
                }
            }
        },
        cells: function (row, col, prop) {
            var cellProperties = {}
            return cellProperties;
        },
        columns: function(index){
            return {
                type: 'numeric',
                allowEmpty: false
            }
        }
    });

    $("#prev-button").on('click', (event) => {
        event.preventDefault();
        table_data.year--;
        render_table();
    });

    $("#next-button").on('click', (event) => {
        event.preventDefault();
        table_data.year++;
        render_table();
    });

    render_table();
    
    $("#project-name-add").focus(async function(){
        let options = await $.post(`/api/team/${APP.team.id}/projects`);
        console.log(options);
        options = options.map(element => {
            return {
                label: element.name,
                value: element
            }
        });
        console.log(options);
        $("#project-name-add").autocomplete({
            source: options,
            focus: function(event, ui) {
                $("#project-name-add").val( ui.item.label );
                return false;
            },
            select: function(event, ui){
                event.preventDefault();
                $("#project-name-add").val( ui.item.label );
                addProject(ui.item.value);
                return false;
            }
          });
    });

});