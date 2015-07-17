/**
 *
 * @copyright (C) 2014-2015
 * Developpeurs " BARDOU AUGUSTIN - REZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
 *                MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN "
 * @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3
 *
 */

// JavaScript Document
$(document).ready(function () {
    $('input[type=checkbox]').each(function () {
        this.checked = false;
    });
    $(".page1").hide();
    $(".page3").hide();

});


$(function () {
    $("#Button3").click(function (e) {
        //calculate again the coordinate
        calcCoord(1);
        if(checkNonFixe.checked){
            for (i=1;i<=inputCounter;i++){
                calcCoord(2,""+i);
            }
        }else{
            calcCoord(2);
        }
        console.log("timeout");
        setTimeout(checkAddresses, 100);
        console.log("timein");
        return false;
    });
});

function checkAddresses(){
    OK = true;
    street = document.getElementById("id_home-street").value.trim();
    latlng = document.getElementById("id_home-latlng").value.trim();
    if (street == "" || latlng == ""){
        OK = false;
        document.getElementById("errorHome").style.display = "block";
        document.getElementById("id_home-street").style.marginBottom = "0px";
    }else{
        document.getElementById("errorHome").style = "";
        document.getElementById("id_home-street").style.marginBottom = "1rem";
    }
    if(checkNonFixe.checked){
        for (i=1;i<=inputCounter;i++){
            street = document.getElementById("id_work"+i+"-street").value.trim();
            latlng = document.getElementById("id_work"+i+"-latlng").value.trim();
            if (street == "" || latlng == ""){
                OK = false;
                document.getElementById("errorWork"+i).style.display = "block";
                document.getElementById("id_work"+i+"-street").style.marginBottom = "0px";
            }else{
                document.getElementById("errorWork"+i).style.display = "none";
                document.getElementById("id_work"+i+"-street").style.marginBottom = "1rem";
            }
        }
        if(!OK)
            return false;
    }else{
       calcCoord(2);
        street = document.getElementById("id_work-street").value.trim();
        latlng = document.getElementById("id_work-latlng").value.trim();
        if (street == "" || latlng == ""){
            document.getElementById("errorWork").style.display = "block";
            document.getElementById("id_work-street").style.marginBottom = "0px";
            return false;
        }else{
            document.getElementById("errorWork").style.display = "none";
            document.getElementById("id_work-street").style.marginBottom = "1rem";
        }
    }
    $(".page2").hide();
    $("#state_menu").attr("src", "/assets/images/Barre_2.png")
    $(".page1").show();
    if(checkNonFixe.checked){
        $('#nonFixePlanning').show();
        $('#regularPlanning').hide();
    }else{
        $('#nonFixePlanning').hide();
        $('#regularPlanning').show();
    }
    return false;
}

$(function () {
    $("#Button4").click(function () {
        var sexChecked = document.getElementById("id_sex_0").checked || document.getElementById("id_sex_1").checked;
        var name = document.getElementById("id_name").value;
        var firstname = document.getElementById("id_firstname").value;
        var mail = document.getElementById("id_mail").value;
        var mail2 = document.getElementById("id_mail2").value;
        var pass = document.getElementById("password").value;
        var pass2 = document.getElementById("password2").value;
        var phone = document.getElementById("id_phone").value;
        var zip = document.getElementById("id_zipCode").value;
        var city = document.getElementById("id_city").value;
        if(!sexChecked
            || !name.trim()
            || !firstname.trim()
            || !mail.trim() || !mail.match(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/)
            || !mail2.trim() || !mail2.match(/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/) || mail2 != mail
            || !pass.trim()
            || (!pass2.trim() || pass2 != pass)
            || !phone.trim() || !phone.match(/^0[0-9]{9}$/)
            || !zip.trim() ||!zip.match(/^[0-9]{5}$/)
            || !city.trim()){

            inputs = $('#form_civ :input');
            Foundation.libs.abide.validate(inputs, {type:''});
        }
        else{
            $(".page1").hide();
            $("#state_menu").attr("src", "/assets/images/Barre_3.png")
            $(".page3").show();
        }
        return false;
    });
});

