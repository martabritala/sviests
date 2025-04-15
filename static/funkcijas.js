function atvertFormu() {
  document.getElementById("forma").style.display = "block";
}

function nospied(){
  let x = document.getElementById("cubis").value;
  x = x.toUpperCase();
  let text;
  if (x == "RIHARDS") {
    text = "Tieši tā!";
  } else {
    text = "Nē dumiķi!";
  }

  document.getElementById("vecene").innerHTML = text
}
function enters() {
  
  document.getElementById("cubis").addEventListener("keyup", (event) => {
  if (event.keyCode === 13) {
    nospied()
  }
});
}
function like(){
  alert("Palielināsies like skaits par vienu, ko katrs lietotājs var uzspiest tikai vienu reizi")
}

function add_Like(celojuma_id){
  Request()
}

function dislike(){
  alert("Palielināsies dislike skaits par vienu, ko katrs lietotājs var uzspiest tikai vienu reizi")
}

function nospied2(){
  var username = document.getElementById("username").value;
  let vards = document.getElementById("vards").value;
  let uzvards = document.getElementById("uzvards").value;
  let epasts = document.getElementById("epasts").value;
  let parole = document.getElementById("parole").value;
  
  

  alert("Username: "+ username +
       "\nVārds:"+ vards+ 
       "\nUzvārds:"+ uzvards+
       "\nE-pasts:"+ epasts+
       "\nParole:"+ parole+
       "\nApstiprinātā parole:"+ parole2
       )
  return true
}
// function nospied3(){
//   var username = document.getElementById("username1").value;
//   var parole = document.getElementById("parole1").value;
//   alert("Tu esi ielogojies" )
// }
function nospied4(){
  alert("Tavs posts tika publicēts!")
}

//function parbaude(){
    //if (document.getElementById("parole").value != document.getElementById("parole2").value){
   // alert("Paroles nesakrīt!")
    //return false
 // }
 // return true
//}



function showCombo(id) {
  // var element = document.getElementById('diena'+id);
  var visi = document.getElementById('dienas').children;
  // var display = element.style.display;
  var pogas = document.getElementById('spiezamie').children;
  for(poga of pogas){
    if (poga.id == 'spiest'+id){
      poga.children[0].classList.add("active");
    } else{
      poga.children[0].classList.remove("active");
    }
  }
  for (diena of visi){
    if (diena.id == 'diena'+id){
      diena.style.display = "block";
    }  else{
      diena.style.display = "none";
    }
    }

  }
  
function pievienoDienu() {
  poga = document.getElementById("pievDienu")
  diena = document.getElementById("diena")
  uztaisaDienu = document.createElement(diena)
  pievienoDienu = document.appendChild(uztaisaDienu)
  
}


// postans google map
// function initMapPostans() {
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: coordinates[0]["lat"], lng: coordinates[0]["lng"] },
//     zoom: 7,
//   });

//   coordinates.forEach((coord, index) => {
//     const marker = new google.maps.Marker({
//       position: { lat: coord.lat, lng: coord.lng },
//       map: map,
//       label: `${index+1}`
//     });
//   });
// }



// google maps code RONALDS lidz 257 linijai
let markers = [];
let map;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 56.92544790694042, lng: 24.07237005164161 },
    zoom: 7,
  });
  google.maps.event.addListener(map, "click", (event) => {
    addMarker(event.latLng, map);
  });
}

var markerPositions = [];

function addMarker(location, map) {
  const marker = new google.maps.Marker({
    position: location,
    map: map,
    label: `${markers.length + 1}`,
  });
  const markerId = uuidv4();
  marker.markerId = markerId;
  const infoWindow = new google.maps.InfoWindow({
    content: `<button class="removeDay" onclick="deleteMarker('${marker.markerId}')">Delete</button>`
  });
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.open(map, marker);
  });
  markers.push(marker);

  markerPositions.push({
    lat: marker.getPosition().lat(),
    lng: marker.getPosition().lng(),
  });
  console.log(markerPositions);
  const markerPositionsJSON = JSON.stringify(markerPositions);
  document.getElementById('tripRoute').value = markerPositionsJSON;
}

function deleteMarker(markerId) {
  const markerIndex = markers.findIndex((marker) => marker.markerId === markerId);
  if (markerIndex >= 0) {
    markers[markerIndex].setMap(null);
    markers.splice(markerIndex, 1);
    refreshMarkers();
  }
}

function refreshMarkers() {
  markers.forEach((marker) => {
      marker.setMap(null);
  });
  markers.forEach((marker, index) => {
    marker.setMap(map);
    marker.setLabel((index + 1).toString());
  });
}

