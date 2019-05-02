
var FORM = {
    fullday: true,
    selector: null,
    checkbox: null,
    dayoff_label: null,
    submit: null,
}

function submit(){
    let date = FORM.selector.val();
    if (date.isEmpty()) {
        APP.toast("Date field is empty!");
        return;
    }
    let hours = FORM.fullday ? 8 : 4;

    APP.post(
        `/api/team/${APP.team.id}/offday/add`,
        {
            date: date,
            hours: hours
        },
        function (data) {
            APP.toast(`Added ${date}`);
            location.reload();
        },
        function (jqXHR, textStatus, errorThrown) {
            APP.toast(`Failed to add ${date} :(`);
            console.log(textStatus, errorThrown);
        }
    )
}


APP.register_module(function () {
    FORM.selector = $("#date");
    FORM.checkbox = $("#fullday");
    FORM.dayoff_label = $("#fulldaylabel");
    FORM.submit = $("#submit-offday");
    FORM.checkbox.on('click', (event) => {
        FORM.fullday = !FORM.fullday;
        FORM.dayoff_label.text(FORM.fullday? "Full day": "Half day");
    });

    FORM.submit.on('click', (event)=>{submit()});
})