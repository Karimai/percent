$(document).ready(function () {
    var dateInputs = ['start-date', 'end-date'];
    var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";

    for (var i = 0; i < dateInputs.length; i++) {
        var input = $('input[name="' + dateInputs[i] + '"]');
        input.datepicker({
            format: 'yyyy-mm-dd',
            container: container,
            todayHighlight: true,
            autoclose: true,
        });
    }

    $(window).on('resize', function () {
        if ($(this).width() > 800) {
            $('.navigation').css({
                'display': 'flex'
            });
        } else {
            $('.navigation').css({
                'display': 'none'
            });
        }
    });

});

// Assuming your CSV file is named "country.csv" and is in the same directory as this HTML file.
const csvFilePath = '../static/countries.csv';
async function fetchCSVFile(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${filePath}. Status: ${response.status}`);
        }
        return await response.text();
    } catch (error) {
        console.error('Error fetching CSV file:', error);
        return null;
    }
}

const selectElement = document.getElementById('country');
async function populateCountryDropdown() {
    const csvData = await fetchCSVFile(csvFilePath);

    if (!csvData) {
        selectElement.innerHTML = '<option disabled selected>Select a country</option>';
        return;
    }

    const countries = csvData.split('\n').map(country => country.trim());

    selectElement.innerHTML = countries.map(country => `<option value="${country}">${country}</option>`).join('');
}

function fillCitiesForCountry(country_code) {

    const citySelect = document.getElementById('city');
    citySelect.innerHTML = '<option value="">Select City</option>';

    const overpassApiUrl = 'https://overpass-api.de/api/interpreter';
    const query = `[out:json];
                area["ISO3166-1"="${country_code}"];
                node["place"="city"](area);
                out;`;

    axios.post(overpassApiUrl, query)
        .then(response => {
            const cities = response.data.elements;

            cities.forEach(city => {
                const cityName = city.tags['name:en'] || city.tags.name;
                const option = document.createElement('option');
                option.value = cityName;
                option.textContent = cityName;
                citySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
        });

}

selectElement.addEventListener('change', function () {
    const selectedCountry = selectElement.value;
    country_code = selectedCountry.split(",")[1];
    fillCitiesForCountry(country_code);
});

document.addEventListener('DOMContentLoaded', populateCountryDropdown);

