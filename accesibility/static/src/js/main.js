/*  Engine that executes accesibility rules that are subscribed and it finish after 10 secs.
    For each click event in a button or link, it starts and stops later again.
*/
var AccesibilityEngine = {
    tasks: [],
    subscribe: function(task){
        this.tasks.push(task);
    },
    start: function(){
        var timer = setInterval(function(){
                for(var i=0; i<this.tasks.length; i++){
                    this.tasks[i]();
                }
                $("a, button").unbind("click.acc").on("click.acc", function(){
                    acc.stop(timer);
                    acc.start();
                });
                
            }.bind(this), 100);
        setTimeout(function(){
            this.stop(timer);
        }.bind(this), 10000);
    },
    stop: function(timer){
        if(timer)
            clearInterval(timer);
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
               // removeLabel(input);
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

function addContentToTeamAction(){
    var ths = document.querySelectorAll("a.oe_sparkline_bar_link.oe_kanban_action.oe_kanban_action_a");
    forEach(ths, function(th){
        th.innerHTML = "Progreso";
    });

    var oths = document.querySelectorAll("oe_salesteams_opportunities.a.oe_sparkline_bar_link.oe_kanban_action.oe_kanban_action_a");
    forEach(oths, function(oth){
        oth.innerHTML = "Opport.";
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


function rewriteIdForGauge(){
    var imgs = document.querySelectorAll(".oe_gauge filter")
    i = 1;
    forEach(imgs, function(img){
       img.id = img.id+i; 
       i += 1;
    });
}

function rewriteIdForDatepicker(){
    var imgs = document.querySelectorAll(".oe_datepicker_master")
    i = 1;
    forEach(imgs, function(img){
       img.id = img.id+i; 
       i += 1;
    });
}


function altForKanbanBottomRight(){
    var imgs = document.querySelectorAll(".oe_kanban_bottom_right img")
    forEach(imgs, function(img){
       img.alt = "Imagen de tarjeta."; 
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

function altForSalesteamsImage() {
    var imgs = document.querySelectorAll("img.oe_kanban_salesteams_avatars")
    forEach(imgs, function(img){
       img.alt = "Icono equipo ventas."
    });
}

function altForKanbanAvatar() {
    var imgs = document.querySelectorAll("img.oe_kanban_avatar.pull-right")
    forEach(imgs, function(img){
       img.alt = "Icono usuario."
    });
}

function altForOppButton() {
    var imgs = document.querySelectorAll(".oe_button.oe_form_button.oe_inline")
    forEach(imgs, function(img){
       img.alt = "Botón acción."
    });
}

function altForSearchButton() {
    var imgs = document.querySelectorAll(".oe_list_field_cell.oe_list_field_object.oe_button")
    forEach(imgs, function(img){
       img.alt = "Botón buscar."
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
        if(!id){
            var el = document.getElementById("acc_label_ck");
            if(el)
                el.id = "";
            id = "acc_label_ck";
            input.id = id;
        }
        var checkboxes = document.querySelectorAll("input[name='radiogroup']");
        forEach(checkboxes, function(ck){
            ck.setAttribute('aria-labelledby', id);
        });
    }
}

function addAriaLabelsForBodyCheckboxes(){
    var theads = document.querySelectorAll("table > tbody > tr > td");
    if(theads.length > 0){
        var thead = theads[theads.length - 1];
        if(!thead) return;
        var input = thead.querySelector("label > input");
        if(!input) return;
        var id = input.id;
        if(!id){
            var el = document.getElementById("acc_label_ck");
            if(el)
                el.id = "";
            id = "acc_label_ck";
            input.id = id;
        }
        var checkboxesel = document.querySelectorAll("input[name='selection']");
        forEach(checkboxesel, function(ck){
            ck.setAttribute('aria-labelledby', id);
        });
    }
}

function addAriaLabelsForRadio(){
    var radioGroups = {};
    var radios = document.querySelectorAll("input[type='radio']");
    // Create radio groups
    forEach(radios, function(radio){
        if(radioGroups[radio.name])
            radioGroups[radio.name].push(radio);
        else
            radioGroups[radio.name] = [radio];
    });
    for(var name in radioGroups){
        var rg = radioGroups[name];
        if(rg){
            var parent = rg[0].parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
            var label = parent.querySelector("label");
            if(label){
                label.id = "acc_" + name;
                forEach(rg, function(radio){
                    radio.setAttribute('aria-labelledby', label.id);
                });
            }
            
        }
    }
}



function addAriaLabelsForTextArea(){
    var textArea = {};
    var texts = document.querySelectorAll("textarea");
    // Create radio groups
    forEach(texts, function(text){
        if(textArea[text.name])
            textArea[text.name].push(text);
        else
            textArea[text.name] = [text];
    });
    for(var name in textArea){
        var rg = textArea[name];
        if(rg){
            var parent = rg[0].parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
            var label = parent.querySelector("label");
            if(label){
                label.id = "acc_ta_" + name;
                forEach(rg, function(text){
                    text.setAttribute('aria-labelledby', label.id);
                });
            }
            
        }
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

function setUniqueDashTutleID(){
    var labels;
    var inputs = document.getElementsByTagName("input");
    for(var j=0; j<inputs.length; j++){
       if(inputs[j].id.split("-")[0] == "acc_dash_title"){
            inputs[j].id = "acc_dash_title";
            labels = inputs[j].parentNode.getElementsByTagName("label");
            if(labels.length > 0){
                labels[0].setAttribute("for", "");
            }
        } 
    }
    var dashes = document.querySelectorAll("#acc_dash_title");
    for(var k=0; k<dashes.length; k++){
        dashes[k].id = "acc_dash_title-" + (k+1);
        labels = dashes[k].parentNode.getElementsByTagName("label");
        if(labels.length > 0){
            labels[0].setAttribute("for", "acc_dash_title-" + (k+1));
        }
    }
}

function uniqueBooleanFieldID(){
    var labels = document.getElementsByClassName("oe_form_label_help");
    var inputs = document.getElementsByClassName("field_boolean");
    for(var i=0; i<labels.length; i++){
        var label = labels[i];
        var id = label.getAttribute("for");
        // If there isn't any matched id for the label
        if(!function(inputs){
            for(var j=0; j<inputs.length; j++){
                if(inputs[j].id == id){
                    return true;
                }
            }
            return false;
        }(inputs)){
            // Match its respective input, because it'll have a repeated id with other input
            var input = label.parentNode.parentNode.querySelector("td > span > input.field_boolean");
            if(input)
                input.id = id;         
        }
    }
}

function addAltForProjectDocumentKanbanImg(){
    var imgs = document.querySelectorAll("div.oe_kanban_vignette > div.oe_attachment > div > img");
    forEach(imgs, function(img){
        img.alt = "Documento de proyecto.";
    });
}

function addAltForStockDirectoryImageButton(){
    var imgs = document.getElementsByTagName("img");
    forEach(imgs, function(img){
       if(img.src.indexOf("STOCK_DIRECTORY") !== -1){
           img.alt = "Seleccionar archivo.";
       }
       else if(img.src.indexOf("gtk-save") !== -1){
           img.alt = "Guardar como.";
       }
       else if(img.src.indexOf("gtk-find") !== -1){
           img.alt = "Buscar";
       }
       else if(img.src.indexOf("gtk-execute") !== -1){
           img.alt = "Lanzar";
       }
       else if(img.src.indexOf("gtk-refresh") !== -1){
           img.alt = "Recargar";
       }
       else if(img.src.indexOf("gtk-ok") !== -1){
           img.alt = "Ok";
       }
       else if(img.src.indexOf("gtk-cancel") !== -1){
           img.alt = "Desist";
       }
       else if(img.src.indexOf("STOCK_MISSING_IMAGE") !== -1){
           img.alt = "Limpiar contenido.";
       }
       else if(img.src.indexOf("STOCK_APPLY") !== -1){
           img.alt = "Validar.";
       }
       else if(img.src.indexOf("image_medium") !== -1){
           img.alt = "Imagen.";
       }
    });
}

function addAltForEmployeeImg(){
    var imgs = document.getElementsByClassName("oe_employee_picture");
    forEach(imgs, function(img){
       img.alt = "Imagen de empleado."; 
    });
}


/* -- agregado manuel 6-12 --*/


function addfocusonSwitchKanban(){
    var imgk = document.querySelectorAll("a.oe_vm_switch_kanban");
    var i;
    for (i = 0; i < imgk.length; i++) {
        imgk[i].href = "#";
        imgk[i].innerHTML ="k";
    }

    var imgl = document.querySelectorAll("a.oe_vm_switch_list");
    var j;
    for (j = 0; j < imgl.length; j++) {
        imgl[j].href = "#";
        imgl[j].innerHTML ="i";
    }

    var imgf = document.querySelectorAll("a.oe_vm_switch_form");
    var f;
    for (f = 0; f < imgf.length; f++) {
        imgf[f].href = "#";
        imgf[f].innerHTML ="m";
    }

    var imgq = document.querySelectorAll("a.oe_vm_switch_calendar");
    var q;
    for (q = 0; q < imgq.length; q++) {
        imgq[q].href = "#";
        imgq[q].innerHTML ="P";
    }

    var imgg = document.querySelectorAll("a.oe_vm_switch_graph");
    var g;
    for (g = 0; g < imgg.length; g++) {
        imgg[g].href = "#";
        imgg[g].innerHTML ="}";
    }

}



/* -- END OF ACCESIBILITY RULES -- */

var acc = AccesibilityEngine;
acc.subscribe(addLabels);
acc.subscribe(addContentToTableHeader);
acc.subscribe(addContentToTeamAction);
acc.subscribe(removeDuplicatedLabelsInIMActions);
acc.subscribe(altForKanbanBottomRight);
acc.subscribe(altForKanbanAvatar);
acc.subscribe(fillLinksKanbanColorPicker);
acc.subscribe(altForFormImage);
acc.subscribe(altForTranslatableImage);
acc.subscribe(altForSalesteamsImage);
acc.subscribe(altForSearchButton);
acc.subscribe(iframeTitles);
acc.subscribe(rewriteIdForGauge);
acc.subscribe(rewriteIdForDatepicker);
acc.subscribe(setAltForEmailTemplateSaveImg);
acc.subscribe(setAltForNIFConfirmationImg);
acc.subscribe(setAltForSegmentationCalculation);
acc.subscribe(setAltForSellerImg);
acc.subscribe(setAltForAlbaranScanImg);
acc.subscribe(setUserScalableForTPVViewport);
acc.subscribe(addCellsToMatchTableHeaders);
acc.subscribe(addAltForScrapImageButton);
acc.subscribe(addAltForPos);
acc.subscribe(changeTHtoTDinBodyRow);
acc.subscribe(addAriaLabelsForCheckboxes);
/*acc.subscribe(addAriaLabelsForBodyCheckboxes);*/
acc.subscribe(setUniqueMenuCounters);
acc.subscribe(setUniqueSearchViewCustomInputID);
acc.subscribe(setUniqueSearchViewCustomPublicID);
acc.subscribe(setUniqueSearchViewCustomDefaultID);
acc.subscribe(setUniqueDashTutleID);
acc.subscribe(uniqueBooleanFieldID);
acc.subscribe(addAriaLabelsForRadio);
acc.subscribe(addAltForProjectDocumentKanbanImg);
acc.subscribe(addAltForStockDirectoryImageButton);
acc.subscribe(addAltForEmployeeImg);
acc.subscribe(addfocusonSwitchKanban);

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
        
            
        },
        get_selection: function () {
            var result = {ids: [], records: []};
            if (!this.options.selectable) {
                return result;
            }
            var records = this.records;
            this.$current.find('td.oe_list_record_selector input:checked')
                    .closest('tr').each(function () {
                var record = records.get($(this).data('id'));
                result.ids.push(record.get('id'));
                result.records.push(record.attributes);
            });
            return result;
        },

        activate: function(id) {
            var self = this;
            var result = self._super(id);

            self.do_action({
                type: 'ir.actions.act_window',
                res_model: self.model,
                view_type: 'form',
                view_mode: 'form',
                res_id: id,
                views: [[false, 'form']],
                });

            return result;
        },
    });
    
    // empty link announcement bar
    instance.web.WebClient.include({
        show_annoucement_bar: function() {
            try {
                var r = this._super();
                var link = this.$el.find(".url a");
                link.html("Enlace vacío");
                link.addClass("acc_filling");

                var link2 = this.$el.find(".href");
                link2.html("Enlace vacío");
                link2.addClass("acc_filling");

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

