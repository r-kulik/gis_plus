function getFileText(fileId, fileName) {
    return new Promise((resolve, reject) => {
        if (!fileId && !fileName) {
            reject(new Error('File ID or File Name is required'));
            return;
        }
    
        let formData = new FormData();
        formData.append('file_id', fileId);
        formData.append('file_name', fileName);
        console.log('Sending AJAX request to get file text:');
        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
        $.ajax({
            url: "/get_file_text/",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log('AJAX request successful:', data);
                if (data.file_text) {
                    resolve(data.file_text);
                } else {
                    reject(new Error('Failed to get internal storage path'));
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
                reject(new Error('AJAX Error: ' + error));
            }
            });
        });
    }

function getImageUrl(fileId, fileName) {
    return new Promise((resolve, reject) => {
        if (!fileId && !fileName) {
            reject(new Error('File ID or File Name is required'));
            return;
        }

        let formData = new FormData();
        formData.append('file_id', fileId);
        formData.append('file_name', fileName);
        console.log('Sending AJAX request to get image:');
        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        };
        $.ajax({
            url: "/get_image_url/",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log('AJAX request successful:', data);
                if (data.image_url) {
                    resolve(data.image_url);
                } else {
                    reject(new Error('Failed to get internal storage path'));
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
                reject(new Error('AJAX Error: ' + error));
            }
        });
    });
}

