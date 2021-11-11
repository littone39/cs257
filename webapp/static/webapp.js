/*
 * books.js
 * Jeff Ondich, 27 April 2016
 * Updated, 5 November 2020
 */

window.onload = initialize;

function initialize() {
    loadCountriesSelector();

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
                            // + '<td>' + country_info['generosity'] + '</td>'
                            // + '<td>' + country_info['percieved_corruption'] + '</td>'
                            // + '<td>' + country_info['positive_affect'] + '</td>'
                            // + '<td>' + country_info['negative_affect'] + '</td>'
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