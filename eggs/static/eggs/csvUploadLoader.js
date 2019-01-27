var uploadButton = document.getElementById("uploadCSV");
uploadButton.addEventListener("click", activateLoader);
var uploadFormDiv = document.getElementById("uploadForm");
var classCollection = document.getElementsByClassName("loader");
var loader = classCollection[0];
var statusMessageDiv = document.getElementById("statusMessageDiv");
var xhttp = new XMLHttpRequest();

// This is for the form data. 
var theForm = document.querySelector("form");

// window.addEventListener("error", function(event){
//     console.error("This is the listener that was added to the window.");
//     console.error(event);
//     console.trace("This is the trace.");
// });

function activateLoader(event){
    event.preventDefault();
    // event.stopPropagation();
    var lastInterval = 0; 

    if (!xhttp){
        alert("giving up");
        return false; 
    }
 
    loader.style = "display:block";
    uploadFormDiv.style = "display:none";

    // This is a textual reminder that we are uploading documents.
    var para = document.createElement("p");
    para.innerHTML = "Uploading data...";
    statusMessageDiv.appendChild(para);

    // Event listeners
    xhttp.upload.addEventListener("abort", function(evt){
        operationCancelled(evt);
    });
    xhttp.upload.addEventListener("error", function(evt){
        operationErrorHandler(evt);
    });
    xhttp.upload.addEventListener("progress", function(evt){
        operationProgressMonitor(evt);
    });

    // This should fire not just when the uploading is finished, but when everything is finished, which
    // is why this is not on the upload attribute. 
    xhttp.addEventListener("load",loadHandler);

    // xhttp.onreadystatechange = handleStateChange;
    
    xhttp.open("POST", "uploadCsv", true);
    xhttp.responseType = "json";
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
     
    // The form data is passed in an argument; nte that it is a FormData object.
    formData = new FormData(theForm); 
    xhttp.send(formData);

    // This prints messages to the console when the XMLHttpRequest object is cancelled.
    function operationCancelled(evt){
        console.log("Operation cancelled");
        console.log(evt);
    }

    // This prints messages tothe console when an error occurs with the XMLHttpRequest.
    function operationErrorHandler(evt){
        console.error("Error!");
        console.error(evt);
        console.trace("This is the trace");
    }

    // This determines what happens when a progress notification event occurs. The percentage is output
    // in multiples of 5. 
    function operationProgressMonitor(evt){
        console.log("progress notification was called");
        var percentComplete;
        if (evt.lengthComputable){
            percentComplete = evt.loaded / evt.total;
        } else {
            percentComplete = -1;
        }
        percentComplete = percentComplete * 100;
        fraction = percentComplete % 1;
        percentComplete = percentComplete - fraction;
        if (percentComplete % 5 === 0){
            // This makes sure the value is only output once.
            if (percentComplete > lastInterval) {
                console.log("Progress:" + percentComplete + "%");
                lastInterval = percentComplete; 
            }
        }
    }

    // This determines what happens when the XMLHttpRequest is successful
    function loadHandler(){
        loader.style="display:none";
        console.log("Success");

        //This navigates to the next page.
        window.location.href = xhttp.response.url;
    }

    // This prints messages to the console about the current state of the 
    // XMLHttprequest
    function handleStateChange(){
        var responseData;
        responseData = xhttp.response; 

        var statusLog  = xhttp.status;
       
        var responseHeader = xhttp.getAllResponseHeaders();
        var logMessage = (`Log from upload page: 
            Ready state: ${this.readyState}
            Status: ${statusLog}
            Response Content: ${responseData}
            Response Header: ${responseHeader}`);
        console.log(logMessage);
    }

    
    
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



