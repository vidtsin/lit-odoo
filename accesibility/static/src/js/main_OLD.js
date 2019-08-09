/*  Engine that executes accesibility rules that are subscribed and it finish after 10 secs.
    For each click event in a button or link, it starts and stops later again.
*/
var AccesibilityEngine = {
    tasks: [],
    timer: {},
    subscribe: function(task){
        this.tasks.push(task);
    },
    start: function(){
        this.timer = setInterval(function(){
            for(var i=0; i<this.tasks.length; i++){
                this.tasks[i]();
            }
            $("a, button").click(function(){
                acc.stop();
                acc.start();
            });
        }.bind(this), 100);
        setTimeout(function(){this.stop();}.bind(this), 10000);
    },
    stop: function(){
        if(this.timer)
            clearInterval(this.timer);
    }
}

/* RULES TO BE SUBSCRIBED */
function addLabels() {
    var createLabel = function(input){
        var label = document.createElement("label");
        label.htmlFor = input.id;
        if(input.id.startsWith("dp")){
            var span = document.createElement("span");
            span.innerHTML = input.placeholder ? input.placeholder : "Campo de formulario";
            span.className = "acc_filling";
            label.appendChild(span);
        } else
            label.innerHTML = input.placeholder ? input.placeholder : "Campo de formulario";
        var parent = input.parentNode;
        parent.removeChild(input);
        label.appendChild(input);
        parent.appendChild(label);
    };
    
    var removeLabel = function(input){
        var grandParent = input.parentNode.parentNode;
        var label = input.parentNode;
        label.removeChild(input);
        grandParent.removeChild(label);
        grandParent.appendChild(input);
    };
    
    var inputs = document.querySelectorAll("input, textarea, select");
    var labels = document.querySelectorAll("label");
    var emptys = [];
    
    // Restore old empty ids
    forEach(inputs, function(input){
        var id = input.id;
        if(id){
            if(id.split("-")[0] == "acc_input_empty"){
                input.id = "";
                removeLabel(input);
            }
        }
    });
    
    for(var i=0; i<inputs.length; i++){
        var input = inputs[i];
        if(!input.id){
            if(input.parentNode.nodeName != "LABEL"){
                emptys.push(input);
                input.id = "acc_input_empty-" + i;
            }
        } else if(!function(id){
            for(var k=0; k<labels.length; k++){
                if(labels[k].htmlFor == id)
                    return true;
            }
            return false;
        }(input.id)) {
            if(input.parentNode.nodeName != "LABEL"){
                createLabel(input);
            }
        }
    }
    for(var i=0; i<emptys.length; i++){
        if(emptys[i].parentNode.nodeName != "LABEL"){
                createLabel(emptys[i]);
            }
    }
}

function addContentToTableHeader(){
    var ths = document.querySelectorAll("th.oe_list_record_delete");
    forEach(ths, function(th){
        th.innerHTML = "Eliminar";
    });
}

// When there're two labels with their input repeated in the notification dropdown of IM
function removeDuplicatedLabelsInIMActions(){
    var inputs = document.querySelectorAll(".oe_subtype td input");
    forEach(inputs, function(input){
        var count = 0;
        forEach(inputs, function(el){
            if(el.parentNode.parentNode.parentNode.parentNode.parentNode
                && el.id == input.id){
                count++;
            }
        });
        if(count == 2){
            var table = input.parentNode.parentNode.parentNode.parentNode;
            table.parentNode.removeChild(table);
        }
    });
}

function altForKanbanBottomRight(){
    var imgs = document.querySelectorAll(".oe_kanban_bottom_right img")
    forEach(imgs, function(img){
       img.alt = "Imagen de tarjeta."; 
    });
}

function altForKanbanAvatar(){
    var imgs = document.querySelectorAll(".oe_kanban_avatar img")
    forEach(imgs, function(img){
       img.alt = "Imagen de avatar."; 
    });
}

function fillLinksKanbanColorPicker(){
    var links = document.querySelectorAll(".oe_kanban_colorpicker a")
    forEach(links, function(link){
        var span = document.createElement("span");
        span.innerHTML = "Color";
        span.className = "acc_filling";
        link.appendChild(span); 
    });
}

