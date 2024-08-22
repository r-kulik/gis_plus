function getFileText(fileId, fileName) {
    return new Promise((resolve, reject) => {
        let url = '/get_file_text/';
        if (fileId) {
            url += `?file_id=${fileId}`;
        } else if (fileName) {
            url += `?file_name=${fileName}`;
        } else {
            reject(new Error('File ID or File Name is required'));
            return;
        }

        console.log('Sending AJAX request to get file text:', { file_id: fileId, file_name: fileName });
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                console.log('AJAX request successful:', data);
                if (data.file_text) {
                    resolve(data.file_text);
                } else {
                    reject(new Error('Failed to get file text'));
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
        let url = '/get_image_url/';
        if (fileId) {
            url += `?file_id=${fileId}`;
        } else if (fileName) {
            url += `?file_name=${fileName}`;
        } else {
            reject(new Error('File ID or File Name is required'));
            return;
        }

        console.log('Sending AJAX request to get image URL:', { file_id: fileId, file_name: fileName });
        $.ajax({
            url: url,
            type: 'GET',
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

