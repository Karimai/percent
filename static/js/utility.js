$(document).ready(function(){
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
});