function altForFormImage() {
    var img = document.querySelector(".oe_form_field_image > img")
    if(img) {
        img.alt = "Imagen de entidad.";
    }
}

function altForTranslatableImage() {
    var imgs = document.querySelectorAll("img.oe_field_translate")
    forEach(imgs, function(img){
       img.alt = "Icono campo traducible."
    });
}

function iframeTitles() {
    var els = document.querySelectorAll("iframe, frame");
    forEach(els, function(el){
        if(!el.title){
            el.title = "Contenedor web.";
        }
    });
}

function setAltForEmailTemplateSaveImg() {
    var img = document.querySelector("tr.oe_form_group_row > td.oe_form_group_cell > button.oe_form_button img");
    if (img) {
        img.alt = "Guardar plantilla de correo.";
    }
}

function setAltForNIFConfirmationImg(){
    var img = document.querySelector("div[name='vat_info'] > button > img");
    if(img){
        img.alt = "Confirmar validez de NIF.";
    }
}

function setAltForExecuteImg(){
    // var imageTag = $("img[src='gtk-execute.png']");
    var imgs = document.querySelectorAll("button > img[src$='gtk-execute.png']");
    forEach(imgs, function(img){
        img.alt = "Ejecutar.";
    });

    var img0s = document.querySelectorAll("button > img[src$='gtk-save.png']");
    forEach(img0s, function(img0){
        img0.alt = "Guardar.";
    });

    var img1s = document.querySelectorAll("button > img[src$='STOCK_DIRECTORY.png']");
    forEach(img1s, function(img1){
        img1.alt = "Directorio.";
    });

    var img2s = document.querySelectorAll("button > img[src$='STOCK_MISSING_IMAGE.png']");
    forEach(img2s, function(img2){
        img2.alt = "Limpiar.";
    });

    var imgps = document.querySelectorAll("img[src$='print.png']");
    forEach(imgps, function(imgp){
        imgp.alt = "Imprimir.";
    });


}

function setAltForSegmentationCalculation(){
    var img = document.querySelector("div.oe_form_nosheet > header > button > img");
    if(img) {
        img.alt = "Calcular segmentación.";
    }
}

function setAltForSellerImg() {
    var img = document.querySelector("div.oe_form_sheetbg > div.oe_form_sheet > span.oe_avatar > img[name='image']");
    if(img) {
        img.alt = "Imagen del proveedor.";
    }
}

function setAltForAlbaranScanImg() {
    // var imgs = document.querySelectorAll("button.oe_stock_scan_button > img.oe_stock_scan_image");
    var imgs = document.querySelectorAll("button > img.oe_stock_scan_image_btn"); 
    for(var i=0; i<imgs.length; i++){
        if(imgs[i]) {
            imgs[i].alt = "Escanear albarán.";
        }
    }
 
    var buts = document.getElementsByClassName("button.oe_stock_scan_image_btn");
    for(var j=0; j<buts.length; j++){
        if(buts[j]) {
            buts[j].setAttribute('aria-label', 'Scan');
        }
    }
}

function setUserScalableForTPVViewport(){
    var tag = document.querySelector("meta[name='viewport']");
    if(tag){
        tag.content = "width=1024";
    }
}

function addCellsToMatchTableHeaders(){
    var theads = document.querySelectorAll("table > thead");
    forEach(theads, function(thead){
        var table = thead.parentNode;
        // Check if it has tbody with datas or empty.
        var tbody = table.getElementsByTagName("tbody");
        if(tbody.length == 1) {
            tbody = tbody[0];
        }
        
        if(tbody.childElementCount > 0){
            var tr = tbody.getElementsByTagName("tr");
            if(tr.length > 0)
                tr = tr[0];
            if(tr.childElementCount > 0){
                    var tds = tr.getElementsByTagName("td");
                    for(var i=0; i<tds.length; i++){
                        var td = tds[i];
                        var node;
                        if(td.getElementsByTagName("input").length > 0)
                            continue;
                        if(td.childNodes.length > 0)
                            node = td.childNodes[0];
                        if(td.childNodes.length == 0 || (td.childNodes.length == 1 && node && node.nodeName == "#text" && node.nodeValue == false)){
                            td.innerHTML = "Sin valor";
                        }
                    }                
            }
        }
    });
}

