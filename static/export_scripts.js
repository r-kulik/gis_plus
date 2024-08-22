function addFilesToTable(responseData) {
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
        selectedFiles.push($(this).closest('tr').find('td:nth-child(2)').text());
    });

    if (selectedFiles.length === 0) {
        alert('Не выбрано ни одного файла для сохранения');
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


function exportSelectedFilesInEnglish() {
    let selectedFiles = [];

    // Gather all selected file IDs
    $('#fileTable tbody input:checked').each(function() {
        selectedFiles.push($(this).closest('tr').find('td:nth-child(2)').text());
    });

    if (selectedFiles.length === 0) {
        alert('Не выбрано ни одного файла для сохранения');
        return;
    }

    console.log(selectedFiles)

    // Send the selected file IDs to the server with in_english parameter set to True
    $.ajax({
        url: '/downloadFiles/',
        type: 'POST',
        data: {
            files: selectedFiles,
            in_english: true,  // Set in_english to True
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() // Include CSRF token if using Django CSRF protection
        },
        xhrFields: {
            responseType: 'blob' // Set the response type to blob
        },
        success: function(response) {
            // Create a download link for the zip file
            let downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(response);
            downloadLink.download = 'exported_files_english.zip';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        },
        error: function(xhr, status, error) {
            console.error('Export Error: ' + status + error);
        }
    });
}


function makeImageDragable(){
    let image = document.getElementById('zoomable-image');
    let isDragging = false;
    let startX, startY;
    let translateX = 0, translateY = 0;
    let scale = 1;
    const minScale = 0.5; // Minimum scale factor
    const maxScale = 3;  // Maximum scale factor (you can adjust this as needed)
  
    // Zoom functionality
    image.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = 1.1;
      if (e.deltaY < 0) {
        // Zoom in
        scale = Math.min(scale * zoomFactor, maxScale);
      } else {
        // Zoom out
        scale = Math.max(scale / zoomFactor, minScale);
      }
      image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    });
  
    // Drag functionality
    image.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.clientX - translateX;
      startY = e.clientY - translateY;
      image.classList.add('grabbing');
    });
  
    image.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      translateX = e.clientX - startX;
      translateY = e.clientY - startY;
      image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    });
  
    image.addEventListener('mouseup', () => {
      isDragging = false;
      image.classList.remove('grabbing');
    });
}
    
$(document).ready(
    () => {
        console.log($.fn.jquery); // Check jQuery version
        console.log(typeof $.tmpl); // Check if $.tmpl is defined
        $('#searchButton').on('click', sendRequestToGetFiles);
        $('#exportButton').on('click', exportSelectedFiles);
        $('#exportEnglishButton').on('click', exportSelectedFilesInEnglish);

        // // Add click event listener to table rows
        // $('#fileTable tbody').on('click', 'tr', function() {
        //     // Check if the clicked row is not already expanded
        //     if (!$(this).next().hasClass('window-container') && !$(this).hasClass('window-container')) {
        //         $('#fileContentTemplate').tmpl().insertAfter($(this));
        //     }
        // });

        $('#fileTable tbody').on('click', 'tr', function(event) {
            if ($(event.target).closest('td').hasClass('ignore-click')) {
                return; // Ignore the click event
            }
            const fileId = $(this).data('fileId');
            const fileName = $(this).data('fileName');
            console.log('Clicked row file ID:', fileId);
            console.log('Clicked row file Name:', fileName);
        
            Promise.all([
                getFileText(fileId, fileName),
                getImageUrl(fileId, fileName)
            ]).then(([fileText, imageUrl]) => {
                const templateData = {
                    fileText: fileText,
                    imageUrl: "../" + imageUrl
                };
                console.log(templateData.imageUrl);
                $('#fileContentTemplate').tmpl(templateData).appendTo('#windowContent');
                $('#windowOverlay').show();
                makeImageDragable();
            }).catch(error => {
                console.error('Error fetching file content or image:', error);
            });
        }); 

        $('#windowOverlay').on('click', function(event) {
            var windows = document.querySelectorAll('div.' + "window-container");
            if (windows.length > 0) { 
                $(this).hide();
                $('#windowContent').empty();
            }
        });
    }
);