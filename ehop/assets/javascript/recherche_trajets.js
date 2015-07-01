// JavaScript Document

//Variable globale pour la map
//Affichage du trajet
var directionsDisplay;
//affichage de la carte
var map;
//Calcul sur le trajet
var directionsService=new google.maps.DirectionsService();
//Outil permettant de convertir une adresse en coordonnee
geocoder = new google.maps.Geocoder();
//Champ autocompletion
var departAuto,arriveeAuto;

function initialize() {
    var mapCanvas = document.getElementById('map_canvas');

    //Option de la map
    var mapOptions = {
        center: new google.maps.LatLng(48.117266, -1.6777925999999752),
        zoom: 9,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    //Creation de la map
    map = new google.maps.Map(mapCanvas, mapOptions)

    //Outil permettant de calculer un trajet
    directionsService = new google.maps.DirectionsService();

    //Outil permettant d'afficher un trajet
    var rendererOptions = {
        draggable: true
    };

    directionsDisplay=new google.maps.DirectionsRenderer();	//Passer rendererOptions en aprametre pour rendre le trajet modifiable

    //Creation des champ auto-complete
    var input1 = document.getElementById('id_departure');
    var input2 = document.getElementById('id_arrival');
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
    directionsDisplay.setMap(map);

    //Draw the path if you refresh the page and old values have been saved
    if(input1.value.trim && input2.value.trim){
        calcCoord(1);
        calcCoord(2);
        traceRoute();
    }

    //ajout listener sur l'adresse de depart
    google.maps.event.addListener(departAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(document.getElementById('id_arrival').value!=''){
            calcCoord(1);
            traceRoute();
        }
        else {
            calcCoord(1);
        }
    });

    //ajout listener sur l'adresse d'arrivee
    google.maps.event.addListener(arriveeAuto, 'place_changed', function() {
        //Si l'adresse 2 est deja rempli, on trace la route
        if(document.getElementById('id_departure').value!=''){
            calcCoord(2);
            traceRoute();
        }
        else {
            calcCoord(2);
        }
    });
}
google.maps.event.addDomListener(window, 'load', initialize);

//fonction qui tracera la route
function traceRoute(){
    var depart =document.getElementById("id_departure").value;
    var arrivee=document.getElementById("id_arrival").value;

    var request = {
        origin: depart,
        destination: arrivee,
        travelMode: google.maps.TravelMode.DRIVING
    };
    //On fait appel au service de google map permettant le calcul des trajets avec sa méthode route
    directionsService.route(request, function(response, status) {
        if(status==google.maps.DirectionsStatus.OK){
            //On passe le trajet calculer a l'objet permettant l'affichage
            directionsDisplay.setDirections(response);
        }else{

        }
    });

}

/**
 * Calculate the coordinates
 * @param 1 for home
 *        2 for work
 **/
function calcCoord(type){
    if(type==1){
        var depart =document.getElementById("id_departure").value;
        geocoder.geocode( { 'address': depart}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_departure_latlng").setAttribute("value", results[0].geometry.location);
            }
            else{
                document.getElementById("id_departure_latlng").setAttribute("value", "");
            }
        });
    }
    else if(type==2){
        var arrivee=document.getElementById("id_arrival").value;
        geocoder.geocode( { 'address': arrivee}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                document.getElementById("id_arrival_latlng").setAttribute("value", results[0].geometry.location);
            }
            else{
                document.getElementById("id_arrival_latlng").setAttribute("value", "");
            }
        });
    }

}

CST_temps_entre_chaque_detour=0
CST_temps_avant_reessai=100
listePath = []
globalDemandDepart=""
globalDemandArrivee=""
globalOffreurDepart=""
globalOffreurArrivee=""

function addPath(depart,arrivee,id){
    path = {
        origin:depart,
        destination:arrivee,
        id:id
    };

    listePath.push(path);
}

function calcAllDetour(demandAdDepart, demandAdArrivee){
    if (listePath.length>0) {
        var path = listePath.shift();
        globalDemandArrivee = demandAdArrivee;
        globalDemandDepart = demandAdDepart;
        globalOffreurDepart = path.origin;
        globalOffreurArrivee = path.destination;
        console.log(globalDemandDepart+"\n"+globalDemandArrivee+"\n"+globalOffreurDepart+"\n"+globalOffreurArrivee+"\n");
        calcDetour(path.origin, path.destination, demandAdDepart, demandAdArrivee, path.id)
    }
}
/**
 * @param:
 *  offreurAdDepart:    adresse depart de l'offreur
 *  offreurAdArrivee:   adresse arrivee de l'offreur
 *  demandAdDepart:     adresse depart ddu demandeur
 *  demandAdArrivee:    adresse arrivee du demandeur
 *  numero:             numero du trajet
 */
function calcDetour(offreurAdDepart, offreurAdArrivee, demandAdDepart, demandAdArrivee, numero){
    directionsService = new google.maps.DirectionsService();
    calculDurationOffreur(offreurAdDepart,offreurAdArrivee, demandAdDepart, demandAdArrivee, numero);
}