function addAltForScrapImageButton(){
    var imgs = document.getElementsByTagName("img");
    forEach(imgs, function(img){
       if(img.src.indexOf("terp-gtk-jump-to-ltr") !== -1){
           img.alt = "Desecho";
           return;
       }
    });
}

function addAltForPos(){
    var posLogo = document.querySelector("img.pos-logo");
    if(posLogo && !posLogo.alt) {
        posLogo.alt = "Imagen de logo del terminal punto de venta."
    }
    var home = document.querySelector("img.breadcrumb-homeimg");
    if(home && !home.alt) {
        home.alt = "Volver a categoría padre."
    }
    var back = document.querySelector(".numpad-backspace img");
    if(back && !back.alt){
        back.alt = "Borrar caracter.";
    }
    
    var products = document.querySelectorAll(".product-list img");
    forEach(products, function(product){
       product.alt = "Imagen de producto."; 
    });
}

function changeTHtoTDinBodyRow(){
    var ths = document.querySelectorAll("table.oe_list_content > tbody > tr > th");
    forEach(ths, function(th){
        var parent = th.parentNode;
        var td = document.createElement("td");
        td.className = th.className;
        td.id = th.id;
        td.innerHTML = th.innerHTML;
        parent.replaceChild(td, th);
    });
}

function addAriaLabelsForCheckboxes(){
    var theads = document.querySelectorAll("table > thead");
    if(theads.length > 0){
        var thead = theads[theads.length - 1];
        if(!thead) return;
        var input = thead.querySelector("tr > th > label > input");
        if(!input) return;
        var id = input.id;
        var checkboxes = document.querySelectorAll("input[name='radiogroup']");
        forEach(checkboxes, function(ck){
            ck.setAttribute('aria-labelledby', id);
        });
    }
}

function setUniqueMenuCounters(){
    var divs = document.getElementsByTagName("div");
    forEach(divs, function(div){
       if(div.id.split("-")[0] == "menu_counter"){
            div.id = "menu_counter";
        } 
    });
    var menus = document.querySelectorAll("#menu_counter");
    for(var i=0; i<menus.length; i++){
        menus[i].id = "menu_counter-" + (i+1);
    }
}

function setUniqueSearchViewCustomInputID(){
    var inputs = document.getElementsByTagName("input");
    forEach(inputs, function(input){
       if(input.id.split("-")[0] == "oe_searchview_custom_input"){
            input.id = "oe_searchview_custom_input";
            var labels = input.parentNode.getElementsByTagName("label");
            if(labels.length > 0){
                labels[0].setAttribute("for", "");
            }
        } 
    });
    var searchViews = document.querySelectorAll("#oe_searchview_custom_input");
    for(var i=0; i<searchViews.length; i++){
        searchViews[i].id = "oe_searchview_custom_input-" + (i+1);
        var labels = searchViews[i].parentNode.getElementsByTagName("label");
        if(labels.length > 0){
            labels[0].setAttribute("for", "oe_searchview_custom_input-" + (i+1));
        }
    }
}

function setUniqueSearchViewCustomPublicID(){
    var inputs = document.getElementsByTagName("input");
    forEach(inputs, function(input){
       if(input.id.split("-")[0] == "oe_searchview_custom_public"){
            input.id = "oe_searchview_custom_public";
            var labels = input.parentNode.getElementsByTagName("label");
            if(labels.length > 0){
                labels[0].setAttribute("for", "");
            }
        } 
    });
    var searchViews = document.querySelectorAll("#oe_searchview_custom_public");
    for(var i=0; i<searchViews.length; i++){
        searchViews[i].id = "oe_searchview_custom_public-" + (i+1);
        var labels = searchViews[i].parentNode.getElementsByTagName("label");
        if(labels.length > 0){
            labels[0].setAttribute("for", "oe_searchview_custom_public-" + (i+1));
        }
    }
}

