
//The elements for selecting samples. 
sample1 = document.getElementById("id_form-0-sampleFile");
sample2 = document.getElementById("id_form-1-sampleFile");

sample1.required=true;
sample2.required=true;
//  This should allow us to hide multiple elements,  since it is contained in a div tag. 
fastaDiv = document.querySelector(".fastaInput");
// This is the actual loader, which is a div tag
var loader = document.getElementById("loader");
// This refers to the submit button
uploadButton = document.getElementById("uploadEntireBatch");
uploadButton.addEventListener("click", function(event){
    activateLoader(event);
});

//This occurs when the button is clicked and starts the action through sending information via POST to the view.
function activateLoader(event){
    // This is so the progress function "remembers" where it was last.
    var lastInterval = 0;
    var xhttp = new XMLHttpRequest();
    // This means that the form will only be sent via AJAX, rather than through the default process associated with the form element in 
    // the template.
    
    event.preventDefault();
    loader.style = "display:block";
    fastaDiv.style = "display:none";
    //this is the form data.
    theForm = document.querySelector("form");
    if (!xhttp){
        alert("giving up");
        return false; 
    }
    // This section creates a textual indicator that the page is loading.
    var para = document.createElement("p");
    para.innerHTML="Uploading files...";
    var divPlaceholder = document.getElementById("divPlaceholder");
    divPlaceholder.appendChild(para);
    // event listeners
    xhttp.upload.addEventListener("abort", function(evt){
        operationCancelled(evt); 
    });
    xhttp.upload.addEventListener("error", function(evt){
       operationErrorHandler(evt);
    });
    xhttp.upload.addEventListener("progress", function(evt){
       operationProgressMonitor(evt);
    });

    // We want this to fire when not just when it's done uploading, but when everything is 
    // finished. This is why it is not on the xhttp.upload object, but just xhttp. 
    xhttp.addEventListener("load",successfulOperation); 

    // xhttp.onreadystatechange = handleStateChange;  
    xhttp.open("POST", "uploadSingleBatch", true);
    xhttp.responseType = "json";
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    formData = new FormData(theForm);

    // The form data is passed in as an argument; note that it is a FormData object. 
    xhttp.send(formData);

   
    // This determines what happens when a cancel event occurs.
    function operationCancelled(evt){
        console.log("Operation cancelled");
        console.log(evt);

    }

    // This determines what happens when an error event occurs.
    function operationErrorHandler(evt){
        console.error("Error!");
        console.error(evt);

    }
    // This determines what happens when a progress event occurs. The percentage is output iin 
    // multiples of 5.
    function operationProgressMonitor(evt){
        var percentComplete;
        if (evt.lengthComputable) {
            percentComplete = evt.loaded/ evt.total;
        } else{
            perentComplete = -1;
        }
        percentComplete = percentComplete * 100;
        fraction = percentComplete % 1;
        percentComplete = percentComplete - fraction; 
        if (percentComplete % 5 === 0){
            // This makes sure the value is only ouput once.
            if (percentComplete > lastInterval) {
                console.log("Progress:" + percentComplete + "%");
                lastInterval = percentComplete;
            }
        }
    }

   

    // This determines what heappens whan all the Xhtml is successful, which includes navigating to a new page.
    function successfulOperation(){
        console.log("Success!");
        // This navigates to a different page.
        window.location.href= xhttp.response.url;
    }
    // This primarily just prints messages to the console.
    function handleStateChange(){

        var statusLog = xhttp.status;
        var responseData = xhttp.response;
        var responseHeader = xhttp.getAllResponseHeaders();
        var logMessage = ("Log from upload page:\n"+ "\tReady State:"+this.readyState+ "\n"+ "\t Status: "+ statusLog + "\n" + "\tResponse Content" +
        responseData + "\n"+ "\tHeaders"+ responseHeader);
        console.log(logMessage);
    }
}

