function getImageUrl(file_name) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_image_url/',
            type: 'POST',
            data: { file_name: file_name },
            success: function(data) {
                if (data.image_url) {
                    resolve(data.image_url);
                } else {
                    reject(new Error('Failed to get image URL'));
                }
            },
            error: function(xhr, status, error) {
                reject(new Error('AJAX Error: ' + error));
            }
        });
    });
}



function getImageUrlByFileId(fileId) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_internal_storage_path/',
            type: 'POST',
            data: { file_id: fileId },
            success: function(data) {
                if (data.internal_storage_path) {
                    getImageUrl(data.internal_storage_path)
                        .then(function(image_url) {
                            resolve(image_url);
                        })
                        .catch(function(error) {
                            reject(error);
                        });
                } else {
                    reject(new Error('Failed to get internal storage path'));
                }
            },
            error: function(xhr, status, error) {
                reject(new Error('AJAX Error: ' + error));
            }
        });
    });
}

function getFileText(file_name) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_file_text_by_name/',
            type: 'POST',
            data: { file_name: file_name },
            success: function(data) {
                if (data.file_text) {
                    resolve(data.file_text);
                } else {
                    reject(new Error('Failed to get file text'));
                }
            },
            error: function(xhr, status, error) {
                reject(new Error('AJAX Error: ' + error));
            }
        });
    });
}

function getFileTextByFileId(fileId) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_file_text_by_id/',
            type: 'POST',
            data: { file_id: fileId },
            success: function(data) {
                if (data.file_text) {
                    resolve(data.file_text);
                } else {
                    reject(new Error('Failed to get file text'));
                }
            },
            error: function(xhr, status, error) {
                reject(new Error('AJAX Error: ' + error));
            }
        });
    });
}


getImageUrlByFileId(1)
    .then(function(image_url) {
        console.log('Image URL:', image_url);
        // You can now use the image_url as needed
    })
    .catch(function(error) {
        console.error('Error:', error);
    });