function rand(max){
    return Math.round(Math.random() * max);
}

function rand_pick(n) {
    return Math.min(Math.floor(Math.random() * n, n - 1));
  }

function getData(){
    var employees = [];
    for (let index = 0; index < rand(10)+5; index++) {
        employees.push(`Employee ${index+1}`);
    }
    var projects = [];
    for (let index = 0; index < rand(30)+5; index++) {
        projects.push(`Project ${index+1}`);
    }
    var data = [];
    for (const employee of employees) {
        for (let index = 0; index < 10; index++) {
            data.push({
                employee: employee,
                project: projects[rand_pick(projects.length)],
                hours: rand(10),
                week: index
            });
        }
    }
    var map = {};
    data.forEach((point)=>{
        var key = point.employee + point.project;
        if (!map.hasOwnProperty(key)) {
            map[key] = {
                employee: point.employee,
                project: point.project,
                hours: []
            }
        };
        map[key].hours.push(point.hours);
    });
    var result = [];
    for (const key in map) {
        if (map.hasOwnProperty(key)) {
            var avg = map[key].hours.reduce((acc, val) => acc+val, 0)/map[key].hours.length;
            result.push({
                employee: map[key].employee,
                project: map[key].project,
                hours: Math.round(avg*10)/10
            });
        }
    }
    console.log(result);
    return result;
}

APP.register_module(function(){
    APP.chart = new Taucharts.Chart({
        type : 'horizontal-stacked-bar',
        y    : 'employee',
        x    : 'hours',
        color: 'project',
        label: 'hours',
        data : getData(),
        plugins: [
            Taucharts.api.plugins.get('tooltip')(),
            Taucharts.api.plugins.get('legend')(),
            Taucharts.api.plugins.get('crosshair')(),
            Taucharts.api.plugins.get('export-to')(),
            Taucharts.api.plugins.get('floating-axes')(),
        ]
    });
    APP.chart.renderTo('#bar-chart');
});