function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
 }
const csrftoken = getCookie('csrftoken');


var ws_scheme = window.location.protocol
var path = ws_scheme + '//' + window.location.host + "/";
var current_page = 1;
var size = 10;
let timer, timeoutVal = 1000;


function editRecordDetail(id){
    url = path
    url += `renta-autos/${id}/edit/`;
 
    $.ajax({
       method: "GET",
       url: url,
       success: function(data){
        
        if (data.status !== 403){
            $('#DetailModal .modal-body').html("")
            $('#DetailModal .modal-body').html(data.html_content)
            $('#DetailModal .modal-footer').append('<button class="btn btn-success submit-button" type="submit" >Guardar Cambios</button>')
        } else {
            Swal.fire({
                title: 'Error!',
                html: data['message'],
                icon: 'error'
            });
        }

       },
       error: function(response){
          console.log("Error Ajax function.")
          console.log(response)
          Swal.fire({
             title: 'Error!',
             html: response['error'],
             icon: 'error'
          });
       }
    })
}

function showDetailModal(id){
    url = path
    url += `api/renta-autos/${id}/`;


 
    $.ajax({
       method: "GET",
       url: url,
       success: function(data){

        detail_modal = putDataToDetailModal(data)

        if ($('body').find('#DetailModal').length === 0){
            $('body').append(detail_modal)
            $('#DetailModal').modal('show')
        } else {
            $('#DetailModal').modal("hide")
            $('#DetailModal').remove()
            $('body').append(detail_modal)
            $('#DetailModal').modal('show')
        }
 
       },
       error: function(response){
          console.log("Error Ajax function.")
          console.log(response)
          Swal.fire({
             title: 'Error!',
             html: response['error'],
             icon: 'error'
          });
       }
    })
}

function changeStatus(action){

    if (action === 'loading'){
        $('.overlay-wrapper').removeClass("d-none")
        $("#hidden-spinner").show();
    } else {
        $('.overlay-wrapper').addClass("d-none")
        $("#hidden-spinner").hide();

    }
}

function create_pagination_control(res){
    previous_url = res.links.previous;
    next_url = res.links.next;
    page_links = res.page_links.page_links;
 
    ul = '<ul class="pagination" style="margin: 5px 0 10px 0;justify-content: center;">'
 
    if (previous_url){
       li = `<li>
                <button  class="page-link" data-url="${previous_url}" aria-label="Previous">
                   <span aria-hidden="true">&laquo;</span>
                </button>
             </li>`;
    } else {
       li = `<li class="page-item disabled">
                <button  class="page-link" aria-label="Previous">
                   <span aria-hidden="true">&laquo;</span>
                </button>
             </li>`;
    }
    ul += li;

    $.each(page_links, function (id, page){
       if (page.is_break) {
          li2 = `<li class="page-item disabled">
                   <button class="page-link"><span aria-hidden="true">&hellip;</span></button>
                </li>`
       } else {
          if (page.is_active ){
             li2 = `<li class="page-item active">
                      <button class="page-link" id="button-${id}" data-url="${page.url}">${page.number}</button>
                   </li>`
          } else {
             li2 = `<li>
                      <button class="page-link" id="button-${id}" data-url="${page.url}">${page.number}</button>
                   </li>`
          }
       }
       ul += li2;
    });
 
    if (next_url) {
       li3 = `<li>
                <button class="page-link" data-url="${next_url}" aria-label="Next">
                   <span aria-hidden="true">&raquo;</span>
                </button>
             </li>`
    } else {
       li3 = `<li class="page-item disabled">
                <button class="page-link" aria-label="Next">
                   <span aria-hidden="true">&raquo;</span>
                </button>
             </li>`
    }
    ul += li3;
    ul += `</ul>`
 
    return ul
 
}

function putTableData(res){
    $(`#table_${section_name} tbody`).html("")
    tbody = $(`#table_${section_name} tbody`)

    if (res['results'].length > 0){
        $.each(res['results'], function (a, b){

            if (section_name === 'renta_autos') {
                var id = b.id_uuid
                var row = "<tr><td>"+b.cuenta_numero+"</td>"
                    row += `<td><a href='javascript:void(0);' onclick='showDetailModal("${id}")'>`+b.user_name+`</a></td>`
                    row += "<td>"+b.fec_alta+"</td>"
                    row += "<td>"+b.codigo_zip+"</td>"
                    row += "<td>"+b.compras_realizadas+"</td>"
                    row += "<td>"+b.color_favorito+"</td>"
                    row += "<td>"+b.fec_birthday+"</td>"
                tbody.append($(row))
            } else if (section_name === 'auditoria'){
                var row = "<tr><td>"+b.history_date+"</td>"
                row += "<td>"+b.user_name+"</td>"
                row += "<td>"+b.changed_by+"</td>"
                row += "<td>"+b.history_change_reason+"</td>"
                tbody.append($(row)) 
            }

        });
    } else {
        $(`#table_${section_name} tbody`).html("No se encontraron resultados.")
    }

    pagination = create_pagination_control(res)
    $(".pagination-box").html("")
    $(".pagination-box").append(pagination)
}

