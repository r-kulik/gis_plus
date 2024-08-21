function loadAndProcessFiles(data) {
    console.log(loadAndProcessFiles);
    $.each(data.files, function(i, file) {
        console.log(file);
    });
}


$(document).ready(function() {
    $('#uploadButton').click(function() {
        var formData = new FormData();
        $.each($('#fileInput')[0].files, function(i, file) {
            formData.append('files', file);
        });

        $.ajax({
            url: '/upload/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (data) => { loadAndProcessFiles(data);}
        });
    });
});