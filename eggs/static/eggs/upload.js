// Grab elements

var sample1Input = document.getElementById("sample1");
var sample2Input = document.getElementById("sample2");
var referenceInput = document.getElementById("referenceFile");
var batchInput = document.getElementById("batch");

var uploadButton = document.getElementById("uploadActionButton");

// This is the name of the batch.

var batchName; 
// a few functions will use this
function getFileFromInput(inputElement){
    return inputElement.value;
}

 referenceInput.setAttribute("accept", ".fasta, .fastq");


// If we have all the inputs, we enable the button 
function checkInputs(){
    var sample1File=getFileFromInput(sample1Input); 
    var sample2File=getFileFromInput(sample2Input);
    var referenceFile=getFileFromInput(referenceInput); 
// var batchName; 
    if (Boolean(sample1File) && Boolean(sample2File) &&
     Boolean(referenceFile) && Boolean(batchName) ) {
        uploadButton.disabled = false;
        console.log("enabled");
     }
     else{
         uploadButton.disabled = true;
         console.log("disabled");}
         console.log(sample1File);
         console.log(sample2File);
         console.log(referenceFile);
         console.log(batchName);
}

// this allows us to enter a batch name via a prompt
function batchHandler(){
    batchName = prompt("Provide batch name");
    checkInputs();
}



sample1Input.addEventListener('change',checkInputs);

sample2Input.addEventListener('change', checkInputs);

referenceInput.addEventListener('change',checkInputs);

batchInput.addEventListener("click", batchHandler);



function uploadBatch(){
    var sample1File=getFileFromInput(sample1Input); 
    var sample2File=getFileFromInput(sample2Input);
    referenceContextFile=getFileFromInput(referenceInput);
    console.log(referenceContextFile);

}






