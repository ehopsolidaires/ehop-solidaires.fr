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
}

google.maps.event.addDomListener(window, 'load', initialize);