
function on() {
    
    //enables the display of the editor hidden layer.
    console.log("Showing MultiPageEditor");
    document.getElementById("overlay").style.display = "block";
    
    //here we should also load up the content of the editor data.
    readCMSContents(1); //The parameter is no longer used. Its a dummy param
   
    //Update the dynamic toggleable publisher or frontpage checkbox
    
    published_checkbox = document.getElementById('published_checkbox');
    published_checkbox.checked = view_json["published"];
    
    frontpage_checkbox = document.getElementById('frontpage_checkbox');
    frontpage_checkbox.checked = view_json["frontpage"];  
 }

function close_admin_overlay() {
    document.getElementById("overlay").style.display = "none";
}

$("#close-admin-overlay-button").click(function(){
        console.log("close-admin-overlay-button clicked");
        close_admin_overlay();
        });

function formatButtonHandler(label){

    console.log(label);
    
    if (label == 'H1') {
        console.log("H1 Not Implemented yet.")
    }else if (label == "H2"){
        console.log("H2 Not Implemented yet")
    }else if (label == "H3"){
            console.log('H3 Not Implemented yet')
            }      
}

function readCMSContents(content_id){
/* Does a GET for the content and updates the editor textarea.
API Version 1 defines the endpoint as: 
/cms/api/v1/cmscontents/{resource_id}/
*/
    console.log("readCMSContents called.");
    url = "/cms/api/v2/cmscontents/" + view_json.content[0]+ "/";
    
    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
            content = data["content"];
            //console.log(content);
            $("#markup").text(content);
        }
    });
}

function updateCMSContents(content_id){

    console.log("updateCMSContents callled");
    url = "/cms/api/v2/cmscontents/"+ view_json.content[0] + "/";
    
    console.log("updateCMSContents: PUT :  " + url);
    
    content = $("textarea#markup").val();
    console.log("updateCMSContents sending " + content);
     $.ajax({
        url: url,
        type: 'PUT',
        data: { content : content, markup: 1},

        error: function(data){ 
            console.log("Publish Failed with error", data); 
        },
        success: function(data){
            console.log("Updated published status of the page.: " ,data);
            /*We also need to update the window.page_content and force a refresh */
            url = "/cms/api/v2/cmscontents/"+ view_json.content[0] + "/html/"
            //url = "/cms/api/v2/utils/cmsformatter/" + view_json.content[0] + "/html/"
           
            $.ajax({
                url: url,
                type: 'GET',
                error: function(error){
                console.log("Error is ", error);
                    var message = "<strong>Failed to get cmscontent object</strong>. The server gave us: " + error.statusText;
                    alerterror(message, "admin-message-panel");
                },
                success: function(data){
                    /*On success we update window.editor_content before going ahead
                    on showing the editor.*/
                    html_content = data["html"];
                    window.page_content = html_content;
                    document.getElementById('page_content').innerHTML = html_content;
                    
                    alertsuccess("Successfully updated page.", "admin-message-panel");
                }
            });
                
            
        }
    });

}

function togglePublishedStatus(){
    published_check_box_status = view_json["published"];
    console.log(published_check_box_status);  
}


function toggleFrontPageStatus(){
}


function previewCMSContent(content_id){
    console.log("previewCMSContents callled");
    url = "/cms/api/v2/cmspreview/";
    
    console.log("updateCMSContents: PUT :  " + url);
    
    content = $("textarea#markup").val();
     $.ajax({
        url: url,
        type: 'POST',
        data: { content : content, markup: 1},

        error: function(data){ 
            console.log("Publish Failed with error", data); 
        },
        success: function(data){
            console.log("got Formatted content");
            document.getElementById('page_preview').innerHTML = data["content"];
           // close_admin_overlay()
        }
    });

}


function resizeEditor(){
    $('#slider').width(1024);
}


