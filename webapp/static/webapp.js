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
            selectorBody += '<option value="' + country['id'] + '">'
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
    let countryID = this.value;

    let url = getAPIBaseURL() + 'country/' + countryID;

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
    // geography.properties.name will be the state/country name (e.g. 'Minnesota')
    // geography.id will be the state/country name (e.g. 'MN')
    var countrySummaryElement = document.getElementById('country-summary');
    if (countrySummaryElement) {
        //call api to get information for a particular country 
        var summary = '<p><strong>Country:</strong> ' + geography.properties.name + '</p>\n'
                    + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
        if (geography.id in extraCountryInfo) {
            var info = extraCountryInfo[geography.id];
            summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
        }

        countrySummaryElement.innerHTML = summary;
    }
}