$(function () {
    $("#Button5").click(function () {
        $(".page1").hide();
        $("#state_menu").attr("src", "/assets/images/Barre_1.png")
        $(".page2").show();
        var center = map.getCenter();
        google.maps.event.trigger(map, "resize");
        map.setCenter(center);
        return false;
    });
});

$(function () {
    $("#Button6").click(function () {
        $(".page2").hide();
        $(".page3").hide();
        $("#state_menu").attr("src", "/assets/images/Barre_2.png")
        $(".page1").show();
        return false;
    });
});

function initCalendar() {
    //initialize the calendar to today
    var date = new Date();
    day = date.getDate()
    if (day < 10) {
        day = "0" + day;
    }
    month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    document.getElementById('dp').value = day + "/" + month + "/" + date.getFullYear();
    updateWeek();
}

function updateWeek() {
    var dateString = document.getElementById('dp').value;
    var d = parseInt(dateString.substring(0, 2));
    var m = parseInt(dateString.substring(3, 5));
    var y = parseInt(dateString.substring(6, 10));
    var date = new Date(y, m - 1, d);
    document.getElementById('week').value = date.getWeek();
}

//Variable globale pour la map
//Affichage du trajet
var directionsDisplay;
//affichage de la carte
var map;
//Calcul sur le trajet
var directionsService;
//Outil permettant de convertir une adresse en coordonnee
geocoder = new google.maps.Geocoder();
//Permet d'extraire des infos d'une adresse
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};
//Champ autocompletion
var departAuto, arriveeAuto, arriveeAuto1, arriveeAuto2, arriveeAuto3, arriveeAuto4, arriveeAuto5;
var inputH, inputW, inputW1, inputW2, inputW3, inputW4;
var checkNonFixe, marker, homelatlng;
var inputCounter = 3;

function initialize() {
    var mapCanvas = document.getElementById('map_canvas');

    //Option de la map
    var mapOptions = {
        center: new google.maps.LatLng(48.117266, -1.6777925999999752),
        zoom: 9,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    //Creation de la map
    map = new google.maps.Map(mapCanvas, mapOptions)

    //Outil permettant de calculer un trajet
    directionsService = new google.maps.DirectionsService();

    //Outil permettant d'afficher un trajet
    var rendererOptions = {
        draggable: true
    };

    directionsDisplay=new google.maps.DirectionsRenderer();	//Passer rendererOptions en parametre pour rendre le trajet modifiable
    initWorkInputs();

    //Creation des champ auto-complete
    inputH = document.getElementById('id_home-street');
    inputW = document.getElementById('id_work-street');
    inputW1 = document.getElementById('id_work1-street');
    inputW2 = document.getElementById('id_work2-street');
    inputW3 = document.getElementById('id_work3-street');
    inputW4 = document.getElementById('id_work4-street');
    inputW5 = document.getElementById('id_work5-street');
    checkNonFixe = document.getElementById('checkNonFixe')
    var options = {
        types: ['geocode'],
        componentRestrictions: {country: 'fr'}
    };
    departAuto = new google.maps.places.Autocomplete(inputH, options);
    arriveeAuto = new google.maps.places.Autocomplete(inputW, options);
    arriveeAuto1 = new google.maps.places.Autocomplete(inputW1, options);
    arriveeAuto2 = new google.maps.places.Autocomplete(inputW2, options);
    arriveeAuto3 = new google.maps.places.Autocomplete(inputW3, options);
    arriveeAuto4 = new google.maps.places.Autocomplete(inputW4, options);
    arriveeAuto5 = new google.maps.places.Autocomplete(inputW5, options);

    addListener(inputH);
    addListener(inputW);
    addListener(inputW1);
    addListener(inputW2);
    addListener(inputW3);
    addListener(inputW4);
    addListener(inputW5);

    directionsDisplay.setMap(map);
    marker = new google.maps.Marker( {map: map} );

    //Draw the path if you refresh the page and old values have been saved
    if(document.getElementById('id_work-street').value!='' && document.getElementById('id_home-street').value!=''){
        inputH.placeholder=inputH.value;
        inputW.placeholder=inputW.value;
    }

    document.getElementById('id_home-street').value='';
    document.getElementById('id_work-street').value='';

    //ajout listener sur l'adresse de depart
    google.maps.event.addListener(departAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(!checkNonFixe.checked && document.getElementById('id_work-street').value!=''){
            calcCoord(1);
            extract(1);
            traceRoute();
        }
        else if(checkNonFixe.checked) {
            calcCoord(1);
            extract(1);
            placeHomeMarker();
        }else{
            calcCoord(1);
            extract(1);
        }
    });

    //ajout listener sur l'adresse d'arrivee
    google.maps.event.addListener(arriveeAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(document.getElementById('id_home-street').value!=''){
            calcCoord(2);
            extract(2)
            traceRoute();
        }
        else {
            calcCoord(2);
            extract(2)
        }
    });
    google.maps.event.addListener(arriveeAuto1, 'place_changed', function() {
        calcCoord(2,"1");
    });
    google.maps.event.addListener(arriveeAuto2, 'place_changed', function() {
        calcCoord(2,"2");
    });
    google.maps.event.addListener(arriveeAuto3, 'place_changed', function() {
        calcCoord(2,"3");
    });
    google.maps.event.addListener(arriveeAuto4, 'place_changed', function() {
        calcCoord(2,"4");
    });
    google.maps.event.addListener(arriveeAuto5, 'place_changed', function() {
        calcCoord(2,"5");
    });
}
google.maps.event.addDomListener(window, 'load', initialize);

