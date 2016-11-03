 $( document ).ready(function(){
 	 $(".button-collapse").sideNav();
     self_classification = document.getElementById('select-self_classification');
     if (self_classification){
         if(document.getElementById('select-self_classification').options[self_classification.selectedIndex].value == "other"){
             self_classification.onchange();
         }
     }

 });
