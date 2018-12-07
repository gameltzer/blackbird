
submit = document.getElementById("submitBatch");
submit.addEventListener("click", myLoad);
var xhttp = new XMLHttpRequest();
// Here AJAX is used for a loader
function myLoad(){
 
    if (!xhttp) {
        alert("giving up");
        return false;
    }
    submit.disabled = true;
    xhttp.onreadystatechange = handle; 
    xhttp.open("POST", "submit", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(); 
 

}

function handle() {
    if (this.readyState !== 4) {
        document.querySelector(".loader").style.display="block";
    } 
    else {
        document.querySelector(".loader").style.display="none";
        var readyStateLog = "Ready State"+ this.readyState;
        var statusLog = this.status;
        var responseTextLog = this.responseText;
        var responseHeaderLog  = this.getAllResponseHeaders();
        var successLog = "success";
        window.location.href = "tabulate";
        var logMessage = "Log from submit page:\n"+ readyStateLog + "\n" + statusLog + "\n" + responseTextLog + "\n" + responseHeaderLog + "\n" + successLog;
        console.log(logMessage);
        // if (this.responseText === "Done." ){
        //     console.log("message recieved that things are done");
        //     xhttp.open("GET","tabulate", true);
        //     xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        //     xhttp.send(); 
        // }
        // else {
        //     console.log("something is wrong with the response from the server");
        // }
 
    } 
}


