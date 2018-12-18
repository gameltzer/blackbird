form0 = document.getElementById("id_form-0-sampleFile");
form1 = document.getElementById("id_form-1-sampleFile");
form0.required=true;
form1.required=true;
uploadButton = document.getElementById("uploadEntireBatch");
uploadButton.addEventListener("click", function(){
    uploadButton.style = "display:none";
});
