upload = document.getElementById("uploadCSV");
upload.addEventListener("click", activateLoader);
var csvFilePickerCollection = document.getElementsByName("csvFile");
var csvFilePicker = csvFilePickerCollection[0];
var classCollection = document.getElementsByClassName("loader");
var loader = classCollection[0];

var label = document.querySelector("label");

// This is for the form data. 
var theForm = document.querySelector("form");

function activateLoader(){
    loader.style = "display:block";
    upload.style = "display:none";
    csvFilePicker.style = "display:none";
    label.style = "display:none";
}
// This gets the file from the form. 
// var file = theForm.files[0];
// var xhttp = new XMLHttpRequest();

// Event handler. Turns on loader and disables "extract info from CSV button", and hides the picker
// function activateLoader(){
//     // debugger;
//     if (!xhttp){
//         alert("giving up");
//         return false; 
//     }
//     // setInterval(ping, 3000);

//     // function ping(){
        
//     //     xhttp.open("GET", "uploadCsv", true);

//     //     xhttp.send();
//     //     console.log("ping: " + this.responseText+" \n");
//     // }

  
//     xhttp.onreadystatechange = ajaxHandle; 
//     xhttp.addEventListener("load", loadHandler);
    
//     var progressMeter = document.getElementById("progress");
//     xhttp.addEventListener("error", errorHandler);
//     xhttp.addEventListener("abort", abortHandler);
//     // xhttp.addEventListener("error", onError);
//     xhttp.upload.addEventListener("progress", uploadProgress);
//     xhttp.open("POST", "uploadCsv", true);
//     // debugger;
//     xhttp.responseType = "json";
  
   

//     xhttp.setRequestHeader("X-CSRFToken", csrftoken);
//     // debugger;
//     // xhttp.setRequestHeader("Connection","Keep-Alive");
//     formData = new FormData(theForm);
//     // formData.append('file',file);
//     // This is the data that would normally be sent under the encoding multipart/form-data
//     xhttp.send(formData);
//     // debugger;
//     loader.style = "display:block";
//     upload.style = "display:none";

//     // Handles abort events.
//     function abortHandler(evt){

//         console.log("Operation cancelled");
//         console.log(evt);
//         console.trace();
//         progressMeter.innerHTML = " Operation cancelled";
//         throw "aborted";
//     }
//     // Handles load events
//     function loadHandler(){
//         progressMeter.innerHTML = "Success!";

//     }
//     // Handles error events
//     function errorHandler(evt){
      
//             progressMeter.innerHTML= "ERROR, failure";
//             console.log(String(evt));
//     }
//     // This is for monitoring progress
//     function uploadProgress(thisEvent){
//         var percentComplete; 
//         if (thisEvent.lengthComputable) {
//             percentComplete = thisEvent.loaded/ thisEvent.total;
//         } else {
//             percentComplete = "Event not computable";
//         }
//         progressMeter.innerHTML=percentComplete;
//     }

//     function ajaxHandle() {
//         // debugger;
    
//         var statusLog = xhttp.status;
//         var responseTextLog = xhttp.response;
//         var responseHeaderLog  = xhttp.getAllResponseHeaders();
//         var successLog = "success";
//         var logMessage = "Log from submit page:\n"+  xhttp.readyState + "\n"+ statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n" + successLog;
//         hidePicker(csvFilePicker, label);
//         console.log(logMessage);
//         if (xhttp.status === 0){
//             console.error("Status is 0 for some reason");
//             throw "0 status";
//         }
//         else if (xhttp.readyState === 4){
//             loader.style = "display:none";
//             console.log(this.response);
//             // window.location.href ="submitCsv";
//         }
//         else {
//             console.log("everything seems to be running smoothly up to this point");
//         }
      
    
//     }

//     // function noAjaxHandle(){
//     //     loader.style = "display:block";
//     //     upload.style = "display:none";
//     //     hidePicker(csvFilePicker, label);
//     //     var statusLog = this.status;
//     //     var responseTextLog = this.responseText;
//     //     var responseHeaderLog  = this.getAllResponseHeaders();
//     //     var successLog = "success";
//     //     var logMessage = "Log from submit page:\n"+  this.readyState + "\n"+ statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n" + successLog;
       
//     //     console.log(logMessage);
//     // }
//     function hidePicker(csvFilePicker, label){
//         csvFilePicker.style = "display:none";
//         label.style = "display:none";
    
//     }
    
// }



