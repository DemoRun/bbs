$("#login_btn").on("click", function () {
    $.ajax({
        url: "",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name = 'csrfmiddlewaretoken']").val(),
            user: $("#user_id").val(),
            pwd: $("#pwd_id").val(),
            valid_code: $("#valid_img").val(),
        },
        success: function (data) {
            console.log(data)
            if (data.state) {
                location.href = "/index/"
            } else {
                $(".error").text(data.msg)
            }
        }

    })
})
// 验证码刷新
$("#change_img").click(function () {
    $(this)[0].src += "?"
});