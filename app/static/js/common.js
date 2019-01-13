

let APP = {
    init: function(){
        this.snackbarContainer = document.querySelector('#page-toast-container');
    },
    redirect: function(url){
        window.location.replace(url);
    },
    toast: function(text){
        this.snackbarContainer.MaterialSnackbar.showSnackbar({message: text});
    }
};

$(document).ready(function() {
    $('#logout').on('click', ()=>{
        $.ajax({
            url: "/auth/logout",
            type: 'POST',
            success: (data) =>{
                APP.toast("You've logged out!")
                setTimeout(()=> {APP.redirect('/');}, 2000)
            },
            error: (jqXHR, textStatus, errorThrown) => {
                console.log("Log out error: " + textStatus);
                APP.redirect('/');
            }
        });
    })
});