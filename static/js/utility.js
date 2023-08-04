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

    // Fetch countries and populate the select element
    const selectDrop = document.querySelector('#country');

    fetch('https://restcountries.com/v2/all') // Use the correct API endpoint
      .then(res => res.json())
      .then(data => {
        let output = '<option value="" disabled selected>Select a country</option>';
        data.forEach(country => {
          output += `<option value="${country.name}">${country.name}</option>`;
        })
        selectDrop.innerHTML = output;
      })
      .catch(err => {
        console.log(err);
      });

});
