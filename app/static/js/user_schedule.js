function trim_str(str, size){
    return str.length > size ?
        str.substring(0, size - 3) + "..." : 
        str;
}

async function render_table(year){
    let data = await $.get('/api/me/schedule', data={
        year: 2019
    });
}


APP.register_module(async function(){
    var year = 2019;
    let table_container = $('#schedule-table');
    let data = await $.get('/api/me/schedule', {
        year: year
    });
    var project_names = data.projects.map((item) => trim_str(item.name, 15));
    var week_names = [];
    for (let index = 0; index < data.schedule.length; index++) {
        var week = new Week(year, index + 1);
        week_names.push(`${week.isoWeek()} (${week.month()})`);
    }
    console.log(table_container.height());
    APP.schedule = new Handsontable(table_container[0], {
        data: data.schedule,
        rowHeaders: week_names,
        colHeaders: project_names,
        rowHeaderWidth: 160,
        // height: table_container.height(),
        afterGetRowHeader: (col, TH) => {
            TH.className = 'left';
        },
        afterChange: function(change, source) {
            if(source === 'edit'){
                console.log(change);
                // TODO: send to server
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
});