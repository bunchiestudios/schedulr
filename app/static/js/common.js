String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};

let APP = {
    modules: [],
    handlers: {
        default_post: (data) => console.log(data),
        post_error: (jqXHR, textStatus, errorThrown) => console.log(jqXHR.responseText + " " + textStatus + " " + errorThrown),
    },
    init(){
        // Setup snackbar
        this.snackbarContainer = document.querySelector('#page-toast-container'),

        // Setup modal
        this.modal = {
            modal: $('#modal'),
            close: $('#modal-close'),
        };
        this.modal.close.on('click', (event)=>{
            event.preventDefault();
            APP.hideModal();
        });

        // Call modules
        this.modules.forEach(element => element());
    },
    showModal(title, text, onClose=null){
        this.modal.modal.find('.mdl-card__title-text').text(title);
        this.modal.modal.find('.mdl-card__supporting-text').text(text);
        this.modal.modal.show();
        $(window).on('click', (event)=>{
            event.preventDefault();
            if(event.target === this.modal.modal[0]){
                this.hideModal();
                $(window).off('click');
                if(onClose !== null){
                    onClose();
                }
            }
        });
    },
    hideModal(event){
        this.modal.modal.hide();
        this.modal.modal.find('.mdl-card__title-text').text('');
        this.modal.modal.find('.mdl-card__supporting-text').text('');
    },
    redirect(url){
        window.location.replace(url);
    },
    redirect_after(url, miliseconds){
        setTimeout(()=> {APP.redirect(url);}, miliseconds)
    },
    toast(text){
        this.snackbarContainer.MaterialSnackbar.showSnackbar({message: text});
    },
    register_module(callback){
        this.modules.push(callback);
    },
    post(url, data=null, success=APP.handlers.default_post, fail=APP.handlers.post_error){
        $.ajax(url, {
            type: 'POST',
            dataType: "json",
	        contentType: "application/json",
            data: JSON.stringify(data),
            success: success,
            error: fail
        });
    },
    get(url, data=null, success=APP.handlers.default_post, fail=APP.handlers.post_error){
        $.ajax({
            url: url, 
            data: data,
            success: success, 
            error: fail
        });
    },
    toggle_drawer(){
        $('.mdl-layout')[0].MaterialLayout.toggleDrawer();
    },
    copy_to_clipboard(text) {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(text).select();
        try{
            document.execCommand("copy");
            APP.toast("Copied!");
        }catch(e){

        }
        $temp.remove();
    },
    iso_week(offset){
        return new Week(offset).isoWeek();
    }
};

$(document).ready(function() {
    APP.init();
    $('#logout').on('click', (event)=>{
        event.preventDefault();
        $.ajax({
            url: "/auth/logout",
            type: 'POST',
            success: (data) =>{
                APP.toast("You've logged out!")
                APP.redirect_after('/', 2000);
            },
            error: (jqXHR, textStatus, errorThrown) => {
                console.log("Log out error: " + textStatus);
                APP.redirect('/');
            }
        });
    })
});

class Week{
    constructor(offset=0){
        this.moment = moment().startOf('isoWeek').add(offset, 'w');
    }
    isoWeek(){
        return this.moment.format('YYYY-[W]WW');
    }
    month(){
        return this.moment.startOf('isoWeek').add(3, 'days').format("MMMM");
    }
}