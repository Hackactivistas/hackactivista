$("#formuploadajax").on("submit", function(e){
    e.preventDefault();
    var formData = new FormData(document.getElementById("formuploadajax"));
    $(".cargar_loader_ajax").show();
    $.ajax({
        url: "/covid19/",
        type: "post",
        dataType: "html",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
          $(".cargar_loader_ajax").hide();
          var date_process = new Date();
          var data = JSON.parse(data);
          if (data.is_valid) {
            $('.imagen_original').attr('src', data.url)
            if (data.data_result) {
              $('.imagen_result').attr('src', data.data_result.url)
              $('.clasificacion').text(data.data_result.clasificacion)
              $('.confiabilidad').text(data.data_result.confiabilidad)
            }
            else
            {
             $('.imagen_result').attr('src', '')
             $('.clasificacion').text('Sin respuesta')
             $('.confiabilidad').text('Desconocido') 
            }
            $('.date_process').text(date_process)
            $('#exampleModal').modal('show');
          }
          else
            {
              alert('Disculpa, ocurrio error interno al procesar la imagen.!')
            }
        },
        error: function () {
            alert('error del servidor o opcion no válida..!');
        }
    });
    
});

/*vlidate upload img */
function readURL(input) {
    if (input.files && input.files[0]) {
  
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
  
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
  
        $('.image-title').html(input.files[0].name);
      };
  
      reader.readAsDataURL(input.files[0]);
  
    } else {
      removeUpload();
    }
  }
  
  function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
  }
  $('.image-upload-wrap').bind('dragover', function () {
          $('.image-upload-wrap').addClass('image-dropping');
      });
      $('.image-upload-wrap').bind('dragleave', function () {
          $('.image-upload-wrap').removeClass('image-dropping');
  });
