var config = {
  apiKey: "AIzaSyBIJYd5Xxa7DIORsLPJUCT2r4DqUa_bxlo",
  authDomain: "analysis-820dc.firebaseapp.com",
  databaseURL: "https://analysis-820dc.firebaseio.com",
  projectId: "analysis-820dc",
  storageBucket: "analysis-820dc.appspot.com",
  messagingSenderId: "863565878024"
};
firebase.initializeApp(config);

function dropdownFunctionTopLevel() {
    document.getElementById("topLevelDropDown").classList.toggle("show");
}

function searchDatabase() {
  var data = firebase.database().ref.child('keywords').get();
}

function addNewElementToList(key, value) {
  var html =
    '<div class="singleItem">'+
    '<p>'+key+' : '+value+'</p'+
    '</div>';
    var div = document.createElement('div');
    div.innerHTML=html;

}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