function insertAtCaret(areaId, text) {
        var txtarea = document.getElementById(areaId);
        if (!txtarea) { return; }

        var scrollPos = txtarea.scrollTop;
        var strPos = 0;
        var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
                "ff" : (document.selection ? "ie" : false ) );
        if (br == "ie") {
                txtarea.focus();
                var range = document.selection.createRange();
                range.moveStart ('character', -txtarea.value.length);
                strPos = range.text.length;
        } else if (br == "ff") {
                strPos = txtarea.selectionStart;
        }

        var front = (txtarea.value).substring(0, strPos);
        var back = (txtarea.value).substring(strPos, txtarea.value.length);
        txtarea.value = front + text + back;
        strPos = strPos + text.length;
        if (br == "ie") {
                txtarea.focus();
                var ieRange = document.selection.createRange();
                ieRange.moveStart ('character', -txtarea.value.length);
                ieRange.moveStart ('character', strPos);
                ieRange.moveEnd ('character', 0);
                ieRange.select();
        } else if (br == "ff") {
                txtarea.selectionStart = strPos;
                txtarea.selectionEnd = strPos;
                txtarea.focus();
        }

        txtarea.scrollTop = scrollPos;
}



/** 

Old functions probably we will not use
**/


function toggleEditor(){
    
    console.log("Editor is: " + window.editor_window);
    if (window.editor_window == true){ 
        console.log("Editor was shown. Going to hide it");
        hideEditor();
        window.editor_window = false;
        }else{
            console.log("Editor was hidden, Going to show");

            showEditor();
            window.editor_window = true;
        } 
    console.log("Editor is now: " + window.editor_window);
}


function hideEditor(){

    /* Load the html back on the editor */ 


    url = "/cms/api/v2/utils/cmsformatter/"+ view_json.content[0] + "/";
    $.ajax({
            url: url,
            type: 'GET',
            error: function(){
                console.log("Failed to get cmscontent object");
            },
            success: function(data){
                /*On success we update window.editor_content before going ahead
                on showing the editor.*/
               
                html_content = data["html"];
                 //console.log("***************************************************************");
                //console.log(html_content);
                document.getElementById('page_content').innerHTML= html_content;
                window.editor_window = false;
                window.page_content = html_content;
                }
        });

}

function showEditor(){
    
    console.log("showEditor called.");
    /* backup the page_content div */
     window.page_content = document.getElementById('page_content').innerHTML;
     
    if  (window.editor_content === null || window.editor_content === undefined ){
        /* 
            We store the page source in window.editor_content. But if this is the 
            first time we are accessing the editor, it could be that we still need 
            to load it first. 
        */
        
        url = "/cms/api/v2/cmscontents/"+ view_json.content[0] + "/";
    
        $.ajax({
            url: url,
            type: 'GET',
            error: function(err, out){
                console.log("Error " + data);
            },
            success: function(data){
                /*On success we update window.editor_content before going ahead
                on showing the editor.*/
                markup_content = data["content"];
                dust.render("yacms\/templates\/yacms\/dustjs_templates\/page_content", 
                            { page_content: markup_content },
                            function(err, out){
                                //console.log(err, out)
                                document.getElementById('page_content').innerHTML = out;
                            });
                            
            }
        });
    }else{
        /*
            The window.editor_content is not null or undefined so we will use 
            what we have in it to render the editor.
        */
    
        console.log("window.editor_content : " + window.editor_content);
        
        /* the page_content html */
        //window.page_content = document.getElementById('page_content').innerHTML;
      
        dust.render("yacms\/templates\/yacms\/dustjs_templates\/page_content", 
                    { page_content: window.editor_content }, function(err, out){
                            //console.log(err, out)
                            document.getElementById('page_content').innerHTML = out;
                    });
        window.editor_window = true;
    }
}

/* Member Pages Creation Functions */


$("#createpage_title").focusout(function(){
    console.log("createpage_title");
    console.log($("#createpage_title").val());

    var title = $("#createpage_title").val();
    var slug = string_to_slug(title);
    $("#createpage_slug").val(slug);
});

function string_to_slug (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    console.log(str);
    return str;
}


$("#create_page_button").click(function(){
    console.log("yhou want to create a category");
    console.log($("#createpage_title").val());

        /* create the path. We need to post:
                1. current path + slug
                2. parent id
        */

        title = $("#createpage_title").val();
        slug = $("#createpage_slug").val();
        page_type = $('select[name=createpage_pagetype_select]').val();

        console.log(page_type);
        data = {
             title: title ,
             slug : slug,
             content: [ ],
             page_type: page_type,
            frontpage: false,
            published: false,
            page_number: 0
            };

        url = "/cms/api/v2/cmsentries/" + view_json.id + "/create_child/";
         $.ajax({
        url: url,
        type: 'POST',
        data: data,

        error: function(data){
            console.log("Category Child Creation Failed with error", data);
        },
        success: function(data){
            /**Update the editor for the newly created pages.**/
           console.log("Success");
           //getCMSCategories();
            getChildCMSEntries()
        }
    });
});



