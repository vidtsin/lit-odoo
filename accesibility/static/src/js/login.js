
(function() {
    var logo_login = document.querySelector(".oe_single_form_logo img");
    logo_login.alt = "Logo";
   
    var logo_db_manager = document.querySelector(".oe_single_form_logo img");
    logo_db_manager.alt = "Logo";
   
    var lang = navigator.language;
    if(lang.split('-').length > 1) {
        lang = lang.split('-')[0];
    }
    document.documentElement.lang = lang;
})();
