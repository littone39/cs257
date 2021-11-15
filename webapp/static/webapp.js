/* Emily Litton and Jayti Arora
    webapp.js
    November 11, 2021 

    Adopted from books.js
    Jeff Ondich, 27 April 2016
    Updated, 5 November 2020
 */

window.onload = initialize;

var extraCountryInfo = {
    GBR: {population: 66700000, jeffhasbeenthere: true, fillColor: '#2222aa'},
    USA: {population: 328000000, jeffhasbeenthere: true, fillColor: '#2222aa'},
    IND: {population: 1353000000, jeffhasbeenthere: false, fillColor: '#aa2222'},
    JPN: {population: 125500000, jeffhasbeenthere: true, fillColor: '#aa2222'},
    PRT: {population: 10300000, jeffhasbeenthere: true, fillColor: '#aa2222'},
};

function initialize() {
    loadCountriesSelector();
    initializeMap();
    /*graph_button has to be clicked for chart to load
    let element = document.getElementById('graph_button');
    if (element) {
        element.onclick = createLineChart;
    }
    */
    let element = document.getElementById('country_selector');
    if (element) {
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
    //countryInfo = create a dictionary of country abreviation geography.properties.name =  
    var map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'world', // which map?
                            projection: 'mercator', // what map projection? 'equirectangular' is also an option
                            done: onMapDone, // once the map is loaded, call this function
                            //data: extraCountryInfo, // here's some data that will be used by the popup template lets replace this with our own data
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
    if (country_name == "United States of America"){
        country_name = "United States"
    }
    let url = getAPIBaseURL() + 'country/' + country_name;

    fetch(url, {method: 'get'})

    .then((response) => response.json())
    .then(function(country_summary){
        let tableBody = '';
        tableBody += '<tr>\
                        <td>Year</td>\
                        <td>Life Ladder Score</td>\
                        <td>GDP Per Capita</td>\
                        <td>Social Support</td>\
                        <td>Life Expectancy</td>\
                        <td>Freedom</td>\
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
                        + '</tr>\n';
                
        }

        var countrySummaryElement = document.getElementById('country-summary');
        if(countrySummaryElement){
            countrySummaryElement.innerHTML = tableBody;
    }})
    .catch(function(error) {
        console.log(error);
    });

    function createLineChart() {
        //x_axis = document.getElementById('x_var');
        //y_axis = document.getElementById('y_var');
        //check if either are null
        //add dict to API with column names to no spaces names

        // make sure x_axis or y_axis index is not null, else exclude that data

        // Data & x-axis labels
        var data = {
            series: [
                { data: [17, -2, 4, 9, 11, 7, 2] },
                { data: [1, 2, 3, 5, 8, 13, 21] }
            ]
        };

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
        var options = {}
    
        /* Initialize the chart with the above settings */
        new Chartist.Line('#sample-line-chart', data, options);
    }
        
    
}
