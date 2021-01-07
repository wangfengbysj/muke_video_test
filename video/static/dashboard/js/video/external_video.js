$(document).ready(function () {

    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return null;
    }

    var error = $.getUrlParam('error');
    var success = $.getUrlParam('success')
    if (error != null) {
        toastr.error(error, '警告')
    }else if (success != null) {
        toastr.success(success, '消息')
    }

    $('#createBtn').click(function () {
        $('#myModal').modal('show')
    })

    $('#videoSubmitBtn').click(function () {
        $('#videoForm').submit()

    });

    $('#videoForm').bootstrapValidator('validate')
        .on('success.form.bv', function (e) {
            console.log('success.form.bv');
            e.preventDefault();
            e.target.submit()
        });
});