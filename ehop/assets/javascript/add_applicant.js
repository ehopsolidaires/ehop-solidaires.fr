geocoder = new google.maps.Geocoder();

var departAuto,arriveeAuto;

function initialize() {
    //Creation des champ auto-complete
    var input1 = document.getElementById('id_home-street');
    var input2 = document.getElementById('id_work-street');
    var options = {
        types: ['geocode'],
        componentRestrictions: {country: 'fr'}

    };
    departAuto = new google.maps.places.Autocomplete(input1, options);
    arriveeAuto = new google.maps.places.Autocomplete(input2, options);

    google.maps.event.addDomListener(input1, 'keydown', function(e) {
        if (e.keyCode == 13) {
            if (e.preventDefault){
                e.preventDefault();
            }
            else{
                e.cancelBubble = true;
                e.returnValue = false;
            }
        }
    });
    google.maps.event.addDomListener(input2, 'keydown', function(e) {
        if (e.keyCode == 13) {
            if (e.preventDefault){
                e.preventDefault();
            }
            else{
                e.cancelBubble = true;
                e.returnValue = false;
            }
        }
    });

    if(document.getElementById('id_work-street').value!='' && document.getElementById('id_home-street').value!=''){
        input1.placeholder=input1.value;
        input2.placeholder=input2.value;
    }
    document.getElementById('id_home-street').value='';
    document.getElementById('id_work-street').value='';

    //ajout listener sur l'adresse de depart
    google.maps.event.addListener(departAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(document.getElementById('id_work-street').value!=''){
            calcCoord(1);
            extract(1)
            traceRoute();
        }
        else {
            calcCoord(1);
            extract(1)
        }
    });

    //ajout listener sur l'adresse d'arrivee
    google.maps.event.addListener(arriveeAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(document.getElementById('id_home-street').value!=''){
            calcCoord(2);
            extract(2)
        }
        else {
            calcCoord(2);
            extract(2)
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);

/**
 * Calculate the coordinates
 * @param 1 for home
 *        2 for work
 **/
function calcCoord(type){
    if(type==1){
        var depart =document.getElementById("id_home-street").value;
        geocoder.geocode( { 'address': depart}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_home-latlng").setAttribute("value", results[0].geometry.location);
            }
            else{
                document.getElementById("id_home-latlng").setAttribute("value", "");
            }
        });
    }
    else if(type==2){
        var arrivee=document.getElementById("id_work-street").value;
        geocoder.geocode( { 'address': arrivee}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_work-latlng").setAttribute("value", results[0].geometry.location);
            }
            else{
                document.getElementById("id_work-latlng").setAttribute("value", "");
            }
        });
    }
}

/**
 * Extract city and zip code from the complete address
 * @param 1 for home
 *        2 for work
 */
function extract(type){
    //Champ autocompletion
    var place;
    var zipCode,city, street="";
    if(type==1) {
        var depart = document.getElementById("id_home-street").value;
        place=departAuto.getPlace().address_components;
    }
    else if(type==2){
        var arrivee=document.getElementById("id_work-street").value;
        place=arriveeAuto.getPlace().address_components;
    }

    //Recupere ville code postale
    for (var i = 0; i < place.length; i++) {
        var addressType = place[i].types[0];
        if (componentForm[addressType]) {
            var val = place[i][componentForm[addressType]];
            if(addressType=="route"||addressType=="street_number"){
                street+=val+" ";
            }
            if(addressType=="postal_code"){
                zipCode=val;
            }
            if(addressType=="locality"){
                city=val;
            }
        }
    }

    if(type==1) {
        document.getElementById("id_home-zipCodeHide").setAttribute("value", zipCode);
        document.getElementById("id_home-cityHide").setAttribute("value", city);
    }
    else if(type==2){
        document.getElementById("id_work-zipCodeHide").setAttribute("value", zipCode);
        document.getElementById("id_work-cityHide").setAttribute("value", city);
    }
}
$(function() {
    $("#id_carringAgency").on('change', function(){
        var typeAgency = $(this).val();
        if(typeAgency=="Pôle Emploi"){
            document.getElementById("ident").style.display = "Block";
        }else{
            document.getElementById("ident").style.display = "None";
        }
    })
});