function setUniqueSearchViewCustomDefaultID(){
    var labels;
    var inputs = document.getElementsByTagName("input");
    for(var j=0; j<inputs.length; j++){
       if(inputs[j].id.split("-")[0] == "oe_searchview_custom_default"){
            inputs[j].id = "oe_searchview_custom_default";
            labels = inputs[j].parentNode.getElementsByTagName("label");
            if(labels.length > 0){
                labels[0].setAttribute("for", "");
            }
        } 
    }
    var searchViews = document.querySelectorAll("#oe_searchview_custom_default");
    for(var k=0; k<searchViews.length; k++){
        searchViews[k].id = "oe_searchview_custom_default-" + (k+1);
        labels = searchViews[k].parentNode.getElementsByTagName("label");
        if(labels.length > 0){
            labels[0].setAttribute("for", "oe_searchview_custom_default-" + (k+1));
        }
    }
}

/* -- END OF ACCESIBILITY RULES -- */

var acc = AccesibilityEngine;
acc.subscribe(addLabels);
acc.subscribe(addContentToTableHeader);
acc.subscribe(removeDuplicatedLabelsInIMActions);
acc.subscribe(altForKanbanBottomRight);
acc.subscribe(altForKanbanAvatar);
acc.subscribe(fillLinksKanbanColorPicker);
acc.subscribe(altForFormImage);
acc.subscribe(altForTranslatableImage);
acc.subscribe(iframeTitles);
acc.subscribe(setAltForEmailTemplateSaveImg);
acc.subscribe(setAltForNIFConfirmationImg);
acc.subscribe(setAltForExecuteImg);
acc.subscribe(setAltForSegmentationCalculation);
acc.subscribe(setAltForSellerImg);
acc.subscribe(setAltForAlbaranScanImg);
acc.subscribe(setUserScalableForTPVViewport);
// acc.subscribe(addCellsToMatchTableHeaders);
acc.subscribe(addAltForScrapImageButton);
acc.subscribe(addAltForPos);
acc.subscribe(changeTHtoTDinBodyRow);
acc.subscribe(addAriaLabelsForCheckboxes);
acc.subscribe(setUniqueMenuCounters);
acc.subscribe(setUniqueSearchViewCustomInputID);
acc.subscribe(setUniqueSearchViewCustomPublicID);
acc.subscribe(setUniqueSearchViewCustomDefaultID);

acc.start();

