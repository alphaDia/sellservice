$(function () {
  $(".side-navbar").on("click", function (ev) {
    $(".active-link").removeClass("active-link");
    const href = $(ev.target).addClass("active-link").attr("href");

    if (!$(href).hasClass("active")) {
      $(".active").removeClass("active").hide();
      $(href).addClass("active");

      $(href).show("fast");
    }
  });

  const button =
    '<button type="submit"  class="btn w-100 p-2" id="save-button">Save</button>';

  const $updateForm = $("#updateProfileForm");
  const url = $updateForm.attr("action");

  $updateForm.on("submit", function (e) {
    e.preventDefault();

    $.ajax({
      type: "POST",
      url: url,
      data: $updateForm.serialize(),
      datatype: "json",
      success: function (response) {
        const { success, redirect_to, profileUpdateForm } = response;
        if (success) {
          location = redirect_to;
        } else $updateForm.html(profileUpdateForm).append(button);
      },

      beforeSend: function () {
        let spinner =
          '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        spinner +=
          ' <span class="sr-only">Loading...</span><span> Saving... </span>';
        $("#save-button").attr("disabled", true).html(spinner);
      },

      complete: function () {
        $("#save-button").attr("disabled", false).html("Save");
      },

      error: function () {
        alert("error occured");
      },
    });
  });
});
