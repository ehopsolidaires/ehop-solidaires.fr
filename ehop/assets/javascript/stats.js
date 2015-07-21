lang = {
    months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
    weekdays: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    downloadJPEG: "Télécharger au format JPG",
    downloadPDF: "Télécharger au format PDF",
    downloadPNG: "Télécharger au format PNG",
    downloadSVG: "Télécharger au format SVG",
    loading: "Chargement...",
    noData: "Aucune donnée à afficher",
    printChart: "Imprimer le graphique",
    decimalPoint: ","
}
panel_counter = 0;
chartDates = ["0","0"];
function drawGraph(id, update) {
    panel_container = document.getElementById("panel_container");
    panel = document.getElementById("panel-"+id);
    select_panel = document.getElementById("select-panel-"+id);
    if(select_panel != null){
        param = select_panel.value
    }else{
        param = ''
    }
    if(!update){
        if(panel_counter == 0){
            panel_container.innerHTML = generate_panel_html(id);
            init_inputDates(id);
            chartDates = ["0","0"];
            panel_container++;
        }else if(panel.style.display == "block"){
            panel.style.display = "none"
            panel_counter--;
        }else{
            panel.style.display = "block"
            panel_counter++;
        }
    }
    titleCOMCOM = "";
    titleDates = "";
    zipCode = $("#selectDept-panel-"+id).val();
    if($("#selectCOMCOM-panel-"+id).val() != "all" && zipCode == "35"){
        titleCOMCOM = "sur "+$("#selectCOMCOM-panel-"+id).val();
    }
    if(zipCode != "35"){
        titleCOMCOM = getDepartementName(zipCode);
        $('#selectCOMCOM-panel-'+id).hide();
    }else{
        $('#selectCOMCOM-panel-'+id).show();
    }
    checkChartDates = document.getElementById("checkChartDates")
    if(checkChartDates != null && !checkChartDates.checked){
        if($("#startDateChart-"+id).val() != "" && $("#endDateChart-"+id).val() != ""){
            titleDates = " entre le "+$("#startDateChart-"+id).val()+" et le "+$("#endDateChart-"+id).val();
        }else if($("#startDateChart-"+id).val() != ""){
            titleDates = " à partir du "+$("#startDateChart-"+id).val();
        }else if($("#endDateChart-"+id).val() != ""){
            titleDates = " avant le "+$("#endDateChart-"+id).val();
        }
    }
    if(id == 1){
        params = [document.getElementById("select-panel-"+id).value,
                document.getElementById("selectCOMCOM-panel-"+id).value,
                document.getElementById("selectDept-panel-"+id).value];
        chartDataUrl = "/BO/generate_chart/"+id+"/"+chartDates[0]+"_"+chartDates[1] +"/"+params[0]+"_"+params[1]+"_"+params[2];
        options = {
            chart: {
                renderTo: 'chart_panel-'+id,
                type: 'line'
            },
            credits: false,
            legend: {enabled: false},
            title: {text: "Inscriptions d'offreurs par "+param_to_FR(param)},
            subtitle: {text: titleCOMCOM+titleDates},
            xAxis: {title: {text: null}, labels: {rotation: -45}},
            yAxis: {title: {text: null}, floor:0},
            series: [{animation: true}],
            lang: lang
        };
    }else if(id == 2){
        params = [document.getElementById("select-panel-"+id).value,
                document.getElementById("selectCOMCOM-panel-"+id).value,
                document.getElementById("selectDept-panel-"+id).value];
        chartDataUrl = "/BO/generate_chart/"+id+"/"+chartDates[0]+"_"+chartDates[1] +"/"+ params[0]+"_"+params[1]+"_"+params[2];
        options = {
            chart: {
                renderTo: 'chart_panel-'+id,
                type: 'line'
            },
            credits: false,
            legend: {enabled: false},
            title: {text: "Inscriptions totales d'offreurs par "+param_to_FR(param)},
            subtitle: {text: titleCOMCOM+titleDates},
            xAxis: {title: {text: null}, labels: {rotation: -45}},
            yAxis: {title: {text: null}, floor:0},
            series: [{animation: true}],
            lang: lang
        };
    }else if(id == 3){
        params = [document.getElementById("selectCOMCOM-panel-" + id).value,
                document.getElementById("selectDept-panel-"+id).value]
        chartDataUrl = "/BO/generate_chart/"+id+"/"+chartDates[0]+"_"+chartDates[1]+"/"+params[0]+"_"+params[1];
        options = {
            chart: {
                renderTo: 'chart_panel-'+id,
                type: 'pie'
            },
            credits: false,
            legend: {enabled: false},
            title: {text: "Nombre d'offreurs et de demandeurs inscrits"},
            subtitle: {text: titleCOMCOM+titleDates},
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        format: '{point.name} : <b>{point.y}<b/>'
                    }
                }
            },
            series: [{
                type: 'pie',
                name: "Pourcentage",
                animation: true
            }],
            lang: lang
        };
    }else if(id == 4) {
        params = [document.getElementById("select-panel-" + id).value,
                document.getElementById("selectCOMCOM-panel-" + id).value,
                document.getElementById("selectDept-panel-"+id).value];
        chartDataUrl = "/BO/generate_chart/" + id + "/" +chartDates[0]+"_"+chartDates[1] + "/" + params[0] + "_" + params[1]+"_"+params[2] ;
        options = {
            chart: {
                renderTo: 'chart_panel-' + id,
                type: 'line'
            },
            credits: false,
            legend: {enabled: false},
            title: {text: "Désinscriptions d'offreurs par " + param_to_FR(param)},
            subtitle: {text: titleCOMCOM+titleDates},
            xAxis: {title: {text: null}, labels: {rotation: -45}},
            yAxis: {title: {text: null}, floor: 0},
            series: [
                {animation: true}
            ],
            lang: lang
        };
    }else if(id == 5){
        params = [document.getElementById("select-panel-" + id).value]
        chartDataUrl = "/BO/generate_chart/" + id + "/" + chartDates[0]+"_"+chartDates[1]+"/"+params[0];
        options = {
            chart: {
                renderTo: 'chart_panel-' + id,
                type: 'pie'
            },
            credits: false,
            legend: {enabled: false},
            title: {text: "Offreurs par "+param_to_FR(params[0])},
            subtitle: {text: titleDates},
            tooltip: {
                pointFormat: '{point.name}: <b>{point.percentage:.1f}%, {point.y}</b>'
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        formatter: function(){
                            if(this.y == 0)
                                return null;
                            return this.point.name+' : '+this.point.percentage.toFixed(1)+'%';

                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: "Inscris",
                animation: true
            }],
            lang: lang
        }
    }
    $.getJSON(chartDataUrl,
        function(data) {
            if(id == 1 || id == 2){
                options.xAxis.categories = data['chart_data']['date'];
                options.series[0].name = 'Inscrits à cette date ';
                options.series[0].data = data['chart_data']['counter'];
            }else if(id == 3) {
                options.series[0].data = [
                    ['Offreurs',data['chart_data']['providers']],
                    ['Demandeurs',data['chart_data']['applicants']]
                ];
            }else if(id == 4){
                options.xAxis.categories = data['chart_data']['date'];
                options.series[0].name = 'Désinscrits à cette date ';
                options.series[0].data = data['chart_data']['counter'];
            }else if(id == 5){
                options.series[0].data = data['chart_data'];
            }
            var chart = new Highcharts.Chart(options);
        });
};

