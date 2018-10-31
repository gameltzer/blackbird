fastChoice = document.getElementById("fastButton");
csvChoice = document.getElementById("csvButton");
formSelectInput = document.querySelector(".formSelectInput");
csvInput = document.querySelector(".csvInput");
// clearModels = document.querySelector(".clear");
// clearStatus = document.getElementById("clearStatus");
// choices =document.querySelector(".determineInputType");

csvInput.style.display = "none";
formSelectInput.style.display ="none";
// clearStatus.style.display= "none";
// choices.style.display="none";

fastChoice.onclick = fastSelect;
csvChoice.onclick = csvSelect;
// clearModels.onclick = clearFunction; 
// This is the default. 




function fastSelect(){
    formSelectInput.style.display = "block";
    csvInput.style.display = "none";
//    clearStatus.textContent = ""; 
    console.log(formSelectInput);
}

function csvSelect(){
    csvInput.style.display = "block";
    formSelectInput.style.display ="none";
//    clearStatus.textContent = ""; 
    console.log(csvInput);
}

// function clearFunction()  {
//     clearStatus.style.display= "block";    
//     csvInput.style.display = "none";
//     formSelectInput.style.display ="none";
//     // choices.style.display="block";
// }
