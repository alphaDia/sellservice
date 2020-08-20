$(function () {
  const $signupForm = $("#signupForm");
  const url = $signupForm.attr("action");

  //$signupForm.hide().show("fast");

  /*$("#id_password1").attr({
    placeholder: "password",
  });
  $("#id_password2").attr({
    placeholder: "confirm password",
    ariaLabel: "confirmez votre mot de passe",
  });*/

  const button =
    '<button type="button" class="btn w-100 p-2 mb-2 button" id="signupbutton">Submit</button>';

  const link =
    '<small><a class="link" href="#">mot de passe oublie?</a></small>';

  let alert_danger =
    '<div class="alert alert-danger alert-dismissible fade show mt-4 d-none" role="alert">';
  alert_danger += "Please type a valid email or password .";
  alert_danger +=
    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">';
  alert_danger += '<span aria-hidden="true">&times;</span></button></div>';

  $("#signupbutton").on("click", function (e) {
    e.stopPropagation();

    if (v_form.form()) {
      $.ajax({
        type: "POST",
        url: url,
        data: $signupForm.serialize(),
        datatype: "json",
        success: function (response) {
          const { success, form_html, redirect_url } = response;
          if (!success) {
            $signupForm.html(form_html).append(button);
            $(".password_lost").next().after(link);
            $(".alert-danger").removeClass("d-none").addClass("d-block");
          } else window.location = `${redirect_url}`;
        },

        beforeSend: function () {
          let spinner =
            "<img src='{% static 'ss/images/small_loading.svg' %}' alt='loading' />";
          spinner +=
            ' <span class="sr-only">Verfing...</span> <span class="ml-2">patientez svp</span>';
          $("#signupbutton").attr("disabled", true).html(spinner);
        },

        complete: function () {
          $("#signupbutton").attr("disabled", false).html("Connecter");
        },

        error: function () {
          alert("error occured");
        },
      });
    }
  });

  $("div.mount-alert").on("click", function (event) {
    $(event.currentTarget).html(alert_danger);
  });
});
