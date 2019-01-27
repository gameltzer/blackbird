var process = document.getElementById("processFiles");

// var csvFilePickerCollection = document.getElementsByName("csvFile");
// var csvFilePicker = csvFilePickerCollection[0];
var loader = document.getElementById("loader");


process.addEventListener("click", function(evt){
    activateLoader(evt);
});
// window.addEventListener("error", function(event){
//     console.error("This is the listener that was added to the window.");
//     console.error(event);
//     console.trace("This is the trace.");
// });

// var label = document.querySelector("label");

// This is for the form data. 
// var theForm = document.querySelector("form");

// function activateLoader(){

//     csvFilePicker.style = "display:none";
//     label.style = "display:none";
// }
// // This gets the file from the form. 
// // var file = theForm.files[0];


// Event handler. Turns on loader and disables "Process files with pipeline."
function activateLoader(event){
    // event.preventDefault();
    // event.stopPropagation();
    // This is so the progress function "remembers" where it was last.
    var lastInterval = 0;
    var xhttp = new XMLHttpRequest();
    loader.style= "display:block";
    process.style = "display:none";

    // debugger;
    if (!xhttp){
        alert("giving up");
        return false; 
    }

    
    xhttp.addEventListener("load", function(event){
        loadHandler(event);
    });   

    xhttp.addEventListener("error", function(event){
        errorHandler(event);
    });
    xhttp.addEventListener("abort", function(event){
        abortHandler(event);
    });
    xhttp.addEventListener("loadstart", loadingHasStarted);

    // xhttp.addEventListener("progress", function(event){
    //     operationProgress(event);
    // });
    // xhttp.onreadystatechange = ajaxHandle; 
    
    xhttp.open("POST", "submitCsv", true);
    // debugger;
    xhttp.responseType = "json";
  
   

    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    // debugger;
    // xhttp.setRequestHeader("Connection","Keep-Alive");
    // formData = new FormData(theForm);
    // formData.append('file',file);
    // This is the data that would normally be sent under the encoding multipart/form-data

       // Event listeners
  

    
    xhttp.send();
    // debugger;
  
    function loadingHasStarted(){
        console.log("Loading has started");
    }
    // Handles abort events.
    function abortHandler(evt){
        failure();
        console.log("Operation cancelled");
        console.log(evt);
        console.trace();
        // progressMeter.innerHTML = " Operation cancelled";
        // throw "aborted";
    }

    // This lets us know if a failure has occured. 
    function failure(){
        failureIcon = document.getElementById("failure");
        failureIcon.style="display:block";
        loader.style="display:none";
    }
    // Handles load events
    function loadHandler(evt){
        var thisResponse = xhttp.response; 
        console.log("success");
        console.log(evt);
        loader.style = "display:none";    
        console.log(thisResponse);
        window.location.href =thisResponse.url;


    }
    // Handles error events
    function errorHandler(evt){
            failure();
            console.error("error");
            console.error(xhttp.statusText);
            // progressMeter.innerHTML= "ERROR, failure";
            console.error(evt);
            console.error("This is the trace");
            console.trace();
    }
    // This is for monitoring progress
    function operationProgress(thisEvent){
        console.log("Progress notification event");
        var percentComplete;
        if (evt.lengthComputable){
            percentComplete = evt.loaded/ evt.total;
        } else{
            percentComplete = -1;
        }
        percentComplete = percentComplete * 100; 
        fraction = percentComplete % 1;
        percentComplete = percentComplete - fraction;
        if (percentComplete % 5 === 0){
            //This makes certain the value is only output once.
            if (percentComplete > lastInterval) {
                console.log("Progress" + percentComplete + "%");
                lastInterval = percentComplete;
            }
        } 
        // var percentComplete; 
        // if (thisEvent.lengthComputable) {
        //     percentComplete = thisEvent.loaded/ thisEvent.total;
        // } else {
        //     percentComplete = "Event not computable";
        // }
        // console.log(percentComplete);
    }

    function ajaxHandle() {
        // debugger;
      
        
        var statusLog = xhttp.status;
        var responseTextLog = xhttp.response;
        var responseHeaderLog  = xhttp.getAllResponseHeaders();
        // var successLog = "success";
        var logMessage = `Log from submit page:
            Ready State: ${xhttp.readyState}
            Status: ${statusLog}
            Response Content: ${responseTextLog}
            Response Header: ${responseHeaderLog}`;
        // hidePicker(csvFilePicker, label);
        console.log(logMessage);
        if (xhttp.status === 0){
            console.info("Status is 0 for some reason");
        }
        // else if (xhttp.readyState === 4){
        //    l;
        // }
        else {
            console.log("everything seems to be running smoothly up to this point");
        }
    }
}
    
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