function placeHomeMarker(){
    var depart = document.getElementById("id_home-street").value;
    geocoder.geocode({'address': depart}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            homelatlng = results[0].geometry.location;
            map.setCenter(homelatlng);
            map.setZoom(10);
            marker.setMap(map)
            marker.setPosition(homelatlng);
            directionsDisplay.setMap(null);
        }else{
            homelatlng = null
        }
    });
}

function addListener(input){
    google.maps.event.addDomListener(input, 'keydown', function(e) {
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
}

function initWorkInputs(){
    $('#inputCounter').val(inputCounter);
    for(i=5;i>inputCounter;i--){
        $('#work' + i).hide();
        $('#work' + i).disabled = true;
    }
}

//fonction qui tracera la route
function traceRoute(){
    var depart =document.getElementById("id_home-street").value;
    var arrivee=document.getElementById("id_work-street").value;

    var request = {
        origin: depart,
        destination: arrivee,
        travelMode: google.maps.TravelMode.DRIVING
    };
    directionsDisplay.setMap(map);
    marker.setMap(null)
    //On fait appel au service de google map permettant le calcul des trajets avec sa méthode route
    directionsService.route(request, function(response, status) {
        if(status==google.maps.DirectionsStatus.OK){
            //On passe le trajet calculer a l'objet permettant l'affichage
            directionsDisplay.setDirections(response);
        }else{

        }
    });
}

function account_path(){
    if(document.getElementById('id_work-street').placeholder!='Indiquez un lieu' && document.getElementById('id_home-street').placeholder!='Indiquez un lieu'){
        document.getElementById('id_home-street').value=document.getElementById('id_home-street').placeholder;
        document.getElementById('id_work-street').value=document.getElementById('id_work-street').placeholder;
        traceRoute();
        calcCoord(1);
        calcCoord(2);
    }
}

function initialize_applicant(){
    if(document.getElementById('id_work-street').placeholder!='Indiquez un lieu' && document.getElementById('id_home-street').placeholder!='Indiquez un lieu'){
        document.getElementById('id_home-street').value=document.getElementById('id_home-street').placeholder;
        document.getElementById('id_work-street').value=document.getElementById('id_work-street').placeholder;
        calcCoord(1);
        calcCoord(2);
    }
}

$(function() {
    $( "#selectSemaine" ).on('change', function(){
        var typeSemaine = $(this).val();
        $("#Tabs1").children().filter("div").not("#tabs-1").remove();
        $("#semaine").children().not("#premiere").remove();
        $("#Tabs1").tabs("refresh");
        nb_semaine = 1;
        if(typeSemaine == "Fixe"){
        }
        else if(typeSemaine == "2*8"){
            ajouterSemaine('B');
        }
        else if(typeSemaine == "3*8"){
            ajouterSemaine('B');
            ajouterSemaine('C');
        }
        else{
            ajouterBouttonsAutre();
        }

        return false;
    });
});

/*
 * Function that initialize the calendar to the Semaine 1
 * @param number of date to add
 *      -Semaine A: 0 day to add
 *      -Semaine B: 14 days to add
 *      -Semaine C: 7 days to add
 */
function initCalendarOADate(numberOfDay){
    //initialize the calendar to a date
    var date = new Date();
    date.setDate(date.getDate()+numberOfDay);
    day = date.getDate()
    if(day < 10){
        day = "0"+day;
    }
    month = date.getMonth()+1;
    if(month < 10){
        month = "0"+month;
    }
    document.getElementById('dp').value = day + "/" + month + "/" + date.getFullYear();
    updateWeek();
}

/**
 * Calculate the coordinates
 * @param 1 for home
 *        2 for work
 **/
function calcCoord(type, id) {
    id = id || '';
    if (type == 1) {
        var depart = document.getElementById("id_home-street").value;
        geocoder.geocode({ 'address': depart}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_home-latlng").setAttribute("value", results[0].geometry.location);
            }
            else {
                document.getElementById("id_home-latlng").setAttribute("value", "");
            }
        });
    }
    else if (type == 2) {
        input = "id_work"+id;
        var arrivee = document.getElementById(input+"-street").value;
        geocoder.geocode({ 'address': arrivee}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById(input+"-latlng").setAttribute("value", results[0].geometry.location);
                console.log(input+" : "+results[0].geometry.location)
            }
            else {
                document.getElementById(input+"-latlng").setAttribute("value", "");
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
    $( "#selectSemaine" ).on('change', function(){
        var typeSemaine = $(this).val();
        $("#Tabs1").children().filter("div").not("#tabs-1").remove();
        $("#semaine").children().not("#premiere").remove();
        $("#Tabs1").tabs("refresh");
        nb_semaine = 1;
        if(typeSemaine == "Fixe"){
        }
        else if(typeSemaine == "2*8"){
            ajouterSemaine('B');
        }
        else if(typeSemaine == "3*8"){
            ajouterSemaine('B');
            ajouterSemaine('C');
        }
        else{
            ajouterBouttonsAutre();
        }

        return false;
    });
});

function checkSchedule(){
    if(!checkNonFixe.checked){
        var hasSchedule = document.querySelector('[id*="-schedule"]') != null;
        if(!hasSchedule){
            document.getElementById('errorSchedule').style.display = 'block';
            return false;
        }
        return true;
    }else{
        dayButtons = $("[id^='dayButton']")
        for(i=0; i<dayButtons.length;i++){
            if(dayButtons[i].getAttribute("status") == "on"){
                return true;
            }
        }
        document.getElementById('errorSchedule2').style.display = 'block';
        return false;
    }
}

Date.prototype.getWeek = function() {
    var date = new Date(this.getTime());
    date.setHours(0, 0, 0, 0);
    // Thursday in current week decides the year.
    date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
    // January 4 is always in week 1.
    var week1 = new Date(date.getFullYear(), 0, 4);
    // Adjust to Thursday in week 1 and count number of weeks from date to week1.
    return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7); }
