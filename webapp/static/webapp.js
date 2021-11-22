/* Emily Litton and Jayti Arora
    webapp.js
    November 11, 2021 

    Adopted from books.js
    Jeff Ondich, 27 April 2016
    Updated, 5 November 2020
 */

window.onload = initialize;

function initialize() {
    loadCountriesSelector();
    initializeMap();
    
    let element = document.getElementById('graph_button');
    if (element) {
        element.onclick = createChartOnClick;
    }
    let selector = document.getElementById('country_selector');
    if (selector) {
        selector.onchange = onCountiresSelectionChanged;
    }
}

// Returns the base URL of the API
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/';
    return baseURL;
}

//Displays information from selector
function loadCountriesSelector() {
    let url = getAPIBaseURL() + 'countries/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(countries) {
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        selectorBody += '<option value = "0">--</option>\n'
        for (let k = 0; k < countries.length; k++) {
            let country = countries[k];
            selectorBody += '<option value="' + country['id'] + '">'
                                 + country['country_name']
                                 + '</option>\n';
        }

        let selector = document.getElementById('country_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onCountiresSelectionChanged() {
    // calls a function to display information for the country selected
    displayCountryInfo(this.value);
} 

function initializeMap() {
    /* Calls the api to assign colors to different countries based on happiness and draws map */
     let url = getAPIBaseURL() + 'countries/happiness';

     fetch(url, {method: 'get'})

     .then((response) => response.json())
     .then(function(happiness_scores){
        countryInfo = {};
        for (const [abbreviation, value] of Object.entries(happiness_scores)) {
            var color; 

            if(value < 4.2){
                color = "#C3FFF9"; //lightest
            }else if(value < 5.4){
                color = "#82BCBC"; //mid 1
            }else if(value < 6.6){
                color = "#447C81"; //mid 2
            }else{
                color = "#00424B"; //darkest
            }
            
            countryInfo[abbreviation] = {"fillColor":color};
          }
    
        var page_map = document.getElementById('map-container');
        if (page_map){ 
            console.log(countryInfo) 
            var map = new Datamap({ element: page_map, 
                                    scope: 'world', 
                                    projection: 'equirectangular', // 'mercator' is also an option
                                    done: onMapDone, // once the map is loaded, call this function
                                    data: countryInfo, // here's some data that will be used by the popup template
                                    fills: { defaultFill: '#999999' }, // fill if another fill not specified
                                    geographyConfig: {
                                        popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                        borderColor: '#eeeeee', // country border color
                                        highlightFillColor: 'beige', //'#99dd99',  color when you hover on a country
                                        highlightBorderColor: '#000000', // border color when you hover on a country
                                    }
                                });
        };
    
     })
     .catch(function(error) {
        console.log(error);
    });

}

function onMapDone(dataMap) {
    /* assigns function to call when country is clicked on map */ 
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onCountryClick);
}

function hoverPopupTemplate(geography, data) {
    /* displays country name on hover */
    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
                    + '</div>';

    return template;
}

function onCountryClick(geography) {
    // set selector to '--'
    document.getElementById('country_selector').getElementsByTagName('option')[0].selected = '--';
    
    let country_abbreviation = geography.id;
    displayCountryInfo(country_abbreviation);
}

