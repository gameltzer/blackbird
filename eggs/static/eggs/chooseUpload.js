fastChoice = document.getElementById("fastButton");
csvChoice = document.getElementById("csvButton");
formSelectInput = document.querySelector(".formSelectInput");
csvInput = document.querySelector(".csvInput");

fastChoice.onclick = fastSelect;
csvChoice.onclick = csvSelect;

// This is the default. 

csvInput.style.display = "none";
formSelectInput.style.display ="none";


function fastSelect(){
    formSelectInput.style.display = "block";
    csvInput.style.display = "none";
    console.log(formSelectInput);
}

function csvSelect(){
    csvInput.style.display = "block";
    formSelectInput.style.display ="none";
    console.log(csvInput);
}