$(document).ready(function () {

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

    selectElement.innerHTML = countries.map(country => {
        if (typeof selectedCountry == 'undefined') {
            return `<option value="${country}">${country}</option>`;
        } else {
            const isSelected = country === selectedCountry ? 'selected' : '';
            return `<option value="${country}" ${isSelected}>${country}</option>`;
        }
    }).join('');
    if (typeof selectedCity != 'undefined' && typeof selectedCountry != 'undefined') {
        console.log("call fillCities");
        fillCitiesForCountry(selectedCountry.split(",")[1]);
    }
}

function fillCitiesForCountry(country_code) {
    const citySelect = document.getElementById('city');
    citySelect.innerHTML = '<option value="">Select City</option>';

    const overpassApiUrl = 'https://overpass-api.de/api/interpreter';
    const query = `[out:json];
            area["ISO3166-1:alpha3"="${country_code}"];
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
                if (typeof selectedCity != 'undefined' && cityName === selectedCity) {
                    option.selected = true;
                }
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

