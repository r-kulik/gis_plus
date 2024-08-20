fieldUploaded = false;




$(document).ready(function() => {
    fieldFilterObject = document.getElementById("fieldFilter")
    fieldFilterObject.addEventListener('input', () => {
        if (!fieldUploaded){
            alert("change!")
        }
    }
}
)