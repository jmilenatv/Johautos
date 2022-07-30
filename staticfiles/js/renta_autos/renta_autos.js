


function putDataToDetailModal(data){
    var $rentas = "<ul class='list-unstyled'>"
    var id = data.id_uuid
    if (data.rentas.length > 0){
        $.each(data.rentas, function(a, b){
            var $li = `<li>${b.auto.auto_name}:
                            <ul>
                                <li>Modelo: ${b.auto.modelo}</li>
                                <li>Tipo: ${b.auto.tipo}</li>
                                <li>Color: ${b.auto.color}</li>
                            </ul>
                        </li>`

            $rentas += $li
        });
    } else {
        $rentas += "<li> Ningun Auto rentado todavia </li>"
    }

    $rentas += "</ul>"

    


    var detail_modal = `<!-- Modal -->
        <div class="modal fade" id="DetailModal" tabindex="-1" aria-labelledby="DetailModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="DetailModalLabel">Detalle de Cliente</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row justify-content-end mb-4">
                        <div class="col-md-2">
                            <button type="button" onclick='editRecordDetail("${id}")' class="btn btn-sm btn-warning"><i class='fas fa-edit'></i></button>
                            <button type="button" class="btn btn-sm btn-danger"><i class='fas fa-trash-alt'></i></button>
                        </div>
                    </div>
                    <div class="row container">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-header bg-success">
                                    <h3 class="card-title">${data.user_name}</h3>
                                </div>
                                
                                <div class="card-body">
                                    <strong><i class="fas fa-book mr-1"></i> Datos Bancarios</strong>
                                    <p class="text-muted">
                                        Nro. de Cuenta: ${data.cuenta_numero}
                                    </p>
                                    <p class="text-muted">
                                        Credit Card Num: 
                                    </p>
                                    <div class="skeleton-text"></div>
                                        
                                    <p class="text-muted">
                                        CVV:
                                    </p>
                                    <div class="skeleton-text-2"></div>
                                    <hr>
                                    <strong><i class="fas fa-map-marker-alt mr-1"></i> Dirección</strong>
                                    <p class="text-muted">
                                        Codigo Zip: ${data.codigo_zip}
                                    </p>
                                    <div class="skeleton-text"></div>
                                    <div class="skeleton-text"></div>
                                    <div class="skeleton-text-3"></div>
                                    <p class="text-muted">Geo latitud: </p>
                                    <div class="skeleton-text-2"></div>
                                    <p class="text-muted">Geo longitud: </p>
                                    <div class="skeleton-text-2"></div>

                                    <hr>
                                    <strong><i class="fas fa-pencil-alt mr-1"></i> Datos Personales</strong>
                                    <p class="text-muted">
                                        Fecha de Nacimiento: ${data.fec_birthday}
                                    </p>
                                    <p class="text-muted">
                                        Color favorito: ${data.color_favorito}
                                    </p>
                                    <span class="skeleton-text"></span> 
                                    <hr>
                                    <strong><i class="far fa-file-alt mr-1"></i> Autos Rentados</strong>
                                    ${$rentas}
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card mb-5" style="width: 16rem;">
                                <img src="${data.avatar}" class="card-img-top profile-user-img img-fluid img-circle" alt="...">
                                <div class="card-body text-center">
                                <h5 class="card-title">Avatar</h5>
                                </div>
                            </div>
                            <div class="card" style="width: 16rem;">
                                <img src="${data.foto_dni}" class="card-img-top" alt="..." style="height: 15rem;">
                                <div class="card-body text-center" style="padding-top: 0;">
                                <h5 class="card-title">DNI</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer justify-content-center">
                </div>
            </div>
            </div>
        </div>`

        return detail_modal
}


$("#id_query" ).on("keypress",function() {
    window.clearTimeout(timer);
    
    $("tbody").html("");
    $('#hidden-spinner').show();
 });
  
 $("#id_query" ).on("keyup",function() {
    console.log($(this).val())
    window.clearTimeout(timer);
    timer = window.setTimeout(() => {
        var form_data = $("#renta_autosFilterForm").serialize();
        $('#hidden-spinner').hide();
        get_datatable(get_list_url(1, form_data))
    }, timeoutVal);
 });


 $("#renta_autosFilterForm input, select").change(function (e){

    $size = $('.page-size-input').val()
    size = $size
    form_data = $("#renta_autosFilterForm").serialize();
    get_datatable(get_list_url(1, form_data))
 
});

$(document).on("click", ".submit-button", function(e){
    e.preventDefault()
    var data = new FormData(document.getElementById("RentaAutoEditClientForm"));
    id = $(".user-id").attr('id')

    submitForm("RentaAutoEditClientForm", "POST", data, id)


});


/*  Bootstrap-Table plugin */
$('table').bootstrapTable({
    showFullscreen: true,
    stickyHeader: true,
})

$('input[name="fec_alta"]').daterangepicker({
    locale: {
       format: 'YYYY-MM-DD',
       "applyLabel": "Aplicar",
       "daysOfWeek": [
       "Do",
       "Lu",
       "Ma",
       "Mi",
       "Ju",
       "Vi",
       "Sa"
   ],
   "monthNames": [
       "Enero",
       "Febrero",
       "Marzo",
       "Abril",
       "Mayo",
       "Junio",
       "Julio",
       "Agosto",
       "Septembre",
       "Octubre",
       "Noviembre",
       "Diciembre"
   ],
   }
});
$('input[name="fec_alta"]').val("")

$(document).on('change', 'input[name="fec_alta"]', function(e){
    window.clearTimeout(timer);
    timer = window.setTimeout(() => {
       var form_data = $("#renta_autosFilterForm").serialize();
       let params = new URLSearchParams(form_data);

       if (params.get('fec_alta') !== ''){
          get_datatable(get_list_url(1, form_data))
       }
    }, timeoutVal);
});

$(`#${section_name}FilterForm`).trigger("reset");