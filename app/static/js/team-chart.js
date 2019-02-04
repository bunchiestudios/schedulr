
var slider1 = $('#team-slider-1 input');
var slider2 = $('#team-slider-2 input');

async function updateChart(start, end){

    var week1 = Week.relative(slider1.val());
    var week2 = Week.relative(Number(slider1.val()) + Number(slider2.val()));
    var data = await $.get('/api/me/team/chart-data', data={
        start_ahead: week1.isoWeek(),
        look_ahead: slider2.val(),
    });
    APP.chart.setData(data);
    $('#team-slider-1 .week').text(`${week1.isoWeek()} (${week1.month()})`);
    $('#team-slider-2 .week').text(`${week2.isoWeek()} (${week2.month()})`);
}

APP.register_module(async function(){
    var start_ahead = 0;
    var look_ahead = 2;
    slider1.val(start_ahead);
    slider2.val(look_ahead);
    var week1 = Week.relative(start_ahead);
    var week2 = Week.relative(start_ahead + look_ahead);
    $('#team-slider-1 .week').text(`${week1.isoWeek()} (${week1.month()})`);
    $('#team-slider-2 .week').text(`${week2.isoWeek()} (${week2.month()})`);
    var data = await $.get('/api/me/team/chart-data', data={
        start_ahead: APP.iso_week(start_ahead),
        look_ahead: look_ahead,
    });
    console.log(data);
    let users = new Set();
    for (const item of data) {
        users.add(item.user);
    }
    $('#bar-chart').css("height", `${users.size * 150}px`);
    APP.chart = new Taucharts.Chart({
        type : 'horizontal-stacked-bar',
        y    : 'user',
        x    : 'hours',
        color: 'project',
        label: 'hours',
        data : data,
        guide: {
            x: {autoScale:false, min:0, max:45}
        },
        plugins: [
            //Taucharts.api.plugins.get('tooltip')(),
            Taucharts.api.plugins.get('legend')(),
            Taucharts.api.plugins.get('crosshair')(),
            Taucharts.api.plugins.get('export-to')(),
            Taucharts.api.plugins.get('floating-axes')(),
        ]
    });
    APP.chart.renderTo('#bar-chart');

    slider1.on('input', async function(event){
        updateChart();
    });

    slider2.on('input', async function(event){
        updateChart();
    });
});