/* Module for accesibility changes in the DOM */
openerp.accesibility = function(instance){
    $('document').ready(function(){
        var lang = navigator.language;
        if(lang.split('-').length > 1) {
            lang = lang.split('-')[0];
        }
        document.documentElement.lang = lang;
    
        var logo = document.querySelector(".oe_logo img");
        if(logo && !logo.alt)
            logo.alt = "Logo de compañía";
        var header = document.getElementsByClassName("oe_view_title");    
        
        // empty button fix
        var button = document.querySelector("nav div button.navbar-toggle");
        if(!button)
            return;
        var span = document.createElement("span");
        span.class = "acc_filling_opt";
        span.innerHTML = "Botón sin texto";
        button.appendChild(span);
    });
    
    instance.web.UserMenu =  instance.web.UserMenu.extend({
        do_update: function () {
            var self = this;
            var fct = function() {
                var $avatar = self.$el.find('.oe_topbar_avatar');
                $avatar.attr('alt', 'Avatar de usuario.');
            };
            self._super();
            this.update_promise = this.update_promise.then(fct, fct);
        }
    });

    instance.web.ViewManager.include({
        start: function() {
            this._super();            
            
            var h1 = document.createElement('h1');
            var h2 = document.getElementsByClassName("oe_view_title")[0];
            if(h2) {
                var parent = h2.parentNode;
                h1.className = h2.className;
                h1.innerHTML = h2.innerHTML;
                parent.replaceChild(h1, h2);
            }
        },
    });
    
    if(instance.mail) {
        instance.mail.Wall.include({
            start: function() {
                this._super();            
                var h1 = document.createElement('h1');
                var h2 = document.getElementsByClassName("oe_view_title")[0];
                if(h2) {
                    var parent = h2.parentNode;
                    h1.className = h2.className;
                    h1.innerHTML = h2.innerHTML;
                    parent.replaceChild(h1, h2);
                }
            },
        });
    }
    
    instance.web_kanban.KanbanGroup.include({
        compute_cards_auto_height: function() {
            this._super();
                    
            var imgs_kanban = document.getElementsByClassName("oe_kanban_image");
            for(var i=0; i<imgs_kanban.length; i++) {
                imgs_kanban[i].alt = "Imagen de tarjeta resumen.";
            }
            var img_form = document.querySelector(".oe_form_sheet img");
            if(img_form) {
                img_form.alt = "Imagen de formulario.";
            }
        },
    });
    
    if(instance.im_chat) {
        instance.im_chat.UserWidget.include({
            update_status: function(){
                this._super();
                var img_user_avatar = document.getElementsByClassName("oe_im_user_avatar");
                for(var i=0; i<img_user_avatar.length; i++) {
                    img_user_avatar[i].alt = "Avatar del chat de usuario.";
                }
                
                var img_user_online = document.getElementsByClassName("oe_im_user_online");
                for(var i=0; i<img_user_online.length; i++) {
                    img_user_online[i].alt = "Usuario conectado.";
                }
            },
        });   
    }
    
    // Empty table header
    instance.web.ListView.List.include({
        // Override delegate method to apply on <td> instead <th>
        init: function (group, opts) {
            var self = this;
            this._super(group, opts);
            this.$current
            .delegate('td.oe_list_record_selector', 'click', function (e) {
                e.stopPropagation();
                var selection = self.get_selection();
                var checked = $(e.currentTarget).find('input').prop('checked');
                $(self).trigger(
                        'selected', [selection.ids, selection.records, ! checked]);
            });
        },
        pad_table_to: function(count){
            this._super(count);
            for(var i=0; i<this.$current[0].children.length; i++){
                if(this.$current[0].children[i].children[0].nodeName == "TH"){
                    var str = '<td class="oe_list_record_selector"></td>'
                        , parser = new DOMParser()
                        , td = parser.parseFromString(str, "text/xml").childNodes[0];
                    if(!this.$current[0].children[i].children[0].children.length){
                        var parent = this.$current[0].children[i].children[0].parentNode;
                        var toRemove = this.$current[0].children[i].children[0];
                        parent.replaceChild(td, toRemove);
                    }
                }
            }
           
            var buttons = this.$current.find(".oe_list_record_delete button");
 
            buttons.each(function(){ 
                var span = document.createElement('span')
                span.innerHTML = 'Borrar';
                span.style.fontFamily = 'Lato, Helvetica, sans-serif';
                span.style.fontSize = '16px'
                span.class = "acc_filling_opt";
                this.append(span);
            });
        
            
        }
    });
    
    // empty link announcement bar
    instance.web.WebClient.include({
        show_annoucement_bar: function() {
            try {
                var r = this._super();
                var link = this.$el.find(".url a");
                link.html("Enlace vacío");
                link.addClass("acc_filling");
                return r;
            }
            catch(e){
            }
        }
    });
    
    instance.web.FormView.include({
       load_record: function(record){
           var r = this._super(record);
           var links = document.querySelectorAll("span.oe_form_field a.oe_form_uri");
           for(var i=0; i<links.length; i++){
               var span = document.createElement("span");
               span.className = "acc_filling";
               span.appendChild(document.createTextNode("Enlace sin contenido"));
               links[i].appendChild(span);
           }
	   var img = document.querySelector("span.oe_form_field_image img");
	   if(img)
	       img.alt = "Imagen de entidad.";
           return r;
       } 
    });
    
    instance.web.DateTimeWidget.include({
        start: function(){
            this._super();
            var id;
            var label = this.$el[0].parentElement.parentElement.parentElement.querySelector("label");
            if(label){
                id = label.htmlFor;
            }
            this.$el.find("input")[1].id = id;
        }
    });
}

