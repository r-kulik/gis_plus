function loadAndProcessFiles(data) {
    // Clear the existing rows in the table body

    // Iterate over each file in the data
    $.each(data.files, function(i, file) {
        // Determine the color based on the status
        var statusColor = '';
        var isCheckboxDisabled = true;
        if (file.status === 'ok') {
            statusColor = 'green';
            isCheckboxDisabled = false;
        } else if (file.status === 'warn') {
            statusColor = 'yellow';
            isCheckboxDisabled = false;
        } else if (file.status === 'error') {
            statusColor = 'red';
        }

        // Count the number of fatal errors and warnings
        var fatalAmount = 0;
        var warnsAmount = 0;
        $.each(file.errors, function(j, error) {
            if (error.status === 'error') {
                fatalAmount++;
            } else if (error.status === 'warn') {
                warnsAmount++;
            }
        });

        // Extract the relevant information from the file data
        var fileRowData = {
            fileName: file.name,
            fieldName: file.company_name,
            wellNumber: file.well_number,
            metrics: (file.metrics_list || []).join(', '), // Ensure metrics_list is an array
            datetime: file.datetime,
            companyName: file.company_name,
            startDepth: file.start_depth,
            stopDepth: file.stop_depth,
            status_color: statusColor,
            fatal_amount: fatalAmount,
            warns_amount: warnsAmount,
            originalFilePath: file.originalFilePath,
            processedFilePath: file.processedFilePath,
            isCheckboxDisabled: isCheckboxDisabled,
            fileVersion: file.file_version
        };

        // Render the template with the fileRowData
        var $row = $('#fileRowTemplate').tmpl(fileRowData).appendTo('#fileTable tbody');

        // Check the checkbox for rows with 'ok' status
        if (file.status === 'ok') {
            $row.find('input[type="checkbox"]').prop('checked', true);
        }
    });

    // Show the save button
    $('#saveButton').show();
}

function uploadFile(file, callback) {
    var formData = new FormData();
    formData.append('files', file);
    $.ajax({
        url: '/upload/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            loadAndProcessFiles(data);
            callback(); // Call the callback to proceed to the next file
        }
    });
}

function uploadFilesSequentially(files, index) {
    if (index >= files.length) {
        return; // All files have been processed
    }

    uploadFile(files[index], function() {
        uploadFilesSequentially(files, index + 1); // Move to the next file
    });
}

function saveFilesToDatabase() {
    var files = [];
    $('#fileTable tbody tr').each(function() {
        var $row = $(this);
        var checkbox = $row.find('input[type="checkbox"]');
        if (checkbox.is(':checked')) {
            files.push({
                name: $row.find('td:eq(3)').text(),
                company_name: $row.find('td:eq(8)').text(),
                well_number: $row.find('td:eq(5)').text(),
                metrics_list: ($row.find('td:eq(6)').text().split(', ') || []), // Ensure metrics_list is an array
                datetime: $row.find('td:eq(7)').text(),
                start_depth: $row.find('td:eq(9)').text(),
                stop_depth: $row.find('td:eq(10)').text(),
                processedFilePath: $row.find('.processedFilePathHolder').text(),
                file_version: $row.find('.fileVersionHolder').text()
            });
        }
    });

    if (files.length === 0) {
        alert('No files selected to save.');
        return;
    }

    $.ajax({
        url: '/save_to_database/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(files),
        success: function(data) {
            alert('Files saved to database successfully!');
            $('#fileTable tbody').empty(); // Clear the table
            $('#saveButton').hide(); // Hide the save button
        },
        error: function(xhr, status, error) {
            alert('Error saving files to database: ' + error);
        }
    });
}

$(document).ready(function() {
    $('#uploadButton').click(function() {
        $('#fileTable tbody').empty();
        var files = $('#fileInput')[0].files;
        uploadFilesSequentially(files, 0); // Start with the first file
    });

    $('#saveButton').click(function() {
        saveFilesToDatabase();
    });
});