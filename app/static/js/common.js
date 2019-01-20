

let APP = {
    modules: [],
    handlers: {
        default_post: (data) => console.log(data),
        post_error: (jqXHR, textStatus, errorThrown) => console.log(textStatus + " " + errorThrown),
    },
    init(){
        this.snackbarContainer = document.querySelector('#page-toast-container');
        this.modules.forEach(element => element());
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