function displayFormMessage(res, sender_form){
    var status_code = res.status;
    var errors = res.errors;


    if (status_code === 200){
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: res['message'],
            showConfirmButton: false,
            timer: 3000
        })

        // $(`#${sender_form}`).find('input, select, textarea')
        // .each(function () {
        //     $(this).val('');
        // });
    } else if (status_code === 400){
        if ($("input").next('p').length) $("input").nextAll('p').empty();
        if ($("select").next('p').length) $("select").nextAll('p').empty();
        if ($('textarea').next('p').length) $("textarea").nextAll('p').empty(); 

        
        for ( var i=0, errorCount=errors.length; i<errorCount; i++){
            err_obj = JSON.parse(errors[i])

            for (var name in err_obj){
                for (var j in err_obj[name]){
                    var $input = $('input[name='+name+']');
                    var $select = $('select[name='+name+']');
                    var $textarea = $('textarea[name='+name+']');
                    $input.after("<p style='color: #ff5f5fde;'>"+ err_obj[name][j].message+ "</p>");
                    $select.after("<p style='color: #ff5f5fde;'>"+ err_obj[name][j].message+ "</p>");
                    $textarea.after("<p style='color: #ff5f5fde;'>"+ err_obj[name][i].message+ "</p>");
                }
            }
        }

        err_obj = JSON.parse(errors[0])

        $('html, body').animate({
        scrollTop: $(":input[name="+Object.keys(err_obj)[0]+"], select[name="+Object.keys(err_obj)[0]+"]").offset().top
        }, 1000);
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: res['message'],
            showConfirmButton: false,
            timer: 3000
        })
    }
}

function sendAjaxRequest(url, method, data, sender_form, load_data_table){

    changeStatus("loading")
    $.ajax({
        url: url,
        type: method,
        dataType: 'json',
        headers: {
           "X-CSRFToken": csrftoken,
        },
        data: data,
        processData: false,
        contentType: false,
        success: function(response){
            if (method === "POST"){
                console.log(response)

                displayFormMessage(response, sender_form)
                showDetailModal(response.id)
                changeStatus(null)
            } else if (method === "GET" && load_data_table === true){ 
                current_page = parseInt(response.links.current);
                putTableData(response);
                
                $("#result-count span").html(response.count)
                if (response.links.current == null){
                    $("#page-count span").html("1")
                } else {
                    $("#page-count span").html(response.links.current)
                }
                changeStatus(null)
                
            } 


        },
        error: function(response){
           console.log("Error Ajax function.")
           console.log(response)
           Swal.fire({
              title: 'Error!',
              html: response['error'],
              icon: 'error'
           });
        }
    })
}

function get_list_url(page, query){
    // TODO: Improve this logic, better change 
    // the url on server-side??
    if (section_name === 'renta_autos'){
        var section = 'renta-autos';
    } else if (section_name === 'auditoria'){
        var section = 'renta-autos/auditoria'
    }


    url = path
    url += `api/${section}/list?page=${page}&size=${size}`;

    if (query){
        query = "&" + query
        url += query
    }
    return url
}

function get_datatable(url){
    sendAjaxRequest(url, "GET", null, null, true)
}

function submitForm(sender_form, method, data, obj_id){

    if (sender_form === 'RentaAutoEditClientForm'){
        if (obj_id !== null){
            url = path + `renta-autos/${obj_id}/edit/`;
            sendAjaxRequest(url, method, data, sender_form, false)
        }
    } 
}

$('.cleaner').click(function(){
    $(`#${section_name}FilterForm`).trigger("reset");
    get_datatable(get_list_url(1))
});

$(document).on("click", ".page-link", function (e) {
    e.preventDefault();
    let url = $(this).attr("data-url");
    
    get_datatable(url);
})

if (section_name === 'renta_autos' || section_name === 'auditoria'){
    get_datatable(get_list_url(current_page));
}