function displayCountryInfo(country_abbreviation){
    /* displays country info for given abbreviation */
    let url = getAPIBaseURL() + 'country/' + country_abbreviation;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(country_summary){
        let ladder_data = []; // values for happiness/time chart
        let labels = []; // labels for chart

        for (let k = 0; k < country_summary.length; k++) {
            let country_info = country_summary[k];
            ladder_data.push(country_info['life_ladder']);
            labels.push(country_info['year']);
        }

        // next we create the summary of most recent data 
        let recent_data = country_summary[country_summary.length - 1]; 
        let summary = ''; 
        var no_data = (country_summary.length == 0);

        if(no_data){
            summary = ' This country has no information in our dataset';
        }else{
            summary = '<ul class="country-summary-list">'
                        + '<li><b>Year: </b>' + recent_data['year'] + '</li>'
                        + '<li><b>Life Ladder: </b>' + recent_data['life_ladder'] + '/10</li>'
                        + '<li><b>GDP Per Capita: </b>' + recent_data['gdp'] + '</li>'
                        + '<li><b>Social Support: </b>' + recent_data['social_support'] + '/1</li>'
                        + '<li><b>Life Expectancy: </b>' + recent_data['life_expectancy'] + '</li>'
                        + '<li><b>Freedom: </b>' + recent_data['freedom'] + '/1</li>'
                        + '<li><b>Generosity: </b>' + recent_data['generosity'] +'</li>'
                        + '</ul>';
        }

        var summaryElement = document.getElementById('summary');
        if(summaryElement){
            summaryElement.innerHTML = summary;
        }
        
        var countrySummaryTitle = document.getElementById('country-title');
        if(countrySummaryTitle){
            if(no_data){
                countrySummaryTitle.innerHTML = '';
            }else{
                countrySummaryTitle.innerHTML = country_summary[0]['country_name'];
            }
        }
        // make the happiness/time chart 
        var happiness_chart = document.getElementById('happiness_chart');
        console.log('next we check')
        if(happiness_chart){
            console.log('happiness_chart exists');
            happiness_chart.innerHTML = '<canvas id="my_chart" width="60%" height="40%"></canvas>';
        }
        // setup 
        const data = {
            labels: labels,
            datasets: [{
                label: '',
                data: ladder_data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        };
        //config
        const config = {
            type: 'line',
            data: data,
            options: {
                scales: {
                    y: {
                        title:{
                            display: true,
                            text: "Life Ladder Score"
                        }
                    },
                },
                plugins: {
                    title: {
                      display: true,
                      text: 'Happiness Over Time',
                    },
                  },
            }
          };
        //make the actual chart if there is data available 
        if(!no_data){
        const myChart = new Chart(
            document.getElementById('my_chart'),
            config
          );
        }
    })

    .catch(function(error) {
        console.log(error);
    });}

function createChartOnClick() {
    var chart = document.getElementById('chart');
    if(chart){
        chart.innerHTML = '<canvas id="myChart" width="60%" height="40%"></canvas>';
    }
    var y_axis_labels = {'social_support': 'Social Support', 
            'gdp':'GDP Per Capita', 'freedom':'Freedom', 'generosity':"Generosity", 
            'percieved_corruption': 'Percieved Corruption', 'life_expectancy':'Life Expectancy'};
    y_selector = document.getElementById('y_selector');
    if(x_selector && y_selector){
        x_axis = "life_ladder" // only compare to life ladder
        y_axis = y_selector.value
        
        let url = getAPIBaseURL() + "graph/" + x_axis + "/" + y_axis
        fetch(url, {method: 'get'})

        .then((response) => response.json())
        .then(function(chart_data){
            let plot_data = [];
            let labels = [];
            let x_max = 0;
            for(let i = 0; i < chart_data.length; i++){
                point_x = chart_data[i]["x"];
                if(point_x > x_max){
                    x_max = point_x;
                };
                point_y = chart_data[i]["y"];
                if(point_x != null && point_y != null){
                    plot_data.push({x:point_x,y:point_y});
                    labels.push(chart_data[i]["country_name"]);
                };
            };

            // chart.js graph below
            const data = {
                datasets: [{
                  label: 'Country data',
                  labels: labels, // list of labels goes here
                  data: plot_data,
                  backgroundColor: '#0B86B5', //blue dots
                  trendlineLinear: {
                    style: "rgb(43 ,66 ,255, 0.3)",
                    lineStyle: "dotted|solid",
                    width: 2
                }
                }],
              };
            const config = {
            type: 'scatter',
            data: data,
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title:{
                            display: true,
                            text: "Life Ladder Score"
                        }
                    },
                    y: {
                        title:{
                            display: true,
                            text: y_axis_labels[y_axis]
                        }
                      }
                },
                plugins: {
                    title: {
                      display: true,
                      text: 'Life Ladder Score vs ' + y_axis_labels[y_axis],
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                var label = tooltipItem.dataset.labels[tooltipItem.dataIndex];
                                var x_coord = tooltipItem.parsed.x;
                                var y_coord = tooltipItem.parsed.y;
                                return label + ' (' + x_coord + ', ' + y_coord + ')';
                            },

                        }

                    },
                  },
            }
            };
            // builds the chart on screen
            const myChart = new Chart(
                document.getElementById('myChart'),
                config
              );
        })
        
        .catch(function(error) {
            console.log(error);
        });
        
    }
        
    
}
