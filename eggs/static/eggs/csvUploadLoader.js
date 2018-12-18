upload = document.getElementById("uploadCSV");
upload.addEventListener("click", activateLoader);
var csvFilePickerCollection = document.getElementsByName("csvFile");
var csvFilePicker = csvFilePickerCollection[0];
var classCollection = document.getElementsByClassName("loader");
var loader = classCollection[0];

var label = document.querySelector("label");
// This is for the form data. 
var theForm = document.querySelector("form");
var xhttp = new XMLHttpRequest();

// Event handler. Turns on loader and disables "extract info from CSV button", and hides the picker
function activateLoader(){

    if (!xhttp){
        alert("giving up");
        return false; 
    }
    // setInterval(ping, 3000);

    // function ping(){
        
    //     xhttp.open("GET", "uploadCsv", true);

    //     xhttp.send();
    //     console.log("ping: " + this.responseText+" \n");
    // }

  
    xhttp.onreadystatechange = ajaxHandle; 
    xhttp.open("POST", "uploadCsv", true);
    xhttp.responseType = "json";
  
   

    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    formData = new FormData(theForm);
    // This is the data that would normally be sent under the encoding multipart/form-data
    xhttp.send(formData);
    loader.style = "display:block";
    upload.style = "display:none";

    function ajaxHandle() {

    
        var statusLog = this.status;
        var responseTextLog = this.response;
        var responseHeaderLog  = this.getAllResponseHeaders();
        var successLog = "success";
        var logMessage = "Log from submit page:\n"+  this.readyState + "\n"+ statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n" + successLog;
        hidePicker(csvFilePicker, label);
        console.log(logMessage);
        if (this.readyState === 4){
            loader.style = "display:none";
            console.log(this.response);
            window.location.href = this.response.url;
        }
    
    }

    // function noAjaxHandle(){
    //     loader.style = "display:block";
    //     upload.style = "display:none";
    //     hidePicker(csvFilePicker, label);
    //     var statusLog = this.status;
    //     var responseTextLog = this.responseText;
    //     var responseHeaderLog  = this.getAllResponseHeaders();
    //     var successLog = "success";
    //     var logMessage = "Log from submit page:\n"+  this.readyState + "\n"+ statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n" + successLog;
       
    //     console.log(logMessage);
    // }
    function hidePicker(csvFilePicker, label){
        csvFilePicker.style = "display:none";
        label.style = "display:none";
    
    }
    
}



