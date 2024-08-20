$(document).ready(function() {
    $('#uploadButton').click(function() {
        var formData = new FormData();
        $.each($('#fileInput')[0].files, function(i, file) {
            formData.append('files', file);
        });

        $.ajax({
            url: '{% url "upload" %}',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $.each(data.files, function(i, file) {
                    $('#fileTable tbody').append(
                        `<tr>
                            <td>${file.name}</td>
                            <td>${file.size}</td>
                            <td>${file.type}</td>
                            <td><a href="${file.path}" target="_blank">View</a></td>
                        </tr>`
                    );
                });
            }
        });
    });
});