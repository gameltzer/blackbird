
submit = document.getElementById("submit");
submit.addEventListener("click", myLoad);

function myLoad(){
    var xhttp = new XMLHttpRequest();
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
    if (this.readyState != 4) {
        document.querySelector(".loader").style.display="block";
    } 
    else {
        document.querySelector(".loader").style.display="none";
    } 
}