function getCMSCategories(content_id){
/** Does a GET for the content and updates the editor textarea.

API Version 1 defines the endpoint as:

/cms/api/v1/cmscontents/{resource_id}/
**/
    console.log("getCMSCategories called.");

    pk = view_json.id;
    //var pk=2;
    url = "/cms/api/v2/cmsentries/" + pk  + "/get_categories/";

    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
            content = data["categories"];
            console.log("DATA ", data);
            results = data["results"];
            console.log("RESULTS " + results );
                dust.render("yacms\/templates\/yacms\/dustjs_templates\/category_editor"
                            , { data: data }, function(err, out) {
                  // `out` contains the rendered output.
                  document.getElementById('category_editor').innerHTML= out;
                });
        }
    });

}



function getChildCMSEntries(){
   
    path_id = view_json.path;
    url = "/cms/api/v2/cmsentries/?limit=20&parent_path_id="+path_id;


    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get CMSEntries");
        },
        success: function(data){
            console.log("ChildCMSEntries:", data);

            $('#CMSEntriesTable tbody').empty();

            results = data["results"];

            for (var i=0; i < results.length; i++){
                 entry = results[i];
                 table_row = "<tr><td>" + entry.id + "</td>";

                title_link = "<a href=\"/cms"+ entry.path + "\">" + entry.title + "</a>"

                table_row = table_row + "<td>" + title_link + "</td>";
                table_row = table_row + "<td>" + entry.page_type + "</td>";
                table_row = table_row + "<td>"+ entry.published +"</td>";
                table_row = table_row + "<td>"+ entry.frontpage +"</td>";
                table_row = table_row + "<td>"+ entry.date_created +"</td></tr>";

                console.log("Adding : " + table_row)

                $('#CMSEntriesTable tbody:last-child').append(table_row);


            }
        }
    });



}


$('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
  var target = $(e.target).attr("href") // activated tab


    
    if (target == "#sub_pages"){
    
        console.log("Getting Child CMS Entries");
       getChildCMSEntries();
    }
});


$(document).ready(function(){ 

    $('#published_checkbox').click(function() {
        var self = this;        
        console.log("Published Status:", self.checked);
        
        //update the view_json because it is used by the editor
    
        view_json["published"] = self.checked;    
        console.log(view_json["published"]);
        console.log(view_json["frontpage"]);
        
        published_check_box_status = view_json["published"];
        console.log(published_check_box_status);
        
        //Do a PUT to set the published status
        
        url = "/cms/api/v2/cmsentries/" + view_json["id"] + "/";
        
        console.log("togglePublishedStatus: partial_update PATCH :  " + url);
    
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { published : self.checked },
    
            error: function(data){ 
                console.log("Publish Failed with error", data); 
            },
            success: function(data){
                console.log("got Formatted content");
                //document.getElementById('page_preview').innerHTML = data["content"];
               // close_admin_overlay()
            }
        });
        
    });
    
    $('#frontpage_checkbox').click(function() {
        var self = this;        
        console.log("Frontpage Status:", self.checked);
         //update the view_json because it is used by the editor
    
        view_json["frontpage"] = self.checked;    
        console.log(view_json["published"]);
        console.log(view_json["frontpage"]);
        
        published_check_box_status = view_json["frontpage"];
        console.log(published_check_box_status);
        
        //Do a PUT to set the published status
        
        url = "/cms/api/v2/cmsentries/" + view_json["id"] + "/";
        
        console.log("togglePublishedStatus: partial_update PATCH :  " + url);
    
        $.ajax({
            url: url,
            type: 'PATCH',
            data: { frontpage : self.checked },
    
            error: function(data){ 
                console.log("Set FrontPage failed.", data); 
            },
            success: function(data){
                console.log("Set frontpage ");
                //document.getElementById('page_preview').innerHTML = data["content"];
               // close_admin_overlay()
            }
        });



        
    });
    
});
