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
        element.onchange = onCountiresSelectionChanged;
    }
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/';
    return baseURL;
}

//Displays table of the country selected from selector
function loadCountriesSelector() {
    let url = getAPIBaseURL() + 'countries/';

    // Send the request to the API
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(countries) {
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        selectorBody += '<option value = "0">--</option>\n'
        for (let k = 0; k < countries.length; k++) {
            let country = countries[k];
            selectorBody += '<option value="' + country['country_name'] + '">'
                                + country['country_name']
                                + '</option>\n';
        }

        let selector = document.getElementById('country_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

//Displays table of the new country selected
function onCountiresSelectionChanged() {
    let countryName = this.value;

    let url = getAPIBaseURL() + 'country/' + countryName;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(world_happiness) {
        let tableBody = '';
        tableBody += '<tr>\
                        <td>Year</td>\
                        <td>Life Ladder Score</td>\
                        <td>GDP Per Capita</td>\
                        <td>Social Support</td>\
                        <td>Life Expectancy</td>\
                        <td>Freedom</td>\
                        </tr>\n'
        for (let k = 0; k < world_happiness.length; k++) {
            let country_info = world_happiness[k];
            tableBody += '<tr>'
                            + '<td>' + country_info['year'] + '</td>'
                            + '<td>' + country_info['life_ladder'] + '</td>'
                            + '<td>' + country_info['gdp'] + '</td>'
                            + '<td>' + country_info['social_support'] + '</td>'
                            + '<td>' + country_info['life_expectancy'] + '</td>'
                            + '<td>' + country_info['freedom'] + '</td>'
                            + '</tr>\n';
        }

        // Put the table body we just built inside the table that's already on the page.
        let countriesTable = document.getElementById('countries_table');
        if (countriesTable) {
          countriesTable.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
} 

function initializeMap() {
     
    //  let url = getAPIBaseURL() + 'countries';

    //  fetch(url, {method: 'get'})

    //  .then((response) => response.json())
    //  .then(function(happiness_scores){
    //     countryInfo = {};
    //     for(var i=0; i<happiness_scores.length;i++){
    //         var country = happiness_scores[i]
    //         green = 255 - (country["life_ladder"] * 20)
    //         blue = (country["life_ladder"] * 1000)
    //         color = "#00" + blue;
    //         countryInfo[country["id"]] = {fillColor:color};
    //         console.log(country["id"]);
    //     };
    var page_map = document.getElementById('map-container');
    
    if (page_map){
        //countryInfo = create a dictionary of country abreviation geography.properties.name =  
        var map = new Datamap({ element: page_map, // where in the HTML to put the map
                                scope: 'world', // which map?
                                projection: 'equirectangular', // what map projection? 'equirectangular' or 'mercator' is also an option
                                done: onMapDone, // once the map is loaded, call this function
                                //data: countryInfo, // here's some data that will be used by the popup template lets replace this with our own data
                                fills: { defaultFill: '#999999' }, // change this fill to the one corresponding to the data
                                geographyConfig: {
                                    //popupOnHover: false, // You can disable the hover popup
                                    //highlightOnHover: false, // You can disable the color change on hover
                                    popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                    borderColor: '#eeeeee', // state/country border color
                                    highlightFillColor: '#99dd99', // color when you hover on a state/country
                                    highlightBorderColor: '#000000', // border color when you hover on a state/country
                                }
                            });
    };
    
    //  })
    //  .catch(function(error) {
    //     console.log(error);
    // });
}

// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onCountryClick);
}

function hoverPopupTemplate(geography, data) {
    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
                    + '</div>';

    return template;
}

function onCountryClick(geography) {
    let country_name = geography.properties.name
    
    //make a dictionary between geography names of countries and our names
    var countryDict = {
        "Republic of the Congo": "Congo (Brazzaville)",
        "Democratic Republic of the Congo": "Congo (Kinshasa)",
        "Somaliland": "Somaliland region",
        "United Republic of Tanzania" : "Tanzania",
        "Taiwan" : "Taiwan Province of China",
        "Republic of Serbia" : "Serbia",
        "Macedonia" : "North Macedonia",
        "United States of America" : "United States"
      };

      if(country_name in countryDict){
          country_name = countryDict[country_name];
      }

    //Countries that have no information:
    /*
    Brunei : not
    Northern Cyprus : not
    Greenland : not
    French Guiana : not
    Faulkland Islands : not 
    Western Sahara : not
    Guinea Bussau : not
    Republic of the Congo : Congo (Brazzaville)
    Democratic Republic of the Congo : Congo (Kinshasa)
    Somaliland : Somaliland region
    Eritrea : not
    United Republic of Tanzania : Tanzania
    Equatorial Guinea : not
    Papa New Guinea :not 
    Puerto Rico : not
    The Bahamas : not 
    French Southern and Antarctic Lands : not
    Fiji : not
    Vanuatu :not 
    Solomon Islands : not
    Taiwan : Taiwan Province of China
    North Korea : not
    New Caledonia : not
    Republic of Serbia : Serbia
    Macedonia : North Macedonia
    United States of America : United States
     */
    
    let url = getAPIBaseURL() + 'country/' + country_name;

    fetch(url, {method: 'get'})

    .then((response) => response.json())
    .then(function(country_summary){
        let tableBody = '';
        
        if(country_summary.length == 0){
            tableBody += 'This country has no information in our dataset';
        }
        
        tableBody += '<tr>\
                        <td><b>Year</b></td>\
                        <td><b>Life Ladder Score</b></td>\
                        <td><b>GDP Per Capita</b></td>\
                        <td><b>Social Support</b></td>\
                        <td><b>Life Expectancy</b></td>\
                        <td><b>Freedom</b></td>\
                        <td><b>Generosity</b></td>\
                        </tr>\n'

        tableBody += '<tr>\
                        <td>(Year the data is from)</td>\
                        <td>(Cantril ladder score rating life on a scale of 0-10)</td>\
                        <td>(Average GDP per person)</td>\
                        <td>(Liklihood of having someone to rely on around you)</td>\
                        <td>(Average life span)</td>\
                        <td>(Satisfaction level with ability to choose what you want to do)</td>\
                        <td>(Liklihood of helping out one another)</td>\
                        </tr>\n'

        for (let k = 0; k < country_summary.length; k++) {
            let country_info = country_summary[k];
            tableBody += '<tr>'
                        + '<td>' + country_info['year'] + '</td>'
                        + '<td>' + country_info['life_ladder'] + '</td>'
                        + '<td>' + country_info['gdp'] + '</td>'
                        + '<td>' + country_info['social_support'] + '</td>'
                        + '<td>' + country_info['life_expectancy'] + '</td>'
                        + '<td>' + country_info['freedom'] + '</td>'
                        + '<td>' + country_info['generosity'] + '</td>'
                        + '</tr>\n';
                
        }

        var countrySummaryElement = document.getElementById('country-summary');
        if(countrySummaryElement){
            countrySummaryElement.innerHTML = tableBody;
        }
        var countrySummaryTitle = document.getElementById('country-title');
        if(countrySummaryTitle){
            countrySummaryTitle.innerHTML = country_name;
            // countrySummaryTitle..scrollIntoView();
        }

        window.location = window.location + '#summary';
    })

    .catch(function(error) {
        console.log(error);
    });}

function createChartOnClick() {
    x_selector = document.getElementById('x_selector');
    y_selector = document.getElementById('y_selector');
    title = document.getElementById("chart-title")
    if(x_selector && y_selector){
        x_axis = x_selector.value
        y_axis = y_selector.value
        if(title){
            title.innerHTML = x_axis + " vs " + y_axis;
        }
        let url = getAPIBaseURL() + "graph/" + x_axis + "/" + y_axis
        fetch(url, {method: 'get'})

        .then((response) => response.json())
        .then(function(chart_data){
            let plot_data = [];
            let x_max = 0
            for(let i = 0; i < chart_data.length; i++){
                point_x = chart_data[i]["x"];
                if(point_x > x_max){
                    x_max = point_x;
                };
                point_y = chart_data[i]["y"];
                if(point_x != null && point_y != null){
                    plot_data.push({x:point_x,y:point_y});
                };
            };
            
            labels = []
            for(let i=0; i<x_max; i++){
                labels.push(i);
            };
            var data = {
                labels: labels,
                series: [
                    {data : plot_data}
                ],
                
            };
            var options = {
                showLine: false
            };

            /* Initialize the chart with the above settings */
            new Chartist.Line('#sample-line-chart', data, options);

            // create chart.js graph below
            const new_data = {
                datasets: [{
                  label: 'Scatter Dataset',
                  data: plot_data,
                  backgroundColor: 'rgb(255, 99, 132)'
                }],
              };
            const config = {
            type: 'scatter',
            data: new_data,
            options: {
                scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
                },
                plugins: {
                    title: {
                      display: true,
                      text: 'Chart Title',
                    }
                  }
            }
            };
            const myChart = new Chart(
                document.getElementById('myChart'),
                config
              );

            
        })
        
        .catch(function(error) {
            console.log(error);
        });

        //check if either are null
        //add dict to API with column names to no spaces names

        // make sure x_axis or y_axis index is not null, else exclude that data

        // Data & x-axis labels

        

        /* x_data = [];
         y_data = [];
        for z in countries:
            check if not null
            x_data.append(z[x]) 
        series: [
                { data: x_data },
                { data: y_data }
            ] 
        */

    
        // There are many options you can add to a chart. For this
        // sample we're not using any. The documentation at Chartist's website
        // says "check the samples for a complete list", but honestly, they do
        // a mediocre job of pointing you to them.
        // https://gionkunz.github.io/chartist-js/
        
    }
        
    
}
