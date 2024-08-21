
function addFilesToTable(responseData) {
    ;

    console.log('Response Data:', responseData); // Check the response data
    console.log(responseData.files)

    // Ensure responseData.files is an array
    if (Array.isArray(responseData.files)) {
        console.log('Files Array:', responseData.files); // Check the structure of the files array

        // Iterate over each file and ensure metrics is a string joined by commas
        responseData.files.forEach(function(file) {
            file.metrics = Array.isArray(file.metrics) ? file.metrics.join(', ') : '';
        });

        // Render the template with the response data
        $('#fileRowTemplate').tmpl(responseData.files).appendTo('#fileTable tbody');
    } else {
        console.error('responseData.files is not an array');
    }
}

function sendRequestToGetFiles(){
    let filters = {
        fileFilter: $('#fileFilter').val(),
        fieldFilter: $('#fieldFilter').val(),
        wellNumberFilter: $('#wellNumberFilter').val(),
        startMeasureFromDepthFilter: $('#startMeasureFromDepthFilter').val(),
        finishMeasureFromDepthDepthFilter: $('#finishMeasureFromDepthFilter').val(),
        startMeasureTillDepthDepthFilter: $('#startMeasureTillDepthFilter').val(),
        finishMeasureTillDepthDepthFilter: $('#finishMeasureTillDepthFilter').val(),
        companiesFilter: $('#companiesFilter').val(),
        metricsFilter: $('#metricsFilter').val(),
        startYearFilter: $('#startYearFilter').val(),
        finishYearFilter: $('#finishYearFilter').val()
    };


    

    $.ajax(
        {
            url: '/exportFiles/',
            type: 'GET',
            data: filters,
            success: (response) => {
                $('#fileTable tbody').empty()
                addFilesToTable(response);
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error: ' + status + error);
            }
        }
    );
}


function exportSelectedFiles() {
    let selectedFiles = [];

    // Gather all selected file IDs
    $('#fileTable tbody input:checked').each(function() {
        selectedFiles.push($(this).closest('tr').find('td:nth-child(2)').text()); // Assuming fileId is in the second column
    });

    if (selectedFiles.length === 0) {
        alert('No files selected for export.');
        return;
    }

    console.log(selectedFiles)

    // Send the selected file IDs to the server
    $.ajax({
        url: '/downloadFiles/',
        type: 'POST',
        data: {
            files: selectedFiles,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() // Include CSRF token if using Django CSRF protection
        },
        xhrFields: {
            responseType: 'blob' // Set the response type to blob
        },
        success: function(response) {
            // Create a download link for the zip file
            let downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(response);
            downloadLink.download = 'exported_files.zip';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        },
        error: function(xhr, status, error) {
            console.error('Export Error: ' + status + error);
        }
    });
}

$(document).ready(
    () => {
        console.log($.fn.jquery); // Check jQuery version
        console.log(typeof $.tmpl); // Check if $.tmpl is defined
        $('#searchButton').on('click', sendRequestToGetFiles);
        $('#exportButton').on('click', exportSelectedFiles);
    }
);