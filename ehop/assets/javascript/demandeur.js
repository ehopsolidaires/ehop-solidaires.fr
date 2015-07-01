var map;
var providers=[];
var directionsService;
var directionsDisplay;

function initialize() {
    directionsService = new google.maps.DirectionsService();
    var mapOptions = {
        center: new google.maps.LatLng(48.117266, -1.6777925999999752),
        zoom: 7,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true
    }
    google.maps.Marker.visible = false;
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    initializeProviders();
}

function initializeProviders(){
    var nb = document.getElementById('sizeQS').value;
    for(var i=11;i<nb; i+=2){
        var depart = document.getElementById(''+i).value;
        var j = i+1;
        var arrivee = document.getElementById(''+j).value;
        depart = depart.split(',')
        arrivee = arrivee.split(',')
        addPathToProviders(new google.maps.LatLng(depart[0], depart[1]),new google.maps.LatLng(arrivee[0], arrivee[1]));
    }
    for(var i=0;i<providers.length;i++){
        drawRoute(providers[i].start,providers[i].finish,providers[i].directions);
    }
}

function addPathToProviders(start,finish){
    var path = {
        start: start,		//Point de depart
        finish: finish,		//Point darrivee
        directions: new google.maps.DirectionsRenderer({suppressMarkers: true})	//Option pour le trajet
    };
    providers.push(path);
}

function drawRoute(start,finish,direction){
    direction.setMap(map);
    //Creation de la requete
    var request = {
        origin: start,
        destination: finish,
        travelMode: google.maps.TravelMode.DRIVING
    };

    //On fait appel au service de googlemap
    //metohode route prend en parametre:
    //la requete et une fonction callback
    directionsService.route(request,function(response,status){
        //Si la requete a pu etre correctement effectu�
        if(status==google.maps.DirectionsStatus.OK){
            direction.setDirections(response);
        }
    });
}

function callback(trajet,duration){

    return function(response, status) {
        if(status==google.maps.DirectionsStatus.OK){
            //On passe le trajet calculer a l'objet permettant l'affichage
            calcul(response,duration,trajet);
        }
        else{
            alert(status);
        }
    }
}

google.maps.event.addDomListener(window, 'load', initialize);
