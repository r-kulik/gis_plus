
function addFilesToTable(responseData) {
    $('#fileTable tbody').empty();

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
                addFilesToTable(response);
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error: ' + status + error);
            }
        }
    );
}


$(document).ready(
    () => {
        console.log($.fn.jquery); // Check jQuery version
        console.log(typeof $.tmpl); // Check if $.tmpl is defined
        $('#uploadButton').on('click', sendRequestToGetFiles)
    }
);