function getDepartementName(zipCode){
    console.log(zipCode)
    if(zipCode == 29)
        return "dans le Finistère";
    if(zipCode == 56)
        return "dans le Morbihan";
}

function checkDates(id){
    checked = document.getElementById("checkChartDates").checked;
    if(checked){
        document.getElementById("chartDates").style.display = "none";
        chartDates = ["0","0"];
    }else{
        document.getElementById("chartDates").style.display = "inline-block";
        start = $('#startDateChart-'+id).datepicker("getDate")
        end = $('#endDateChart-'+id).datepicker("getDate")
        if(start == null)
            start = "0";
        else
            start = getDateFormatted(start);
        if(end == null)
            end = "0";
        else
            end = getDateFormatted(end);
        chartDates = [start ,end];
    }
    drawGraph(id,true);
}

function updateChartDates(id){
    start = $('#startDateChart-'+id).datepicker("getDate");
    end = $('#endDateChart-'+id).datepicker("getDate");
    if(start == null)
        start = "0";
    else
        start = getDateFormatted(start);
    if(end == null)
        end = "0";
    else
        end = getDateFormatted(end);
    chartDates = [start ,end];
    drawGraph(id,true)
}

function generate_download_csv(id, param){
    return '<a id="downloadCSV" href="/BO/generate_csv/'+id+'/'+param+'">Télécharger le fichier CSV</a>'
}

function param_to_FR(param){
    if(param == 'day')
        return 'jour';
    if(param == 'week')
        return 'semaine';
    if(param == 'month')
        return 'mois';
    if(param == 'year')
        return 'année';
    if(param == 'COMCOM')
        return 'COMCOM'
    if(param == 'firm')
        return 'entreprises'
    if(param == 'adfirm')
        return 'entreprises adhérentes'
}

