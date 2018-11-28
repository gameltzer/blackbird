
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
    if (this.readyState !== 4 && this.status !== 203) {
        document.querySelector(".loader").style.display="block";
        console.log("Ready State"+ this.readyState);
        console.log(this.status);
        console.log(this.responseText);
        console.log(this.getAllResponseHeaders());
    } 
    else {
        document.querySelector(".loader").style.display="none";
        console.log("Ready State"+ this.readyState);
        console.log(this.status);
        console.log(this.responseText);
        console.log(this.getAllResponseHeaders());
        console.log("success");
        window.location.href = "tabulate";
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