dienas = 0
function addElement(dayID) {
  dienas++
  const newDivMain = document.createElement("div");
  const newDiv1 = document.createElement("div");
  const newContent1 = document.createElement("textarea");
  const newDiv2 = document.createElement("div");
  const newContent2 = document.createElement("textarea");
  const newDiv3 = document.createElement("div");
  const newContent3 = document.createElement("textarea");
  const newDiv4 = document.createElement("div");
  const newContent4 = document.createElement("textarea");
  const newButton = document.createElement("button")
  const newButton2 = document.createElement("button")

  var num = document.getElementsByTagName("textarea").length / 3 + 1;
  newContent1.id = "textarea" + num + "1";
  newContent1.setAttribute("cols", "60");
  newContent1.setAttribute("name", "celojumaDienasApraksts");
  newButton.setAttribute('type', "button")
  newButton.setAttribute('class', 'day')
  newButton.setAttribute('onclick', "addPieturvieta()")
  newButton.innerHTML = "Pievienot pieturvietu" + newButton.innerHTML;
  newButton2.setAttribute('type', "button")
  newButton2.setAttribute('class', 'removeDay')
  newButton2.setAttribute('onclick', "removePieturvieta()")
  newButton2.innerHTML = "Noņemt pieturvietu" + newButton2.innerHTML;
  newDiv1.appendChild(newContent1);
  newDiv1.appendChild(newButton);
  newDiv1.appendChild(newButton2);
  newContent2.id = "textarea" + num + "2";
  newContent2.setAttribute("cols", "60");
  newContent2.setAttribute("name", "celojumaDienasPlans"+dienas);
  newDiv2.appendChild(newContent2);
  newContent3.id = "textarea" + num + "3";
  newContent3.setAttribute("cols", "60");
  newContent3.setAttribute("name", "celojumaDienasNaktsmitnes");
  newDiv3.appendChild(newContent3);
  newContent4.id = "textarea" + num + "3";
  newContent4.setAttribute("cols", "60");
  newContent4.setAttribute("name", "celojumaTransportsUzNaktsmitni");
  newDiv4.appendChild(newContent4);


  const currentDiv = document.getElementById(dayID);
  currentDiv.appendChild(newDiv1);
  currentDiv.appendChild(newDiv2);
  currentDiv.appendChild(newDiv3);
  currentDiv.appendChild(newDiv4);
  newDiv1.innerHTML = dienas + ". dienas apraksts" + "<br>" + newDiv1.innerHTML;
  newDiv2.innerHTML = dienas + ". dienas pieturvietas" + "<br>" + newDiv2.innerHTML;
  newDiv3.innerHTML = dienas + ". dienas naktsmītnes" +"<br>" + newDiv3.innerHTML;
  newDiv4.innerHTML = dienas + ". transports uz naktsmītni" +"<br>" + newDiv4.innerHTML + "<br>";
}

function addPieturvieta() {
  const parentDiv = event.target.parentNode.nextElementSibling; // Get the parent div of the button
  const newContent2 = document.createElement("textarea");
  newContent2.setAttribute("cols", "60");
  newContent2.setAttribute("name", "celojumaDienasPlans"+dienas);
  parentDiv.appendChild(newContent2);
}

function removePieturvieta() {
  const parentDiv = event.target.parentNode.nextElementSibling; // Get the parent div of the button
  parentDiv.removeChild(parentDiv.lastChild);
}

function removeElement(dayID) {
  if (dienas > 0 ) {
    dienas--
  }
  const currentDiv = document.getElementById(dayID);
  const divs = currentDiv.getElementsByTagName("div");
  var removeCount = Math.min(divs.length, 4);
  for (var i = 0; i < removeCount; i++) {
    currentDiv.removeChild(divs[divs.length - 1]);
  }
}

function showPreview(event) {
  const previewContainer = document.getElementById("preview-container");
  previewContainer.innerHTML = "";
  const files = event.target.files;
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const reader = new FileReader();
    reader.onload = function (e) {
      const image = document.createElement("img");
      image.src = e.target.result;
      image.width = 150;
      image.height = 150;
      image.id = "bilde" + i
      previewContainer.appendChild(image);
    };
    reader.readAsDataURL(file);
  }
} 

function commentPoga(id){
  document.getElementById("CommentDIV"+id).classList.toggle("d-none")
}

function search(){
}

/* function Validate_Form(){
  let Name = document.getElementById("Nosaukums").value;
  let Desc = document.getElementById("Apraksts").value;
  let Days = [];
  for Day in document.getElementsByClassName("day"){
    
  }
  
 }
*/