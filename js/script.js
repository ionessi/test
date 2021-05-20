'use strict';

document.addEventListener('DOMContentLoaded', () => {

});

function addFile(event, id) {
    event.preventDefault();
    event.stopImmediatePropagation();
    
    let filer = document.getElementById(id);
    filer.click();
    /*document.getElementById('mime_type').value = file.files[0].type;
    console.log(file.files[0].type)*/
}