baseProviderUrl = "/BO/generate_csv/4/";
providerDates = ["0","0"];
providerParams = "";
providerButton = document.getElementById("providerCSV");

baseApplicantUrl = "/BO/generate_csv/5/";
applicantDates = ["0","0"];
applicantParams = "";
applicantButton = document.getElementById("applicantCSV");

baseMERUrl = "/BO/generate_csv/6/"
MERDates = ["0","0"]
MERButton = document.getElementById("MERCSV");

baseUnsubUrl = "/BO/generate_csv/7/"
unsubDates = ["0","0"]
unsubButton = document.getElementById("unsubCSV");
function updateProviderUrl(field){
    if(field=='all'){
        box = document.getElementById(field+"Provider");
        if(box.checked){
            providerButton.href = generateUrl(baseProviderUrl,providerDates,"")
            document.getElementById("providerFieldsDiv").style.display = "none";
        }else{
            providerButton.href = generateUrl(baseProviderUrl,providerDates,providerParams)
            document.getElementById("providerFieldsDiv").style.display = "block";
        }
    }else{
        box = document.getElementById(field+"Provider")
        if(box.checked){
            providerParams = providerParams.replace(field+"_","");
            providerButton.href = providerButton.href.replace(field+"_","");
        }else{
            providerParams += field+"_";
            providerButton.href += field+"_";
        }
    }
}
function updateApplicantUrl(field){
    if(field=='all'){
        box = document.getElementById(field+"Applicant");
        if(box.checked){
            applicantButton.href = generateUrl(baseApplicantUrl,applicantDates,"")
            document.getElementById("applicantFieldsDiv").style.display = "none";
        }else{
            applicantButton.href = generateUrl(baseApplicantUrl,applicantDates,applicantParams)
            document.getElementById("applicantFieldsDiv").style.display = "block";
        }
    }else{
        box = document.getElementById(field+"Applicant")
        if(box.checked){
            applicantParams = applicantParams.replace(field+"_","");
            applicantButton.href = applicantButton.href.replace(field+"_","");
        }else{
            applicantParams += field+"_";
            applicantButton.href += field+"_";
        }
    }
}

function showHide(id,type){
    e = document.getElementById(id+type);
    if(e.style.display == "block"){
        e.style.display = "none";
        if(id == "startDate"){
            if(type=="Provider") providerDates[0] = "0";
            else if(type=="Applicant") applicantDates[0] = "0"
            else if(type=="MER") MERDates[0] = "0"
            else if(type=="Unsub") unsubDates[0] = "0"
        }else{
            if(type=="Provider") providerDates[1] = "0";
            else if(type=="Applicant") applicantDates[1] = "0"
            else if(type=="MER") MERDates[1] = "0"
            else if(type=="Unsub") unsubDates[1] = "0"
        }
        if(type=="Provider") providerButton.href = generateUrl(baseProviderUrl,providerDates,providerParams)
        else if(type=="Applicant") applicantButton.href = generateUrl(baseApplicantUrl,applicantDates,applicantParams)
        else if(type=="MER") MERButton.href = generateUrl(baseMERUrl,MERDates,"")
        else if(type=="Unsub") unsubButton.href = generateUrl(baseUnsubUrl,unsubDates,"")
    }else{
        e.style.display = "block";
        if(e.value != ""){
            updateDates(id,type);
        }
    }
}

function updateDates(id,type){
    e = $('#'+id+type).datepicker("getDate");
    s = getDateFormatted(e)
    if(id.indexOf("start") > -1){
        if(type=="Provider") providerDates[0] = s;
        else if(type=="Applicant") applicantDates[0] = s;
        else if(type=="MER") MERDates[0] = s;
        else if(type=="Unsub") unsubDates[0] = s;
    }else{
        if(type=="Provider") providerDates[1] = s;
        else if(type=="Applicant") applicantDates[1] = s;
        else if(type=="MER") MERDates[1] = s;
        else if(type=="Unsub") unsubDates[1] = s;
    }
    if(type=="Provider") providerButton.href = generateUrl(baseProviderUrl,providerDates,providerParams);
    else if(type=="Applicant") applicantButton.href = generateUrl(baseApplicantUrl,applicantDates,applicantParams);
    else if(type=="MER") MERButton.href = generateUrl(baseMERUrl,MERDates,"");
    else if(type=="Unsub") unsubButton.href = generateUrl(baseUnsubUrl,unsubDates,"");
}

function getDateFormatted(date){
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth()+1).toString();
    var dd  = date.getDate().toString();
    return (dd[1]?dd:"0"+dd[0]) + (mm[1]?mm:"0"+mm[0]) + yyyy;
}

function generateUrl(base, dates, params){
    return base+dates[0]+"_"+dates[1]+"/"+params;
}