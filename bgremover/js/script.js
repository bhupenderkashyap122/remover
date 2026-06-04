const form =
document.getElementById("uploadForm");

const input =
document.getElementById("imageInput");

const before =
document.getElementById("beforeImg");

const after =
document.getElementById("afterImg");

const loader =
document.getElementById("loader");

const download =
document.getElementById("downloadBtn");

input.addEventListener(
"change",
function(){

before.src =
URL.createObjectURL(
this.files[0]
);

}
);

form.addEventListener(
"submit",
async function(e){

e.preventDefault();

loader.classList.remove("d-none");

let formData =
new FormData();

formData.append(
"image",
input.files[0]
);

let response =
await fetch(
"/remove",
{
method:"POST",
body:formData
}
);

let data =
await response.json();

after.src =
data.output +
"?" +
new Date().getTime();

loader.classList.add("d-none");

download.classList.remove(
"d-none"
);

}
);

document
.getElementById("darkMode")
.addEventListener(
"click",
()=>{
document.body.classList.toggle(
"dark"
);
});