/**
* Calcul de la durée d'un trajet d'un offreur
*/
function calculDurationOffreur(start,finish,demandAdDepart, demandAdArrivee, numero){
    var request = {
        origin: start,
        destination: finish,
        travelMode: google.maps.TravelMode.DRIVING
    };
    directionsService.route(request, callBCackCalculDuration(start,finish,demandAdDepart, demandAdArrivee, numero));
}

function callBCackCalculDuration(start,finish,demandAdDepart, demandAdArrivee, numero){
    return function(response,status){
        var done = false;
        var delay = CST_temps_avant_reessai
            if (status == google.maps.DirectionsStatus.OK) {
                done=true;
                var totalTime = 0;
                var totalDist = 0;
                var myroute = response.routes[0].legs[0];
                for (i = 0; i < myroute.steps.length; i++) {
                    totalTime += myroute.steps[i].duration.value;
                    totalDist += myroute.steps[i].distance.value;
                }
                calcDiff(start, finish, demandAdDepart, demandAdArrivee, totalTime, totalDist, numero)
            }
            else {
                console.log(status+" number: "+numero+" duree: "+delay);
                sleep(delay)
                calculDurationOffreur(start,finish,demandAdDepart, demandAdArrivee, numero)
                /*var path={
                    origin: start,
                    destination: finish,
                    id: numero
                };
                listePath.push(path);
                calcAllDetour(globalDemandDepart,globalDemandArrivee)*/
            }
    }
}

/**
 * fonction qui calcule le detour
 * @param start point par lequel le trajet devra passer
 * @param finish point par lequel le point devra passer en second
 * @param totalTime temps de base du trajet sans le detour
 * @param totalDist distance totale du trajet
 */
        function calcDiff(start,finish,demandAdDepart, demandAdArrivee,totalTime,totalDist, numero){
        var waypts=[];
		waypts.push({
			location: demandAdDepart,
			stopover:false
		});

		waypts.push({
			location: demandAdArrivee,
			stopover:false
		});

				var request = {
				origin: start,
				destination: finish,
				waypoints: waypts,
				optimizeWaypoints: true,
				travelMode: google.maps.TravelMode.DRIVING
			};
				//On fait appel au service de google map permettant le calcul des trajets avec sa méthode route
				directionsService.route(request, callback(totalTime,totalDist, numero));
        }

    function callback(duration,distance, numero){
		return function(response, status) {
            var done=false;
            var delay=CST_temps_avant_reessai;
				if(status==google.maps.DirectionsStatus.OK){
                    done=true;
					//On passe le trajet calculer a l'objet permettant l'affichage
					calcul(response,duration, distance, numero);
				}
				else{
					console.log("Erreur Api GOOGLE, veuillez reessayer. Code erreur: "+status+" numero: "+numero+" duree: "+delay);
                    sleep(delay)
                    calcDiff(globalOffreurDepart,globalOffreurArrivee,globalDemandDepart, globalDemandArrivee,duration,distance, numero)
                        /*var path={
                            origin: start,
                            destination: finish,
                            id: numero
                        };
                        listePath.push(path);
                        calcAllDetour(globalDemandDepart,globalDemandArrivee)*/
				}
            }
	}

    function calcul(response,initialDuration,initialDistance, numero){
		var totalTime = 0;
        var totalDist=0;
		var myroute = response.routes[0].legs[0];
		for (i = 0; i < myroute.steps.length; i++) {
			totalTime += myroute.steps[i].duration.value;
            totalDist += myroute.steps[i].distance.value;
		}
		totalTime=totalTime-initialDuration;
        totalDist=totalDist-initialDistance;
		var duree=convertTime(totalTime);
        var distance=totalDist/1000;
        document.getElementById("id_"+numero+"-0-detourkm").value=distance+"km";
        document.getElementById("id_"+numero+"-0-detour").value=duree[0]+"h "+duree[1]+"min "+duree[2]+"s";
        var distancekm = Math.trunc(distance);
        var temps=""
        if(duree[0].length > 0)
            temps += duree[0]+"h "+duree[1]+"min";
        else
            temps += duree[1]+"min";
        document.getElementById("id_"+numero+"-0-detourboth").value=distancekm+"km/"+temps;
        if(listePath.length>0){
            sleep(CST_temps_entre_chaque_detour)
            calcAllDetour(globalDemandDepart,globalDemandArrivee)
        }
	}

		/**
		  * Fonction qui converti un temps en seconde, en heure minute seconde
		 */
		function convertTime(detour){
			var time=[];
			time.push(parseInt(detour/3600));
			time.push(parseInt((detour%3600)/60));
			time.push((detour%3600)%60);
			return time;
		}

function checkForm() {
    var date = document.getElementById("id_date");
    if(date.value == ""){
        document.getElementsByClassName("xdsoft_datetimepicker")[0].style.backgroundColor = "#F04124";
        return false;
    }else{
        document.getElementsByClassName("xdsoft_datetimepicker")[0].style.backgroundColor = "#FFF";
    }
}
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function clean(string){
    s = string.replace(', France','').split(',');
    if(s.length > 1)
        return s[1]
    else
        return s[0]
}