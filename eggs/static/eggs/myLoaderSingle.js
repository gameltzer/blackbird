
var submit = document.getElementById("submitBatch");
submit.addEventListener("click", function(event){ myLoad(event);});
var info_id = document.getElementById("info_id");

var loader = document.getElementById("loader");

// Here AJAX is used for a loader
function myLoad(event){
    // event.preventDefault();

    // This is so the progress function "remembers" where it was last.
    var lastInterval = 0;
    var xhttp = new XMLHttpRequest();
    if (!xhttp) {
        alert("giving up");
        return false;
    }
    loader.style= "display:block";
    submit.style = "display:none";

    // This creates a textual reminder that the page is loading. 
    var para = document.createElement("p");
    para.innerHTML = "Processing data...";
    info_id.appendChild(para);

     // Listeners
     xhttp.addEventListener("load", function(evt){
        loadHandler(evt);
        });
    xhttp.addEventListener("error",function(evt){
        errorHandler(evt);
    });
    xhttp.addEventListener("abort", function(evt){
        aborthandler(evt);
    });
    xhttp.addEventListener("loadstart", loadingHasStarted);
        // xhttp.addEventListener("progress", function(evt){
        //     updateProgress(evt);
        // });
    // xhttp.onreadystatechange = handle; 
    
    xhttp.open("POST", "submit", true);
    xhttp.responseType = "json";
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
   
    xhttp.send(); 
 
    // This lets us know if a failure has occured.
    function failure(){
        failureIcon = document.getElementById("failure");
        failureIcon.style="display:block";
        loader.style="display:none";
    }

    function handle() {

        // if (this.readyState !== 4) {
            // loader.style.display="block";
        // } 
        // else {
        //     document.querySelector(".loader").style.display="none";
            var readyStateLog = "Ready State"+ this.readyState;
            var statusLog = this.status;
            var responseTextLog = this.response;
            var responseHeaderLog  = this.getAllResponseHeaders();
            // window.location.href = "graph";
            var logMessage = "Log from submit page:\n"+ readyStateLog + "\n" + statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n"+ this.responseURL ;
            console.log(logMessage);
            // if (this.readyState !== 4) {

            // }
            // if (this.responseText === "Done." ){
            //     console.log("message recieved that things are done");
            //     xhttp.open("GET","tabulate", true);
            //     xhttp.setRequestHeader("X-CSRFToken", csrftoken);
            //     xhttp.send(); 
            // }
            // else {
            //     console.log("something is wrong with the response from the server");
            // }
    
        // } 
    }

    // Indicates that we have started loading. 
    function loadingHasStarted(){
        console.log("Loading has started");
    }
    // Handles successful loading. 
    function loadHandler(evt){
        if (xhttp.status === 200){
            var thisResponse = xhttp.response; 
            console.log("success");
            console.log(evt);
            loader.style = "display:none";
            console.log(thisResponse);
            window.location.href =thisResponse.url;
        } else{
            console.log(xhttp.statusText);
            console.log("XMLHttpRequest Failed");
        }
    }

    // handles error
    function errorHandler(evt){
        failure();
        console.error("error");
        console.error(evt);
    }

    // handles cancel
    function aborthandler(evt){
        failure();
        console.log("Operation cancelled");
        console.log(evt);
        var error =evt.target.error;
            if (error != null){
                console.log(String(error));
            }
    }

    // monitors progress
    function updateProgress(evt){
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
    }

}